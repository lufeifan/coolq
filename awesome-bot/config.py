from nonebot.default_config import *
import re

HOST = '0.0.0.0'
PORT = 8080
TULING_API_KEY = '6ddbd285a92e47a4b129e7ab0b6eb40a'
API_ROOT = 'http://127.0.0.1:5700'
SUPERUSERS = {1714004230}
# COMMAND_START = {'', '/', '!', '／', '！'}  #设置开头
COMMAND_START = ['', re.compile(r'[/!]+')]