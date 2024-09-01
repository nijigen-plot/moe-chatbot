import pyaudio
import time
import wave

CHUNK = 4096
CHANNELS = 1  # モノラル
FRAME_RATE = 44100

# カード番号
CARD_NUM = 0 # PyAudioのget_device_count()のIndex番号を指定。


class Audio:
    wav_file = None
    stream = None

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        for x in range(0, self.audio.get_device_count()):
            print(self.audio.get_device_info_by_index(x))

    # コールバック関数
    def callback(self, in_data, frame_count, time_info, status):
        # wavに保存する
        self.wav_file.writeframes(in_data)
        return None, pyaudio.paContinue

    # 録音開始
    def start_record(self):

        # wavファイルを開く
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

        # ストリームを止める
        self.stream.stop_stream()
        self.stream.close()

        # wavファイルを閉じる
        self.wav_file.close()

    # インスタンスの破棄
    def destructor(self):

        # pyaudioインスタンスを破棄する
        self.audio.terminate()


if __name__ == '__main__':
    audio = Audio()
    audio.start_record()
    time.sleep(5)   # 5秒間待つ
    audio.stop_record()
    audio.destructor()
