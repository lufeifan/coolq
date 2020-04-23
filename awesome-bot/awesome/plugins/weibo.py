import requests
from bs4 import BeautifulSoup
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot

@nonebot.scheduler.scheduled_job('cron',minute=30)
#@nonebot.scheduler.scheduled_job('interval', minutes=60)
async def _():
    bot = nonebot.get_bot()
    r=requests.get('https://tophub.today/n/KqndgxeLl9',headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
    soup = BeautifulSoup(r.text)
    result=[]
    for item in soup.find_all('a')[2:22]:
        result.append(item.get_text().strip().split('\n')[0])
    result='\n'.join(result)
    try:
        await bot.send_group_msg(group_id=777697417,message='微博热搜\n'+result)
        await bot.send_private_msg(user_id=1714004230,message='微博热搜\n'+result)
        
    except CQHttpError:
        pass
