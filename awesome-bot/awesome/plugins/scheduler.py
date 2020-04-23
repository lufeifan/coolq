from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

# @nonebot.scheduler.scheduled_job('cron', minute='*')
@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        # await bot.send_group_msg(group_id=777697417,message=f'现在{now.hour}:{now.minute}啦！')
        # await bot.send_group_msg(group_id=876013087,message=f'现在{now.hour}点啦！')
        await bot.send_group_msg(group_id=308050037,message=f'现在{now.hour}:{now.minute}啦！')
        # await bot.send_discuss_msg(group_id=1087470718,message=f'现在{now.hour}:{now.minute}啦！')
        await bot.send_private_msg(user_id=1714004230, message=f'现在{now.hour}:{now.minute}啦！')
        # await bot.send_private_msg(user_id=2674645084, message=f'现在{now.hour}:{now.minute}啦！')
    except CQHttpError:
        pass

