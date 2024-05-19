import pyaudio
import time
import wave

CHUNK = 4096
CHANNELS = 1
FRAME_RATE = 44100
CARD_NUM = 2

class AudioRecorder:
    
	def __init__(self):
        self.audio = pyaudio.PyAudio()
		wav_file = None
		stream = None


    # コールバック関数
    def callback(self, in_data, frame_count, time_info, status):
        # wavに保存する
        self.wav_file.writeframes(in_data)
        return None, pyaudio.paContinue

    # 録音開始
    def start_record(self):

        # wavファイルを開く
		print("Start a Record.")
        self.wav_file = wave.open('record.wav', 'w')
        self.wav_file.setnchannels(CHANNELS)
        self.wav_file.setsampwidth(2)  # 16bits
        self.wav_file.setframerate(FRAME_RATE)

        # ストリームを開始
        self.stream = self.audio.open(format=self.audio.get_format_from_width(self.wav_file.getsampwidth()),
                                      channels=self.wav_file.getnchannels(),
                                      rate=self.wav_file.getframerate(),
                                      input_device_index=CARD_NUM,
                                      input=True,
                                      output=False,
                                      frames_per_buffer=CHUNK,
                                      stream_callback=self.callback)

    # 録音停止
    def stop_record(self):
		
		print("Stop a Record.")
        # ストリームを止める
        self.stream.stop_stream()
        self.stream.close()

        # wavファイルを閉じる
        self.wav_file.close()

    # インスタンスの破棄
    def destructor(self):

        # pyaudioインスタンスを破棄する
        self.audio.terminate()


	# 録音を行って、結果のwavファイルを返す
	def record_for(self, duration=5, output_filename='record.wav'):
		self.start_record()
		time.sleep(duration)
		self.stop_record()
		self.destructor()
		return output_filename

