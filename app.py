import json
import os
import tempfile
import wave
import sys
from io import BytesIO

from scipy.io.wavfile import read, write
import pyaudio
import requests
from dotenv import load_dotenv
from openai import OpenAI
import openai
from record import AudioRecorder


try:
    url_arg = sys.argv[1]
    print(f"URL = {url_arg}")

except:
    raise ValueError("TTS APIアクセスの為のURLを引数にいれてください。")

load_dotenv()
p = pyaudio.PyAudio()
CHUNK = 1024
CARD_NUM = 2 # arecord -l で確認するスピーカーデバイス

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)
recorder = AudioRecorder()

if __name__ == "__main__":
	# 録音開始
	recorded_file = recorder.record_for()

	# whisperでAudio to Text
	with open(recorded_file, "rb") as wavfile:
		input_wav = wavfile.read()
	rate, data = read(BytesIO(input_wav))

	try:
		transcript = client.audio.transcriptions.create(
			model="whisper-1",
			file=data
		)
	except openai.APIStatusError as e:
		raise print(f"openai status error. {e}")

    # OpenAI GPT4oで会話
    chat_completion = client.chat.completions.create(
        messages=[
            {"role":"system", "content": "あなたはゆずソフトのキャラクター「在原 七海」です。七海ちゃんの口調で回答してください。"},
            {"role":"user", "content": f"{transcript.text}"} # ここはあとでマイク入力に変更する
        ],
        model=os.environ.get('OPENAI_API_MODEL')
        )
    answer = chat_completion.choices[0].message.content
    
    # nanami-moe-ttsで七海の声に変換
    payload = {"text" : f"{answer}"}
    headers = {"Content-Type" : "application/json"}
    response = requests.post(f"{url_arg}/run", headers=headers, data=json.dumps(payload))
    if response.ok:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(response.content)
            audio_file_path = tmp_file.name
            print(audio_file_path)
        with wave.open(audio_file_path, 'rb') as wf:
            # Instantiate PyAudio and initialize PortAudio system resources (1)
            p = pyaudio.PyAudio()

            # Open stream (2)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True # output_device_indexは指定せずデフォルトにする
                        )

            # Play samples from the wave file (3)
            while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
                stream.write(data)

            # Close stream (4)
            stream.close()

            # Release PortAudio system resources (5)
            p.terminate()
        
    else:
        print(f"Request Failed with status code {response.status_code}: {response.text}")
