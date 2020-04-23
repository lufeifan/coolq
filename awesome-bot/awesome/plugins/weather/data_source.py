import aiohttp,json
async def get_weather_of_city(city: str) -> str:
    url = 'http://v.juhe.cn/weather/index?key=c096ce51302bb2f29c1e920a44904f81&cityname='+city

    # 构造请求数据
    payload = {
        # 'key':'c096ce51302bb2f29c1e920a44904f81',
        'cityname':city,
        # 'time':'1418745237',
        
    }
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url) as response:
            if response.status != 200:
                return None
            resp_payload = json.loads(await response.text())
            if resp_payload['result']:
                reason =resp_payload['result']['sk']
                return f'{city}的天气:\n当前温度:{reason["temp"]}\n当前湿度:{reason["humidity"]}\n当前风向:{reason["wind_direction"]}\n当前风力:{reason["wind_strength"]}\n更新时间:{reason["time"]}'
            else:
                return "查询城市错误"
