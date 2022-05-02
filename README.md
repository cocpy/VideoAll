# VideoAll
    All video download


## Installation
    pip install videoall


## How to import
    from videoall import video


## Examples
    
    from videoall import video

    config = {
        "logfilepath": "video.log",
        "proxies": {},
        "savedir": "download"
    }
    
    video_client = video.videoall(config=config)
    
    video_path = 'the video path'
    
    video_client.get_video(video_path)
    

### Support List
    Ted, CNTV, MGTV, Migu, Pipix, AcFun, Zhihu, Xigua, Iqiyi, Douyin, Haokan, Bilibili, Pipigaoxiao,
    Yinyuetai, Weibo, BaiduTieba, Ku6, Kuaishou, Sohu