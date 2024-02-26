import whisper_timestamped as whisperts
from whisper_timestamped.make_subtitles import write_srt
if __name__ == '__main__':
    
    audio = whisperts.load_audio("python\Callum.mp3")
    model = whisperts.load_model("tiny", device="cpu")

    result = whisperts.transcribe(model, audio, language="en")
    words = result['segments'][0]['words']

    with open('whisper_out.srt', 'w') as file:
    # Your print statement here
    
        write_srt(words, file)
    # import json
    # print(json.dumps(result, indent = 2, ensure_ascii = False))
    # print(result['segments'][0]['words'])