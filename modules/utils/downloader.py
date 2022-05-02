import os
import time
import math
import shutil
import requests
import subprocess
from .misc import touchdir
from alive_progress import alive_bar


'''下载器类'''
class Downloader():
    def __init__(self, videoinfo, session=None, **kwargs):
        self.videoinfo = videoinfo
        self.session = requests.Session() if session is None else session
        self.__setheaders(videoinfo['source'])
    '''外部调用'''
    def start(self):
        if self.videoinfo['ext'] in ['mp4']: 
            if isinstance(self.videoinfo['download_url'], list):
                return self.defaultmultivideopartdownload()
            else:
                return self.defaultsinglevideodownload()
        elif self.videoinfo['ext'] in ['m3u8']: 
            if isinstance(self.videoinfo['download_url'], list):
                return self.m3u8download('requests')
            else:
                return self.m3u8download('ffmpeg')
        else: 
            raise NotImplementedError('Unsupport download file type %s' % self.videoinfo['ext'])
    '''默认的下载函数'''
    def defaultsinglevideodownload(self):
        videoinfo, session, headers = self.videoinfo.copy(), self.session, self.headers.copy()
        touchdir(videoinfo['savedir'])
        with session.get(videoinfo['download_url'], headers=headers, stream=True) as response:
            if response.status_code not in [200]: return False
            total_size, chunk_size, downloaded_size = int(response.headers['content-length']), videoinfo.get('chunk_size', 1024), 0
            savepath = os.path.join(videoinfo['savedir'], f"{videoinfo['savename']}.{videoinfo['ext']}")
            text, fp = '[FileSize]: %0.2fMB/%0.2fMB', open(savepath, 'wb')
            with alive_bar(manual=True) as bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if not chunk: continue
                    fp.write(chunk)
                    downloaded_size += chunk_size
                    bar.text(text % (downloaded_size / 1024 / 1024, total_size / 1024 / 1024))
                    bar(min(downloaded_size / total_size, 1))
        return True
    '''下载多个mp4文件'''
    def defaultmultivideopartdownload(self):
        videoinfo = self.videoinfo.copy()
        touchdir(videoinfo['savedir'])
        savepath = os.path.join(videoinfo['savedir'], videoinfo['savename']+'.mp4')
        savepath = savepath.replace(' ', '')
        tmp_dir = f'tmp_{int(time.time())}'
        os.mkdir(tmp_dir)
        fp = open(f'{tmp_dir}/filelist.txt', 'w')
        for idx, url in enumerate(videoinfo['download_url']):
            self.videoinfo['download_url'] = url
            self.videoinfo['savedir'] = tmp_dir
            self.videoinfo['savename'] = f'{idx}'
            self.videoinfo['ext'] = self.videoinfo['split_ext']
            self.defaultsinglevideodownload()
            fp.write(f'file {idx}.{self.videoinfo["ext"]}\n')
        fp.close()
        self.videoinfo = videoinfo
        p = subprocess.Popen(f'ffmpeg -f concat -safe 0 -i {tmp_dir}/filelist.txt -y {savepath}')
        while True:
            if subprocess.Popen.poll(p) is not None: 
                shutil.rmtree(tmp_dir)
                return True
    '''下载m3u8文件'''
    def m3u8download(self, mode='ffmpeg'):
        assert mode in ['ffmpeg', 'requests']
        videoinfo = self.videoinfo.copy()
        touchdir(videoinfo['savedir'])
        savepath = os.path.join(videoinfo['savedir'], videoinfo['savename']+'.mp4')
        savepath = savepath.replace(' ', '')
        if mode == 'ffmpeg':
            download_url = videoinfo['download_url']
            if 'ffmpeg_headers' in videoinfo:
                ffmpeg_headers = videoinfo['ffmpeg_headers']
                p = subprocess.Popen(f'ffmpeg -headers "{ffmpeg_headers}" -i "{download_url}" {savepath}')
            else:
                p = subprocess.Popen(f'ffmpeg -i "{download_url}" {savepath}')
            while True:
                if subprocess.Popen.poll(p) is not None: 
                    return True
        else:
            tmp_dir = f'tmp_{int(time.time())}'
            os.mkdir(tmp_dir)
            fp = open(f'{tmp_dir}/filelist.txt', 'w')
            for idx, url in enumerate(videoinfo['download_url']):
                self.videoinfo['download_url'] = url
                self.videoinfo['savedir'] = tmp_dir
                self.videoinfo['savename'] = f'{idx}'
                self.videoinfo['ext'] = self.videoinfo['split_ext']
                self.defaultsinglevideodownload()
                fp.write(f'file {idx}.{self.videoinfo["ext"]}\n')
            fp.close()
            self.videoinfo = videoinfo
            p = subprocess.Popen(f'ffmpeg -f concat -safe 0 -i {tmp_dir}/filelist.txt -y {savepath}')
            while True:
                if subprocess.Popen.poll(p) is not None: 
                    shutil.rmtree(tmp_dir)
                    return True
    '''设置请求头'''
    def __setheaders(self, source):
        self.douyin_headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66',
        }
        self.bilibili_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Referer': 'http://player.bilibili.com/',
        }
        self.yinyuetai_headers = {}
        if hasattr(self, f'{source}_headers'):
            self.headers = getattr(self, f'{source}_headers')
        else:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            }