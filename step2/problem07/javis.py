import os
import wave
import pyaudio
import datetime


class Recorder:
    def __init__(self, duration=5, sample_rate=44100, channels=1, chunk=1024):
        self.duration = duration
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk = chunk
        self.format = pyaudio.paInt16

        # 저장 폴더 생성
        self.folder = os.path.join(os.path.dirname(__file__), 'records')
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def record_audio(self):
        '''마이크를 통해 오디오 녹음하고 저장'''
        audio = pyaudio.PyAudio()

        try:
            stream = audio.open(format=self.format,
                                channels=self.channels,
                                rate=self.sample_rate,
                                input=True,
                                frames_per_buffer=self.chunk)

            print('[*] 녹음 시작...')
            frames = []

            for _ in range(0, int(self.sample_rate / self.chunk * self.duration)):
                data = stream.read(self.chunk)
                frames.append(data)

            print('[*] 녹음 종료')

            stream.stop_stream()
            stream.close()
            audio.terminate()

            filename = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.wav'
            filepath = os.path.join(self.folder, filename)

            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))

            print(f'[✓] 저장 완료: {filename}')

        except Exception as e:
            print(f'[-] 오류 발생: {str(e)}')

    def list_files_by_date_range(self, start_date, end_date):
        '''
        보너스: 지정한 날짜 범위에 포함된 파일들을 출력
        날짜 형식: 'YYYYMMDD'
        '''
        try:
            start = datetime.datetime.strptime(start_date, '%Y%m%d')
            end = datetime.datetime.strptime(end_date, '%Y%m%d')

            print(f'[*] {start_date} ~ {end_date} 녹음 파일 목록:\n')

            for filename in os.listdir(self.folder):
                if filename.endswith('.wav'):
                    try:
                        file_date = datetime.datetime.strptime(filename[:8], '%Y%m%d')
                        if start <= file_date <= end:
                            print('  -', filename)
                    except ValueError:
                        continue

        except Exception as e:
            print(f'[-] 날짜 형식 오류 또는 처리 중 오류 발생: {str(e)}')


if __name__ == '__main__':
    rec = Recorder(duration=5)  # 5초 녹음
    rec.record_audio()

    # ↓ 날짜 범위 확인 예시 (주석 해제 후 사용)
    # rec.list_files_by_date_range('20240601', '20240630')
