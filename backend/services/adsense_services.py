from flask import jsonify
import requests
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

def sync_get_adsense_data(dateStart,dateEnd,channelName, bearerToken):
    url = "https://adsense.revcompass.in/get_adsense_data"
    print(f"Fetching AdSense data from {dateStart} to {dateEnd} for channel: {channelName}")

    payload = json.dumps({
        "data": {
            "clientName": "geetika",
            "dateStart": dateStart,
            "dateEnd": dateEnd,
            "countryName": [
                "All Countries"
            ],
            "channelName": channelName,
            "geodata": False,
            "accountName": "SIP",
            "currencyCode": "INR"
        }
    })
    headers = {
        'Authorization': bearerToken,
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)
    filtered_data = response.json().get('response', {}).get('data', [])
    return filtered_data

async def get_adsense_data(dateStart,dateEnd,channelName):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        token = await loop.run_in_executor(pool, login)
        error, bearerToken = token['err'], token['token']
        if bool(error):
            raise Exception('Email Or Password is wrong')
    
        return await loop.run_in_executor(pool, sync_get_adsense_data, dateStart,dateEnd, channelName,  bearerToken)

async def ads_earning(dateStart,dateEnd,channelName):
    try: 
        data = await get_adsense_data(dateStart,dateEnd,channelName)
        return data
    except Exception as e:
        return {"error": str(e)}

def login():
    url = "https://adsense.revcompass.in/user/login"
    payload = json.dumps({
            "username": "geetika",
            "password": "keg5oDL4RQQyH36"
    })
    headers = {
        'Content-Type': 'application/json',
    }
    
    response = requests.post(url,data=payload, headers=headers)
    return response.json()