from datetime import datetime
from nonebot import CommandSession
import nonebot
import pytz
import requests,json
from datetime import datetime

@nonebot.scheduler.scheduled_job('cron',hour=10, minute=1)
async def _da():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    url = 'http://open.iciba.com/dsapi/'
    res =requests.get(url)
    data= res.json()
    content_e = data['content']
    content_c =data['note']
    img_url =data['fenxiang_img']

    await bot.send_private_msg(user_id=1714004230, message=f'现在{now.hour}:{now.minute}啦！')
    await bot.send_private_msg(user_id=1714004230,message=content_e)
    await bot.send_private_msg(user_id=1714004230,message=content_c)
    await bot.send_private_msg(user_id=1714004230,message=f'[CQ:image,file={img_url}]')

    await bot.send_group_msg(group_id=777697417,message=content_e)
    await bot.send_group_msg(group_id=777697417,message=content_c)
    await bot.send_group_msg(group_id=777697417,message=f'[CQ:image,file={img_url}]')

    await bot.send_group_msg(group_id=308050037,message=content_e)
    await bot.send_group_msg(group_id=308050037,message=content_c)
    await bot.send_group_msg(group_id=308050037,message=f'[CQ:image,file={img_url}]')

    # await bot.send_group_msg(group_id=976867410,message=content_e)
    # await bot.send_group_msg(group_id=976867410,message=content_c)
    # await bot.send_group_msg(group_id=976867410,message=f'[CQ:image,file={img_url}]')
