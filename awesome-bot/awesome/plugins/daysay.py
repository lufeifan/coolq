from nonebot import on_command,CommandSession
import nonebot
import requests,json
from datetime import datetime
import pytz

@on_command('say', aliases=('每日一句'))
async def everydaysay(session:CommandSession):
    says=session.state.get('says')
    url = 'http://open.iciba.com/dsapi/'
    res =requests.get(url)
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    data= res.json()
    content_e = data['content']
    content_c =data['note']
    img_url =data['fenxiang_img']
    # print(img_url)
    # await session.send_private_msg(user_id=1714004230, message=f'[CQ:sign,title=学习打卡,image=https://pub.idqqimg.com/pc/misc/files/20200216/732eb71557dd240a57e2dcd72841827c.png]')
    await session.send(content_e)
    await session.send(content_c)
    await session.send(f'[CQ:image,file={img_url}]')
    # 帐号: 1714004230 [CQ:record,file=4BB0291A4108FE4737A9546EC5514FDE.silk]
    # await session.send('[CQ:rich,text= 梦泪：人生注定是场孤独的旅行，原来这就是“团队的力量吗”？]')

