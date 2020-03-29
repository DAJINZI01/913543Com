## [某个视频网站的分析下载 http://913543.com/](http://913543.com/)

### 1. 这个网站的视频分为两种

先来一张图片：镇楼。

![无心法师](images/wxfs.jpg)

#### 1.1 `index.m3u8`

#### 1.2 1还有一个解析`vip`的接口

[https://api.lfeifei.cn/super_vip.php?url=](https://api.lfeifei.cn/super_vip.php?url=)

通过这个接口，可以直接观看视频，里面没有广告，这有一个`DPlayer`的视频插件，具体这个插件是什么，我就不研究了。这个接口的用法也简单，把要看的`vip`视频的链接（可以从浏览器的地址栏窗口获取），j就是这个接口`url`参数的值然后浏览器就会跳出播放的窗口了。

但是我，也就了这个接口，就是，能不能直接通过这个拿到解析后的`vip`链接，但是好像失败了。这里就不想费功夫了。(^_^)

### 2. `m378`视频类别的下载

#### 2.1 `m3u8`请求响应信息

首先，可以看到，它请求了两次的`index.m3u8`文件（两次的`url`）不同，第一次请求的`url`: [https://www.yxlmbbs.com:65/20200303/QoHwYtCg/index.m3u8](https://www.yxlmbbs.com:65/20200303/QoHwYtCg/index.m3u8)

文件内容如下：

```python
#EXTM3U
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1500000,RESOLUTION=1080x608
/20200303/QoHwYtCg/1500kb/hls/index.m3u8
```

可以看到这里面，第一个有效的行就是，第二个存放了主要的视频`ts`信息的文件的`m3u8`文件的`url`，根据这个`url`发送请求可以得到下面的信息:

```python
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:4
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:3.183,
/20200303/QoHwYtCg/1500kb/hls/MXHDo1Me.ts
#EXTINF:3.44,
/20200303/QoHwYtCg/1500kb/hls/j1dPumQ1.ts
#EXTINF:2.48,
/20200303/QoHwYtCg/1500kb/hls/D3fgPIr6.ts
```

这里只放一部分的数据，总共有几千行。`m378`文件的下载，就是通过这个`m378`里面的请求地址进行发送的。

#### 2.2 如何获取第一次请求`m3u8`的`url`

经过分析，发现在这个视频播放的主页面，也就是`html`页面发现了：

```html
<script type="text/javascript">var player_data={"flag":"play","encrypt":0,"trysee":0,"points":0,"link":"\/bf\/25408-1-1.html","link_next":"\/bf\/25408-1-2.html","link_pre":"","url":"https:\/\/www.yxlmbbs.com:65\/20200303\/QoHwYtCg\/index.m3u8","url_next":"https:\/\/www.yxlmbbs.com:65\/20200303\/gzAruYXx\/index.m3u8","from":"158m3u8","server":"no","note":""}</script>
```

不难看到，这个里面的`player_data`下的`url`就是第一次请求`m3u8`的`url`。好了到这里是不是感觉整个网站，全部瓦解。**其实最关键的地方就是找到这个`player_data`信息**。

### 3. 需求：根据关键字下载视频

通过上面几个部分，我们已经掌握了，如何获取请求的`m3u8`的`url`。但是，这个`url`是通过在播放主页找到的。

现在的需求时，通过关键词下载视频。那么，我们就去看看，这个站点有没有搜索功能。发现，起始是有的。

接口: [[http://913543.com/vodsearch/%E4%B8%A4%E4%B8%96%E6%AC%A2-------------.html](http://913543.com/vodsearch/两世欢-------------.html)](http://913543.com/vodsearch/%E4%B8%A4%E4%B8%96%E6%AC%A2-------------.html)

是不是感觉这个接口太差劲啊。我也觉得。怎么弄横线。。。。。

然后，我们通过想这个接口填充参数，发送请求，得到视频的`id`值和总的集数`update_to_episodes`。因为这个播放主页的链接是由规律（http://913543.com/bf/{id}-1-{episode}.html）的所以，只获取了这两个值。

然后，要做的是就是循环请求播放主页，拿到`player_data`数据，然后请求两次`index.m3u8`文件，最后将视频保存到本地。

### 4. 代码

请到我的`github` [https://github.com/DAJINZI01/913543Com](https://github.com/DAJINZI01/913543Com)