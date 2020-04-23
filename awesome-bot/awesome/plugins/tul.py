import json,os
from typing import Optional
import requests
import base64
import aiohttp
from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression
from urllib import request
from PIL import Image
from lxml import etree
import random,jieba

# 定义无法获取图灵回复时的「表达（Expression）」
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)


# 注册一个仅内部使用的命令，不需要 aliases
@on_command('tuling')
async def tuling(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')
    imgurl = session.state.get('imgurl')
    msg=session.state.get('msg')
    print(msg)
    print("*"*40)
    # print(msg)
    print(imgurl)

    if imgurl:
        # 获取图片返回的文字
        s = await call_tupian_api(session,imgurl)
        # 有文字返回，爬取斗图网，搜索关键字
        if s:
            # 调用回复内容，随机获取关键字
            reply = await call_tuling_api(session, s)
            duanyu = jieba.lcut(reply)
            guanzijian = random.choice(duanyu)
            print(guanzijian)
            try:
                reply = await call_doutu_api(str(guanzijian))
                reply =str(reply).split('\'')[1]
                # 图片链接
                if reply:
                    await session.send(f'[CQ:image,file={reply}]')
                # 没图片链接
                else:
                     await session.send(message=reply)
            except :
                await session.send(render_expression(EXPR_DONT_UNDERSTAND))
        # 没文字，直接返回图片
        else:
            await session.send(message=msg)
    # await session.send(message)
    # 通过封装的函数获取图灵机器人的回复
    elif message:
        reply = await call_tuling_api(session, message)
        # 如果调用图灵机器人成功，得到了回复，则转义之后发送给用户
        # 转义会把消息中的某些特殊字符做转换，以避免 酷Q 将它们理解为 CQ 码
        if reply:
            await session.send(escape(reply))
        else:
            await session.send(render_expression(EXPR_DONT_UNDERSTAND))
        # await session.send(message)
    else:
        await session.send(message=msg)
        # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取图灵回复时的「表达」
        # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
        # await session.send(render_expression(EXPR_DONT_UNDERSTAND))

#不用@也可以(only_to_me=False)
@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    # print(session.msg_images)
    # print('msg_text:'+session.msg_text)
    # print("*"*30)
    # 以置信度 60.0 返回 tuling 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 tuling 命令
    # return IntentCommand(60.0, 'tuling', args={'message': session.msg_text})
    return IntentCommand(60.0, 'tuling', args={'msg':session.msg,'message': session.msg_text,'imgurl':session.msg_images})


async def call_tuling_api(session: CommandSession, text: str) -> Optional[str]:
    # 调用图灵机器人的 API 获取回复

    if not text:
        return None

    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg='+text

    # 构造请求数据

    try:
        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url) as response:
                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    return None
                # print(response.url)
                resp_payload = json.loads(await response.text())
                if resp_payload['content']:
                    print(resp_payload['content'])
                    return resp_payload['content']
                
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # 抛出上面任何异常，说明调用失败
        return None

async def call_tupian_api(session: CommandSession, imgurl: str):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'images')
    if not os.path.exists(path):
        os.mkdir(path)

    try:
        imgname =imgurl[0].split('=')[-1]+'.gif'
        request.urlretrieve(imgurl[0],os.path.join(path,imgname))

        im = Image.open(f'./images/{imgname}')
        newname=imgname.split('.')[0]

        for i, frame in enumerate(iter_frames(im)):
            frame.save(f'./images/{newname}.png',**frame.info)

        f = open(f'./images/{newname}.png', 'rb')
        img = base64.b64encode(f.read())

        params = {"image":img}
        access_token = '[24.b0c8f39e7c6d00efecc3ffcdace5d700.2592000.1587415328.282335-18985885]'
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            # print (response.json())
            if json.loads(response.text)['words_result']:
                # print(json.loads(response.text)['words_result'])
                words_result = response.json()['words_result']
                # print(words_result[0]['words'])
                word = ''
                for words in words_result:
                    # print('*'*30)
                    # print(words['words'])
                    word=word+words['words']
                    # word=''.join(words)
                # return words_result[0]['words']
                # print(word)
                return word
            else :
                return None
    except :
        pass
        # imgname =imgurl[0].split('=')[-1]+'.jpg'
        # print(os.getcwd())
        # request.urlretrieve(imgurl[0],os.path.join(path,imgname))
        # f = open(f'./images/{imgname}', 'rb')
        # img = base64.b64encode(f.read())
        # # print(img)
        # params = {"image":img}
        # access_token = '[24.b0c8f39e7c6d00efecc3ffcdace5d700.2592000.1587415328.282335-18985885]'
        # request_url = request_url + "?access_token=" + access_token
        # headers = {'content-type': 'application/x-www-form-urlencoded'}
        # response = requests.post(request_url, data=params, headers=headers)
        # if response:
        #     print (response.json())
        #     if json.loads(response.text)['words_result']:
        #         print(json.loads(response.text)['words_result'])
        #         words_result = response.json()['words_result']
        #         print(words_result[0]['words'])
        #         return words_result[0]['words']
        #     else :
        #         return None
    finally:
        pass

def iter_frames(im):
    try:
        i= 0
        while 1:
            im.seek(i)
            imframe = im.copy()
            if i == 0:
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass
# 返回斗图地址
async def call_doutu_api(keyworld):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    }
    # keyworld='天真'
    url ='https://www.doutula.com/search?keyword='+keyworld
    # print(url)
    r=requests.get(url,headers=headers)
    html=etree.HTML(r.text)

    reponse = html.xpath('//*[@id="search-result-page"]/div/div/div[2]/div/div[1]/div/div/a')[:20]
    imgurl_list= []
    for img in reponse:
        imgurl_list.append(img.xpath('./img/@data-backup'))
    # print(imgurl_list)
    # print(random.choice(imgurl_list))
    imgurl = str(random.choice(imgurl_list)).split('[')[1].split(']')[0]
    # print(imgurl)
    return str(imgurl)
    # return [CQ:image,file=random.choice(imgurl_list)]

# call_doutu_api()