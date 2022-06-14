# -*- coding: utf-8 -*-
import json
import os
import requests
import xml.etree.ElementTree as ET

WEATHER_URL_FORMAT = "http://wthrcdn.etouch.cn/WeatherApi?citykey={city}"
NOTIFICATION_FORMAT = "阿里云函数计算 今日天气播报\n\n城市: {city}\n温度: {temperature}°C\n风力: {level_wind}\n风向: {wind_direction}\n湿度: {humidity}\n日出: {sunrise}\n日落: {sunset}"

def handler(event, context):
    # Extract city and DingTalk webhook from environment variables
    webhook = os.getenv("webhook")
    city = os.getenv("city")

    # Fetch weather raw data
    response = requests.get(WEATHER_URL_FORMAT.format(city=city))
    xml_root = ET.fromstring(response.text)
    weather_dict = {}
    for child in xml_root:
        key = child.tag
        value = child.text
        if value != "":
            weather_dict[key] = value

    # Post to DingTalk chatbot
    data = {
        "msgtype": "text",
        "text": {
            "content": NOTIFICATION_FORMAT.format(city=weather_dict['city'], temperature=weather_dict['wendu'], level_wind=weather_dict['fengli'], wind_direction=weather_dict['fengxiang'], humidity=weather_dict['shidu'], sunrise=weather_dict['sunrise_1'], sunset=weather_dict['sunset_1'])
        }
    }
    requests.post(webhook, json=data)

    return
