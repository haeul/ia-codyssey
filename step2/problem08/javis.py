import os
import wave
import pyaudio
import datetime
import csv
import speech_recognition as sr


class Javis:
    def __init__(self, duration=5, sample_rate=44100, channels=1, chunk=1024):
        self.duration = duration
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk = chunk
        self.format = pyaudio.paInt16
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
        '''보너스: 지정한 날짜 범위에 포함된 파일 목록 출력'''
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

    def transcribe_audio_files(self):
        '''STT: 녹음된 음성 파일을 텍스트로 변환하여 CSV 저장'''
        recognizer = sr.Recognizer()

        for filename in os.listdir(self.folder):
            if filename.endswith('.wav'):
                wav_path = os.path.join(self.folder, filename)
                csv_name = filename.replace('.wav', '.csv')
                csv_path = os.path.join(self.folder, csv_name)

                print(f'[+] STT 변환 중: {filename}')

                try:
                    with sr.AudioFile(wav_path) as source:
                        audio = recognizer.record(source)

                    text = recognizer.recognize_google(audio, language='ko-KR')

                    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Time', 'Text'])
                        writer.writerow(['00:00:00', text])

                    print(f'[✓] 변환 성공: {csv_name}')

                except sr.UnknownValueError:
                    print(f'[-] 인식 실패 (알 수 없음): {filename}')
                except sr.RequestError:
                    print(f'[-] STT 서버 연결 실패: {filename}')
                except Exception as e:
                    print(f'[-] 기타 오류 발생: {e}')

    def search_keyword_in_csv(self, keyword):
        '''보너스: 모든 CSV 파일에서 키워드 검색'''
        found = False
        for filename in os.listdir(self.folder):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.folder, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # 헤더 스킵

                    for row in reader:
                        if keyword in row[1]:
                            print(f'[✓] {filename} @ {row[0]}: {row[1]}')
                            found = True

        if not found:
            print('[!] 일치하는 결과가 없습니다.')


if __name__ == '__main__':
    javis = Javis(duration=5)

    while True:
        print('\n=== JARVIS MENU ===')
        print('1. 음성 녹음')
        print('2. 날짜 범위로 파일 보기')
        print('3. 음성 STT 변환 및 CSV 저장')
        print('4. 키워드로 CSV 검색')
        print('0. 종료')
        choice = input('선택 >> ')

        if choice == '1':
            javis.record_audio()
        elif choice == '2':
            s = input('시작 날짜 (YYYYMMDD): ')
            e = input('종료 날짜 (YYYYMMDD): ')
            javis.list_files_by_date_range(s, e)
        elif choice == '3':
            javis.transcribe_audio_files()
        elif choice == '4':
            k = input('검색 키워드: ')
            javis.search_keyword_in_csv(k)
        elif choice == '0':
            print('종료합니다.')
            break
        else:
            print('[!] 올바른 번호를 선택하세요.')
