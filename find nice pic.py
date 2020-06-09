import urllib.request
import os
import re
class downLoadOOXX():
    def __init__(self):
        #双下划线前缀会导致Python解释器重写属性名称，以避免子类中的命名冲突。
        self.__page = 0#page当前访问的第几页
        self.__url = 'http://jandan.net/ooxx/MjAxOTEyMjItMQ==#comments'#应该是第一页的页面地址
        self.__nexturl = None #下一页的地址 为下一次下载存储网址
        self.__picurl = []#存储照片地址的列表
        self.__dir = '.\\OOXX'#存储照片的文件夹
        self.__headers = {}#头文件
        self.__headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        
    def __getResponse(self):#获取html语句 
        req = urllib.request.Request(self.__url,headers = self.__headers)
        response = urllib.request.urlopen(req)
        self.__page += 1#获取的页数增加 
        html = response.read().decode('utf-8')
        return html
    def __anaylist(self,html):#分析语句
        #利用正则表达式 获取图片和下一页的网址
        #找到下一页的位置并赋值
        #从compile()函数的定义中，可以看出返回的是一个匹配对象,与search联合使用可以匹配出有效信息
        nextUrlPattern = re.compile(r'<a title="Newer Comments" href="(//jandan.net/ooxx/\w+==#comments)" class="next-comment-page">上一页</a>')
        matchResult = nextUrlPattern.search(html)
        self.__nexturl = 'http:' + matchResult.group(1)
        #或得图片的网址：
        picUrlPattern = re.compile(r'<span class="righttext"><a href="/t/\d+">\d+</a></span><p><a href="(//\w+\.sinaimg\.cn/\w+/\w+\.jpg)" target="_blank" class="view_img_link" referrerPolicy="no-referrer">')
        matchResult = picUrlPattern.finditer(html)
        for eachPic in matchResult:
            self.__picurl.append('http:' + eachPic.group(1))
    def __downLoad(self):#下载图片
        try:
            os.mkdir(self.__dir)#创建文件夹：
        except Exception as reason:
            pass
        #下载图片
        try:
            os.mkdir(self.__dir + '\\' + str(self.__page))#创建子文件夹：
        except Exception as reason:
            pass
        index = 1
        for eachPic in self.__picurl:
            req = urllib.request.Request(eachPic,headers = self.__headers)
            response = urllib.request.urlopen(req)
            picName = self.__dir + '\\' + str(self.__page) + '\\' + str(self.__page) + '_' + str(index)+ '.jpg'
            with open(picName,'wb') as f:
                f.write(response.read())
            index += 1
    def action(self,number):#number是一次下载几页 具体的动作页,这个函数是提前准备的一个函数
        index = 0
        while index<number:
            html = self.__getResponse()#获取html语句 string
            self.__anaylist(html) #分析语句 完成self.__picurl的填写 和 self.__nexturl的记录
            self.__downLoad()#下载图片
            self.__url = self.__nexturl
            self.__picurl = []
            index = index + 1
            
print('嘿嘿，这是下载美图的爬虫哦')
test = downLoadOOXX()
try:
    number = int(input('请输入下载页数'))
    test.action(number)
except ValueError as reason:
    print('呀出错了，请您输入整数')
else:
    print('下载成功！')
while True:
    status = input('是否继续下载：（y/n）y是，n否:')
    if status == 'y':
        try:
            number = int(input('请输入下载页数'))
            test.action(number)
        except ValueError as reason:
            print('呀出错了，请您输入整数')
        else:
            print('下载成功！')
    elif status == 'n':
        break
    else:
        print('请正确选择是否继续下载h h h ')
