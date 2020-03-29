# coding=utf-8
from utils.mym3u8 import MyM3u8

from lxml import etree
import requests
import re
import json
import os


class _913543Com(object):
    def __init__(self):
        self.host = "http://913543.com"
        self.video_host = "https://www.yxlmbbs.com:65"
        self.search_url = "http://913543.com/vodsearch/%s-------------.html" # 不是我说这个搜索接口太什么
        self.episode_url = "%s/bf/%d-1-%d.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }
        self.m3u8 = MyM3u8()
        self.episode_title = "第%d集.ts"

    def my_get(self, url):
        response = requests.get(url, headers=self.headers)
        print("%s [%d]" % (response.url, response.status_code))
        return response

    def get_play_data(self, play_url):
        """
        通过play_url，拿到播放的数据
        :params play_url: 播放的url链接
        :return: player_data 字典数据
        """
        html = self.my_get(play_url).content.decode("utf-8")
        player_data  = json.loads(re.search(r"player_data=({.+})", html).group(1))
        return player_data

    def get_index_m3u8(self, player_data):
        """
        通过player_data，拿到播放的index.m3u8文件
        :params player_data: 播放相关的数据 字典
        :return: m3u8 列表
        """
        html = self.my_get(player_data["url"]).content.decode("utf-8")
        ts_list = self.m3u8.parse_m3u8(html)
        if not ts_list:
            return []
        html = self.my_get("%s%s" % (self.video_host, ts_list[0])).content.decode("utf-8")
        return self.m3u8.parse_m3u8(html)

    def get_episode_list_by_keyword(self, keyword):
        # 1. 拿到播放主页
        html = self.my_get(self.search_url % keyword).content.decode("utf-8")
        # 2. 解析获取集数和影片id
        elem = etree.HTML(html)
        update_episodes = int(re.search(r"\d+", elem.xpath('//span[@class="pic-text text-right"]/text()')[0]).group())
        video_id = int(re.search(r"/js/(\d+)\.html",elem.xpath('//div[@class="detail"]/h4[@class="title"]/a/@href')[0]).group(1))
        return (video_id, update_episodes)

    def download_by_play_url(self, play_url, file_name="download.ts"):
        """
        根据play_url播放链接，下载视频
        :params play_url: 播放链接
        :params file_name: 下载存放的文件名
        :return: 
        """
        print(play_url)
        index_m3u8 = self.get_index_m3u8(self.get_play_data(play_url))
        if not index_m3u8:
            print("index.m3u8文件不存在，无法下载。")
            return
        self.m3u8.download_m3u8_video(self.video_host, index_m3u8, file_name)

    def download_by_keyword(self, keyword, folder="data", index=None):
        """
        根据关键字下载视频
        :params keyword: 关键字 字符串
        :params folder: 存放的文件夹
        :params index: 指定下载第几集, 从1开始, 如果为None, 表示下载所有
        :return: 成功标志 True表示下载成功, False表示下载失败
        """
        # 1. 创建文件夹
        if not os.path.exists(folder):
            os.mkdir(folder)
        # 2. 创建视频文件夹
        video_folder = "%s/%s" % (folder, keyword)
        if not os.path.exists(video_folder):
            os.mkdir(video_folder)
        # 3. 下载剧集
        video_id, update_episodes = self.get_episode_list_by_keyword(keyword)
        if not index: # 表示下载到跟新的集数
            for index in range(1, update_episodes+1):
                self.download_by_play_url(self.episode_url % (self.host, video_id, index), "%s/%s" % (video_folder, self.episode_title % index))
            return True
        if index > update_episodes or index < 0: # 一集
            print("index: %d error." % index)
            return False
        
        self.download_by_play_url(self.episode_url % (self.host, video_id, index), "%s/%s" % (video_folder, self.episode_title % index))
        return True
        
        

if __name__ == "__main__":
    v = _913543Com()
    # print(v.get_play_data("http://913543.com/bf/25408-1-1.html"))
    # player_data = v.get_play_data("http://913543.com/bf/25408-1-1.html")
    # v.get_index_m3u8(player_data)
    # v.download_by_play_url("http://913543.com/bf/25408-1-1.html", "data/1.ts")
    # v.get_episode_list_by_keyword("无心法师3")
    v.download_by_keyword("无心法师", index=20) # 到了这里只能这个网站的保存下来的视频，但是不能看vip视频

    # 别人做的vip视频，api接口
    # https://api.lfeifei.cn/super_vip.php?url= 这个地址可以看但是拿不下来 播放的地址
    # ay9lbjh4cVMwM2VPamttMnpUNWhWUDRlZHZjaS9DR3ZaMTQvQUJ0SkVOakZtRWFHUEhtNW9SY2hZRXJUaU9uRWtLajkybHRuWnU0TElVZjZYaDBBekFuR255MDJFdDV1aTNMeFF4U0Nyb2pCSEtEUzRRdG0yQjdmZ214dXA3NDZtMkNvNzdNWk9SQk0wMDhLM3BBemo0cndiRlpnNThWVEdVRm9iQUE2bS9Kd2FEK1FLVDkvbHFBOHNkQlJ5YWpCT1ZxYnZMS3VwOTVFNGExdEZTdWpYeW1XNXF0ejBrcENtU3BpSGJQM00wT3lRZU5LaHZBRDNTZW1XWmllY0xyZTJoUUJkM3hzOFRXeHB5ZUw4VDlBbFFFUTJDZFVzTDhvNEtmOWgrK2JmSVE9