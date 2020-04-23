#!/usr/bin/python3
# -*- coding: utf-8 -*-
#时间: 2020-04-09 15:42:14
from nonebot import CommandSession
import nonebot
import requests,json
from aiocqhttp.exceptions import Error as CQHttpError
@nonebot.scheduler.scheduled_job('interval', minutes=150)
# @nonebot.scheduler.scheduled_job('cron',hour=22, minute=17)
# @nonebot.scheduler.scheduled_job('cron', minute='*')
async def _da():
    bot = nonebot.get_bot()
    datas = getjuejin()
    for data in json.loads(datas)['data']:
        try:
            print(data["url"])
            await bot.send_private_msg(user_id=1714004230, message=f'[CQ:share,url={data["url"]},title={data["title"]}]')
            await bot.send_private_msg(user_id=1714004230, message=f'{data["url"]},{data["title"]}')
            # await bot.send_private_msg(user_id=1714004230, message='[CQ:sign,title=学习打卡,image=https://pub.idqqimg.com/pc/misc/files/20200216/732eb71557dd240a57e2dcd72841827c.png]')

        except CQHttpError:
            pass

def getjuejin():
    headers={
        'Host': 'web-api.juejin.im',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'X-Agent': 'Juejin/Web',
        'Origin': 'https://juejin.im',
        'Referer': 'https://juejin.im/welcome/ai/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90'
    }
    params = {"operationName":"","query":"","variables":{"tags":["58e753128d6d810061760e56"],"category":"57be7c18128fe1005fa902de","first":10,"after":"","order":"POPULAR"},"extensions":{"query":{"id":"653b587c5c7c8a00ddf67fc66f989d42"}}}
    r=requests.post('https://web-api.juejin.im/query',json=params,headers=headers,)
    datas = r.json()['data']['articleFeed']['items']['edges']
    mas = {}
    result = []
    for data in datas:
        dic = {}
        dic['url'] = data['node']['originalUrl']
        dic['title'] = data['node']['title']
        result.append(dic)
    mas['data'] = result
    return json.dumps(mas,ensure_ascii=False)
