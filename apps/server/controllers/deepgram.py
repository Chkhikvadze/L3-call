 # Example filename: deepgram_test.py

from deepgram import Deepgram
import asyncio
import aiohttp


# Your Deepgram API Key
DEEPGRAM_API_KEY = 'f356d66c50f1943171c4a893e2047deefc089a59'

# URL for the realtime streaming audio you would like to transcribe
URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_world_service'

async def main():
  # Initialize the Deepgram SDK
  deepgram = Deepgram(DEEPGRAM_API_KEY)

  # Create a websocket connection to Deepgram
  # In this example, punctuation is turned on, interim results are turned off, and language is set to UK English.
  try:
    deepgramLive = await deepgram.transcription.live({
      'smart_format': True,
      'interim_results': False,
      'language': 'en-US',
      'model': 'nova',
    })
  except Exception as e:
    print(f'Could not open socket: {e}')
    return

  # Listen for the connection to close
  deepgramLive.registerHandler(deepgramLive.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))

  # Listen for any transcripts received from Deepgram and write them to the console
  deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, print)

  # Listen for the connection to open and send streaming audio from the URL to Deepgram
  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as audio:
      while True:
        data = await audio.content.readany()
        deepgramLive.send(data)

        # If no data is being sent from the live stream, then break out of the loop.
        if not data:
            break

  # Indicate that we've finished sending data by sending the customary zero-byte message to the Deepgram streaming endpoint, and wait until we get back the final summary metadata object
  await deepgramLive.finish()



def analyze_with_openai(text):
    # Step 3: Text Analysis with OpenAI
    # This is just a dummy example; you can replace it with your actual logic.
    response = openai.Completion.create(prompt=text, max_tokens=100)
    return response.choices[0].text.strip()



# async def handle_transcript(transcript):
#     # Step 2: Sentence Detection
#     text = transcript.get("text", "")
#     if text.endswith(('.', '!', '?')):  # Simple check for sentence ending
#         response = analyze_with_openai(text)
        
#         # Convert the response to audio
#         audio_response = text_to_speech(response)
        
#         # Send audio back via Twilio
#         send_audio_to_twilio(audio_response)
        

# Define a handler for transcripts
def handle_transcript(transcript):
    # Process the transcript here. For example, you could analyze the transcript and generate a response.
    print(transcript)

async def transcribe_audio_with_deepgram(audio_data):
    # Initialize the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)

    # Create a websocket connection to Deepgram
    try:
        deepgramLive = await deepgram.transcription.live({
            'smart_format': True,
            'interim_results': True,  # Enable interim results
            'language': 'en-US',
            'model': 'nova',
        })
    except Exception as e:
        print(f'Could not open socket: {e}')
        return

    # Listen for the connection to close
    deepgramLive.registerHandler(deepgramLive.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))

    # Listen for any transcripts received from Deepgram and process them
    deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, handle_transcript)

    print(f"Sending audio data to Deepgram: {audio_data}")
    # Send the audio data to Deepgram
    deepgramLive.send(audio_data)

    # Indicate that we've finished sending data by sending the customary zero-byte message to the Deepgram streaming endpoint, and wait until we get back the final summary metadata object
    await deepgramLive.finish()