from fastapi import APIRouter, Depends
from uuid import uuid4
from services.aws_s3 import AWSS3Service
from utils.auth import authenticate
from typings.auth import UserAccount
from typings.file import FileInput
import os
from twilio.rest import Client
import requests   
import json

router = APIRouter()


@router.post("/outbound", status_code=201)
def make_call():
    """Description"""
    account_sid = "AC0809f246a1527efd247543913845f4e9" #self.get_env_key("TWILIO_ACCOUNT_SID")
    auth_token = "1aad3dafaf6e83e0fce776670837d253" #self.get_env_key("TWILIO_AUTH_TOKEN")
    from_number = "+13345648359" #self.get_env_key("TWILIO_FROM_NUMBER")
    to='+995597570605',
    client = Client(account_sid, auth_token)
    call = client.calls.create(
                url='http://demo.twilio.com/docs/voice.xml',
                to='+13345648359',
                from_="+995597570605"
            )
    print(call.sid)
    return {
        "outbound": True,
    }
    
@router.post("/webhook", status_code=201)
def make_call():
    """Make call"""

    return {
        "true": True,
    }


@router.post("/text-to-speech", status_code=201)
def text_to_speech():
    """Text to speech"""

    url = "https://play.ht/api/v2/tts/stream"

    payload = {
        "text": "Hello Giga, How are you, I want ti introduce our products, which one would you like?",
        "voice": "larry",
        "quality": "draft",
        "output_format": "mp3",
        "speed": 1,
        "sample_rate": 24000
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AUTHORIZATION": "Bearer 56b08c59cc2e44c5bbdb2e6b9ac7b038",
        "X-USER-ID": "NF9Psaqy2cOKRDqrUVs2bYnELWW2"
    }

    response = requests.post(url, json=payload, headers=headers)

    response_json = json.loads(response.text)

    return response_json

@router.post("/speech-to-text", status_code=201)
def text_to_speech():
    """Text to speech"""

    url = "https://play.ht/api/v2/tts/stream"

    payload = {
        "text": "Hello Giga, How are you, I want ti introduce our products, which one would you like?",
        "voice": "larry",
        "quality": "draft",
        "output_format": "mp3",
        "speed": 1,
        "sample_rate": 24000
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AUTHORIZATION": "Bearer 56b08c59cc2e44c5bbdb2e6b9ac7b038",
        "X-USER-ID": "NF9Psaqy2cOKRDqrUVs2bYnELWW2"
    }

    response = requests.post(url, json=payload, headers=headers)

    response_json = json.loads(response.text)
    
    url = response_json["href"]

    #Get Audio
    payload = {}
    headers = {
    'Authorization': 'Bearer 56b08c59cc2e44c5bbdb2e6b9ac7b038',
    'X-USER-ID': 'NF9Psaqy2cOKRDqrUVs2bYnELWW2'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response
