#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
import nonebot
import pytz
import requests,json
import time 
from aiocqhttp.exceptions import Error as CQHttpError

# @nonebot.scheduler.scheduled_job('cron', minute='*')
@nonebot.scheduler.scheduled_job('cron',hour=12, minute=0)
async def _da():
    bot = nonebot.get_bot()
    idlist = getmas()
    # idlist =['1408901739', '1436961077']
    for id in idlist:
        try:
            # 570919436
            await bot.send_group_msg(group_id=777697417, message=f'[CQ:music,type=163,id={id}]')
            await bot.send_private_msg(user_id=1714004230, message=f'[CQ:music,type=163,id={id}]')
            await bot.send_private_msg(user_id=3106349854, message=f'[CQ:music,type=163,id={id}]')
            await bot.send_group_msg(group_id=570919436, message=f'[CQ:music,type=163,id={id}]')
        except CQHttpError:
            pass
def getmas():
    browser = webdriver.PhantomJS()
    browser.get("https://music.163.com")
    browser.implicitly_wait(10)  # 等待js代码加载完毕
    iframe_elemnt = browser.find_element_by_id("g_iframe")
    browser.switch_to.frame(iframe_elemnt)
    elements = browser.find_elements_by_xpath('//div[@id="top-flag"]//dl[1]//dd//ol//li')[:5]
    idlist=[]
    for element in elements:
        title = element.find_element_by_xpath('./a').get_attribute("href")
        idlist.append(title.split('=')[1])
    # print(idlist)
    browser.quit()
    return idlist

    
