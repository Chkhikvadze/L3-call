from fastapi import APIRouter, Depends
from uuid import uuid4
from utils.auth import authenticate
from typings.auth import UserAccount
from typings.file import FileInput
import os
from twilio.rest import Client
import requests   
import json
from fastapi import FastAPI, WebSocket, Request, Response
from starlette.websockets import WebSocketDisconnect
import logging
import base64
from twilio.twiml.voice_response import VoiceResponse
from pydantic import BaseModel
from controllers.deepgram import transcribe_audio_with_deepgram
import asyncio
import websockets
import base64
import httpx

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from twilio.twiml.voice_response import Connect, VoiceResponse


router = APIRouter()

domain =  "l3agi.ngrok.dev"
socket_url = 'wss://l3agi.ngrok.dev/twilio/media'
# socker_url = 'wss://localhost:4000/twilio/media'


@router.post("/call/connect", status_code=200)
def connect(req: Request):
    response = VoiceResponse()
    connect = Connect(action='https://l3agi.ngrok.dev/twilio/twiml')
    connect.virtual_agent(
        connector_name='connector-friendly-name-giga', status_callback='https://l3agi.ngrok.dev/twilio/voice/connector/cx'
    )
    response.append(connect)

    print(response)
    return 1

@router.post("/call/outbound", status_code=200)
# def make_call(req: Request, res: Response):
#     """Description"""
#     account_sid = "AC3a1cd89b4f2908071affc1f56f23b2d5" #self.get_env_key("TWILIO_ACCOUNT_SID")
#     auth_token = "6c176f0f6495f82fa6b7ed06eb1c64ae" #self.get_env_key("TWILIO_AUTH_TOKEN")
#     # from_number = "+13345648359" #self.get_env_key("TWILIO_FROM_NUMBER")
#     # to='+995597570605',
    
    
#     say =f"""<Say>Ahoy there, are you here Giga!</Say>"""
#     # play = f"""<Play oop="0>https://l3agi.ngrok.dev/twilio/audio-proxy/cowbell.mp3</Play>"""
#     # play = f"""<Play loop="10">https://api.twilio.com/cowbell.mp3</Play>"""
#     # play = f"""<Play loop="1">https://l3agi.ngrok.dev/twilio/audio-proxy/cowbell.mp3</Play>"""
    
#     record_url = "https://l3agi.ngrok.dev/twilio/voice/record"
#     record = f"""<Record timeout="30" transcribe="true" recordingStatusCallback="{record_url}"/>"""
                    
                    
#     start = f"""<Start>
#                     <Stream url="{socket_url}" />
#                 </Start>"""
#     twiml=f"""
#     <Response>
#         {start}
#         {record}
#         {connect}
#     </Response>
#     """
#     client = Client(account_sid, auth_token)
#     call = client.calls.create(
#                 record=True,
#                 # url='http://demo.twilio.com/docs/voice.xml',
#                 twiml=twiml,               
                
                
#                 # to='+18052901594',
#                 to='+995597570605',
                
                
#                 from_='+18052901594'
#                 # from_='+995597570605'
#             )
#     print(call.sid)
#     return {
#         "sid": call.sid,
#     }
def make_call(req: Request, res: Response):
    """Description"""
    account_sid = "AC3a1cd89b4f2908071affc1f56f23b2d5"
    auth_token = "6c176f0f6495f82fa6b7ed06eb1c64ae"
    
    # Generate the TwiML for connecting to a virtual agent
    response = VoiceResponse()
    connect = Connect(action='https://l3agi.ngrok.dev/twilio/twiml')
    connect.virtual_agent(
        connector_name='connector-friendly-name-giga', 
        status_callback='https://l3agi.ngrok.dev/twilio/voice/connector/cx'
    )
    response.append(connect)
    twiml = str(response)  # Convert the VoiceResponse object to a string

    client = Client(account_sid, auth_token)
    call = client.calls.create(
        twiml=twiml,
        to='+995597570605',
        from_='+18052901594'
    )
    print(call.sid)
    return {
        "sid": call.sid,
    }
    
@router.post("/voice/webhook", status_code=200)
def webhook_voice(req: Request, res: Response):
    """Make call"""

    return {
        "true": True,
    }
    
@router.post("/webhook/fails", status_code=200)
def webhook_fails(req: Request, res: Response):
    """Make call"""

    return {
        "true": True,
    }
    
@router.post("/voice/call-status-change", status_code=201)
def voice_call_status_change(req: Request, res: Response):
    """Make call"""

    return {
        "true": True,
    }

class RecordData(BaseModel):
    RecordingUrl: str
    RecordingSid: str
    RecordingDuration: str
    

@router.post("/voice/record")
async def record(request: Request):
    form_data = await request.form()
    record_data = RecordData(**form_data)
    print(record_data.RecordingUrl)  # Access the recording URL
    print(record_data.RecordingSid)  # Access the recording SID
    print(record_data.RecordingDuration)  # Access the recording duration
    # Process the data as needed
    return {"status": "success"}

@router.get("/twiml")
async def record(request: Request):
    print(request)
    
    say =f"""<Say>Ahoy there, are you here Giga!</Say>"""
    # play = f"""<Play oop="0>https://l3agi.ngrok.dev/twilio/audio-proxy/cowbell.mp3</Play>"""
    # play = f"""<Play loop="10">https://api.twilio.com/cowbell.mp3</Play>"""
    # play = f"""<Play loop="1">https://l3agi.ngrok.dev/twilio/audio-proxy/cowbell.mp3</Play>"""
    
    connect=f"""<Connect>
                    <VirtualAgent connectorName="connector-friendly-name-giga" statusCallback="https://l3agi.ngrok.dev/twilio/voice/connector/cx">
                        <Parameter name="customer_name" value="Burton Guster"/>
                    </VirtualAgent>                    
                </Connect>"""
                    
    record_url = "https://l3agi.ngrok.dev/twilio/voice/record"
    record = f"""<Record timeout="30" transcribe="true" recordingStatusCallback="{record_url}"/>"""
                    
                    
    start = f"""<Start>
                    <Stream url="{socket_url}" />
                </Start>"""
    twiml=f"""
    <Response>
        {say}
    </Response>
    """
    return twiml


@router.post("/voice/dialog")
async def record(request: Request):
    print(request)
    # form_data = await request.form()
    # record_data = RecordData(**form_data)
    # print(record_data.RecordingUrl)  # Access the recording URL
    # print(record_data.RecordingSid)  # Access the recording SID
    # print(record_data.RecordingDuration)  # Access the recording duration
    # Process the data as needed
    return {"status": "success"}

@router.get("/voice/cx")
async def record(request: Request):
    print(request)
    # form_data = await request.form()
    # record_data = RecordData(**form_data)
    # print(record_data.RecordingUrl)  # Access the recording URL
    # print(record_data.RecordingSid)  # Access the recording SID
    # print(record_data.RecordingDuration)  # Access the recording duration
    # Process the data as needed
    return {"status": "success"}

@router.get("/voice/connector/cx")
async def record(request: Request):
    print(request, 'get')

    return {"status": "success"}

@router.post("/voice/connector/cx")
async def record(request: Request):
    print(request, 'post')

    return {"status": "success"}




# def transcribe_audio_with_deepgram(audio_data):
#     url = "https://api.deepgram.com/v1/listen"
#     headers = {
#         "Authorization": "2233b7497c00e286e3d3ff507b7ef47905f929bd",
#     }
#     response = requests.post(url, headers=headers, data=audio_data)
#     transcript = response.json()["results"]["channels"][0]["alternatives"][0]["transcript"]
#     print("Transcript: ", transcript)

# async def transcribe_audio_with_deepgram(audio_data):
#     uri = "wss://api.deepgram.com/v1/listen?access_token=f356d66c50f1943171c4a893e2047deefc089a59"
#     async with websockets.connect(uri) as websocket:
#         await websocket.send(audio_data)
#         while True:
#             response = await websocket.recv()
#             transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
#             print("Transcript: ", transcript)
            

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
        
        # print(data['event'])
        # print(data)
        

        if data['event'] == "connected":
            logging.info("Connected Message received: {}".format(message))
        if data['event'] == "start":
            logging.info("Start Message received: {}".format(message))
        if data['event'] == "media":
            if not has_seen_media:
                logging.info("Media message: {}".format(message))
                payload = data['media']['payload']
                logging.info("Payload is: {}".format(payload))
                audio_data = base64.b64decode(payload)
                logging.info("That's {} bytes".format(len(audio_data)))
                # asyncio.create_task(transcribe_audio_with_deepgram(audio_data))
                has_seen_media = True
        if data['event'] == "stop":
            logging.info("Stop Message received: {}".format(message))
            break
        message_count += 1
        



# @router.post("/speech-to-text", status_code=201)
# def text_to_speech():
#     """Text to speech"""

#     url = "https://play.ht/api/v2/tts/stream"

#     payload = {
#         "text": "Hello Giga, How are you, I want ti introduce our products, which one would you like?",
#         "voice": "larry",
#         "quality": "draft",
#         "output_format": "mp3",
#         "speed": 1,
#         "sample_rate": 24000
#     }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "AUTHORIZATION": "Bearer 56b08c59cc2e44c5bbdb2e6b9ac7b038",
#         "X-USER-ID": "NF9Psaqy2cOKRDqrUVs2bYnELWW2"
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     response_json = json.loads(response.text)
    
#     url = response_json["href"]

#     #Get Audio
#     payload = {}
#     headers = {
#     'Authorization': 'Bearer 56b08c59cc2e44c5bbdb2e6b9ac7b038',
#     'X-USER-ID': 'NF9Psaqy2cOKRDqrUVs2bYnELWW2'
#     }

#     response = requests.request("GET", url, headers=headers, data=payload)

#     return response

@router.post("/text-to-speech", status_code=201)
def text_to_speech():
    """Text to speech"""
    text =   "Hello Leeroy! How's everything going for you today? I'm thrilled to introduce you to our range of premium products. Whether you're interested in iPhones, MacBooks, AirPods, or something else from our collection, we have it all. Just let me know your preference, and I'll be delighted to assist you further!"
    url = "https://play.ht/api/v2/tts/stream"

    payload = {
        "text": text,
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

    return response_json['href']

@router.get("/audio-proxy/cowbell.mp3")
# async def audio_proxy():
#     data = text_to_speech("Hello Giga, How are you, I want ti introduce our products, which one would you like?")
#     play_ht_url = data['href']
    
#     headers = {
#         "AUTHORIZATION": "Bearer 56b08c59cc2e44c5bbdb2e6b9ac7b038",
#         "X-USER-ID": "NF9Psaqy2cOKRDqrUVs2bYnELWW2"
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(play_ht_url, headers=headers)
    
#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail="Unable to fetch audio.")
    
#     async def content_generator():
#         async for chunk in response.aiter_bytes():
#             yield chunk

#     return StreamingResponse(content_generator(), media_type="audio/mpeg")
async def audio_proxy():
    # text = "Hello Leeroy! How are you today? We have a fantastic range of products including iPhones, MacBooks, and AirPods. What catches your eye?"
    text = "Hello Leeroy! How's everything going for you today? I'm thrilled to introduce you to our range of premium products. Whether you're interested in iPhones, MacBooks, AirPods, or something else from our collection, we have it all. Just let me know your preference, and I'll be delighted to assist you further!"
    url = "https://play.ht/api/v2/tts/stream"
    headers = {
        "AUTHORIZATION": "Bearer 56b08c59cc2e44c5bbdb2e6b9ac7b038",
        "X-USER-ID": "NF9Psaqy2cOKRDqrUVs2bYnELWW2",
        "accept": "*/*",
        "content-type": "application/json"
    }
    payload = {
        "text": text,
        "voice": "larry",
        "quality": "draft",
        "output_format": "mp3",
        "speed": 1,
        "sample_rate": 24000,
        "voice_engine": "PlayHT1.0"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Unable to fetch audio.")

    async def content_generator():
        async for chunk in response.aiter_bytes():
            yield chunk

    return StreamingResponse(content_generator(), media_type="audio/mpeg")



@router.get("/fetch_audio/")
def fetch_audio():
    TTS_URL = text_to_speech()

    # The credentials or headers you need for the TTS service
    HEADERS = {
        "AUTHORIZATION": "Bearer 56b08c59cc2e44c5bbdb2e6b9ac7b038",
        "X-USER-ID": "NF9Psaqy2cOKRDqrUVs2bYnELWW2",
    }


    response = requests.get(TTS_URL, headers=HEADERS)
    
    # Ensure you have error handling here for failed requests
    
    return response.content