import base64
import json
import logging
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

HTTP_SERVER_PORT = 5000

@app.websocket("/media")
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=HTTP_SERVER_PORT)