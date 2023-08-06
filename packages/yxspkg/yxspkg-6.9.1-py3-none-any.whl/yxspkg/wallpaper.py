from urllib import request
import ssl
import time 
from pathlib import Path
import os
import random 
import click
import subprocess
global_urls = ['https://eatshit.cn/',
            'https://acg.yanwz.cn/wallpaper/api.php',
            'https://api.lyiqk.cn/scenery',
            'https://random.52ecy.cn/randbg.php',
            'https://img.paulzzh.com/touhou/random',
            'https://www.dmoe.cc/random.php',
            'https://api.cyfan.top/acg',
            'https://imgapi.cn/bing.php',
            'https://source.unsplash.com/random',
            'https://source.unsplash.com/user/tkirkgoz/1600x900',
            'https://source.unsplash.com/user/erondu/1600x900']
def get_picture_from_url(output,url):
    ssl._create_default_https_context = ssl._create_unverified_context
    opener=request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    request.install_opener(opener)
    request.urlretrieve(url,output)
def get_picture_from_url_set(output):

    url = random.choice(global_urls)
    get_picture_from_url(output,url)
def set_wallpaper(screen_name='DP-2',url=None):
    abs_path = Path.home()/'.yxspkg'/'wallpapers'
    if not abs_path.is_dir():
        os.makedirs(abs_path)
    abs_path = abs_path / (str(int(time.time()))+'.jpg')
    if url:
        get_picture_from_url(abs_path,url)
    else:
        get_picture_from_url_set(abs_path)
    if not abs_path.exists() or abs_path.stat().st_size<1000:
        for _ in range(10):
            get_picture_from_url_set(abs_path)
            if abs_path.exists() and abs_path.stat().st_size>1000:
                break 
    if abs_path.exists() and abs_path.stat().st_size>1000:
        cmd = f'dbus-send --dest=com.deepin.daemon.Appearance /com/deepin/daemon/Appearance --print-reply com.deepin.daemon.Appearance.SetMonitorBackground string:"{screen_name}" string:"file:///{abs_path}"'
        subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")

@click.command()
@click.option('--screen','-s',default=None,help='设置显示器的名称，右键显示设置可以查看')
@click.option('--url',default=None,help='指定url')
@click.option('--show_urls',default=False,help='显示内置的url')
@click.option('--time_interval','-t',default=0,help="壁纸更换时间间隔，默认0s")
def main(screen,url,show_urls,time_interval):
    if show_urls:
        for i in global_urls:
            print(i)
    if screen:
        while True:
            set_wallpaper(screen,url)
            if time_interval>0:
                time.sleep(time_interval)
            else:
                break
if __name__=='__main__':
    main()