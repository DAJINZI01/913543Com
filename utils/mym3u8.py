# coding=utf-8
import requests

class MyM3u8(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }

    @staticmethod
    def parse_m3u8(m3u8_text):
        """
        解析m3u8文件
        :params m3u8_text: 文本字符串
        :return: 列表
        """
        ts_list = []
        if not m3u8_text.startswith("#"):
            return ts_list
        text_lines = m3u8_text.split("\n")
        for line in text_lines:
            if not line.startswith("#") and line:
                ts_list.append(line)
        return ts_list

    def download_m3u8_video(self, video_host, ts_list, file_name):
        """
        根据ts_list，下载ts格式的视频
        """
        f = open(file_name, "wb")
        for ts in ts_list:
            f.write(requests.get("%s%s" % (video_host, ts)).content)
            print("%s [ok]" % ts)
        f.close()
        print("%s [ok]" % file_name)



if __name__ == "__main__":
    f = open("./utils/index.m3u8", encoding="utf-8")
    m3u8_text = f.read()
    f.close()
    m = MyM3u8()
    # print(m.parse_m3u8(m3u8_text))
    ts_list = m.parse_m3u8(m3u8_text)
    m.download_m3u8_video("https://www.yxlmbbs.com:65", ts_list, "1.ts")