
from io import BytesIO
import os
import requests
from dotenv import load_dotenv
from app.tools import utilities
import ast
import time

def _audio_complete_callback(url, headers):
        lapsed_time = 0
        resp = requests.get(url, headers=headers)
        status = ast.literal_eval(resp.content.decode())["data"]["attributes"]["status"]
      
        while(status != 'done'):
            resp = requests.get(url, headers=headers)
            status = ast.literal_eval(resp.content.decode())["data"]["attributes"]["status"]
            print("resp: ", resp.content)
            time.sleep(3)
            lapsed_time += 3
            if lapsed_time > 30:
                raise Exception("Timeout Error") 

        return resp

def _curl_from_cdn(url):
        response = requests.get(url)
        audio = BytesIO(response.content)
        
        return audio

def _write_file(url):  
    data = _curl_from_cdn(url)
    tts_path = os.path.join(utilities.get_root_path(), 'temp', 'tts_audio.mp3')
    
    # Save the raw data to a temporary file
    with open(tts_path, 'wb') as temp_file:
        temp_file.write(data.getvalue())
    
    return tts_path

def generate_tts(text, voice):
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path, override=True)
    shotstack_api_key = os.getenv('SHOTSTACK_KEY')
    print("sstck api kesy: ", shotstack_api_key, "\n", os.getenv('ENVIRONMENT'))

    if voice == 'Joey' or voice == 'Kendra':
         language = 'en-US'
    if voice == 'Arthur' or voice == 'Amy':
         language = 'en-GB'
    if voice == 'Pedro':
         language = 'es-US'
    # Audio request url and headers
    req_url = "https://api.shotstack.io/create/stage/assets/"
    audio_headers = {'content-type': 'application/json',
                    'x-api-key': f'{shotstack_api_key}'
                    }
    audio_data = {
        "provider": "shotstack",
        "options": {
            "type": "text-to-speech",
            "text": f'''{text}''',
            "voice": f'{voice}',
            "language": f'{language}'
        },       
    }

    
    # Get audio cdn link from post to shotstack API
    resp = requests.post(req_url, json=audio_data, headers=audio_headers)
    print("resp: ", resp.content)
    if resp.status_code >= 200 and resp.status_code < 300:
        # Print the response content (usually in JSON format)
        audio_id = str(ast.literal_eval(resp.text)["data"]["id"])
        audio_url = req_url + audio_id
    else:
        print(f"Error generating tts audio: {resp.status_code}")

    
    resp = _audio_complete_callback(audio_url, audio_headers)
    audio_cdn_link = ast.literal_eval(resp.content.decode())["data"]["attributes"]["url"]

    outfile = _write_file(audio_cdn_link)

    return outfile

# if __name__ == '__main__':
#     path = generate_tts('This is a test', "Matthew")
#     print(path)