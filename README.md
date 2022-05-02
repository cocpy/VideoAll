# VideoAll
    All video download


## Installation
    pip install videoall


## How to import
    from videoall import videoall


## Examples
    
    from videoall import videoall

    config = {
        "logfilepath": "video.log",
        "proxies": {},
        "savedir": "download"
    }
    
    video_client = videoall(config=config)
    
    video_path = 'the video path'
    
    video_client.get_video(video_path)
    

### Support List
    央视网	
    芒果TV	
    咪咕视频	
    AcFun视频	
    抖音	
    好看视频	
    B站视频	
    知乎视频	
    西瓜视频	
    爱奇艺视频	
    TED视频	
    皮皮搞笑	
    皮皮虾	
    音悦网	
    微博	
    百度贴吧	
    快手视频	
    酷6网	
    搜狐TV
