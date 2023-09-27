from fastapi import APIRouter, Depends
from uuid import uuid4
from utils.auth import authenticate
from typings.auth import UserAccount
from typings.file import FileInput
import os
from twilio.rest import Client
import requests   
import json
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import logging
import base64
from twilio.twiml.voice_response import VoiceResponse

router = APIRouter()

domain =  "l3agi.ngrok.dev"

@router.post("/call/outbound", status_code=200)
def make_call():
    """Description"""
    account_sid = "AC3a1cd89b4f2908071affc1f56f23b2d5" #self.get_env_key("TWILIO_ACCOUNT_SID")
    auth_token = "826fd14a632821335b98743de5eb04a0" #self.get_env_key("TWILIO_AUTH_TOKEN")
    # from_number = "+13345648359" #self.get_env_key("TWILIO_FROM_NUMBER")
    # to='+995597570605',
    
    
    say =f"""<Say>Ahoy there!</Say>"""
    
    twiml=f"""
    <Response>
        <Start>
            <Stream url="wss://{domain}/twilio/media" />
        </Start>
        <Play oop="0>https://api.twilio.com/cowbell.mp3</Play>
        <Record timeout="10" transcribe="true" />
    </Response>
    """
    client = Client(account_sid, auth_token)
    call = client.calls.create(
                record=True,
                # url='http://demo.twilio.com/docs/voice.xml',
                twiml=twiml,               
                
                
                to='+18052901594',
                # to='+995597570605',
                
                
                # from_='+18052901594'
                from_='+995597570605'
            )
    print(call.sid)
    return {
        "sid": call.sid,
    }
    
    
@router.post("/voice/webhook/voice", status_code=200)
def webhook_voice():
    """Make call"""

    return {
        "true": True,
    }
    
@router.post("/webhook/fails", status_code=200)
def webhook_fails():
    """Make call"""

    return {
        "true": True,
    }
    
@router.post("/voice/call-status-change", status_code=201)
def voice_call_status_change():
    """Make call"""

    return {
        "true": True,
    }



@router.post("/record")
def record():
    """Returns TwiML which prompts the caller to record a message"""
    # Start our TwiML response
    response = VoiceResponse()

    # Use <Say> to give the caller some instructions
    response.say('Hello. Please leave a message after the beep.')

    # Use <Record> to record the caller's message
    response.record(timeout=10, transcribe=True)

    # End the call with <Hangup>
    response.hangup()

    return str(response)

@router.websocket("/media")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logging.info("Connection accepted")
    has_seen_media = False
    message_count = 0
    while True:
        try:
            message = await websocket.receive_text()
        except WebSocketDisconnect:
            logging.info("Connection closed. Received a total of {} messages".format(message_count))
            break

        data = json.loads(message)

        if data['event'] == "connected":
            logging.info("Connected Message received: {}".format(message))
        if data['event'] == "start":
            logging.info("Start Message received: {}".format(message))
        if data['event'] == "media":
            if not has_seen_media:
                logging.info("Media message: {}".format(message))
                payload = data['media']['payload']
                logging.info("Payload is: {}".format(payload))
                chunk = base64.b64decode(payload)
                logging.info("That's {} bytes".format(len(chunk)))
                logging.info("Additional media messages from WebSocket are being suppressed....")
                has_seen_media = True
        if data['event'] == "stop":
            logging.info("Stop Message received: {}".format(message))
            break
        message_count += 1
        

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
