import random
from datetime import datetime


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        '''환경 정보를 무작위로 설정'''
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2) # random.uniform(a, b) : a와 b 사이의 실수를 무작위로 생성
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2) # round(..., 2) : 소수점 둘째자리까지 반올림림
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        '''환경 정보 반환 및 사람이 읽기 쉬운 로그 파일에 저장'''
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # strftime : 날짜와 시간을 원하는 형식의 문자열로 바꿔줌

        try:
            with open('mars_env_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(
                    f'[{now}] '
                    f'내부 온도: {self.env_values["mars_base_internal_temperature"]}℃ | '
                    f'외부 온도: {self.env_values["mars_base_external_temperature"]}℃ | '
                    f'내부 습도: {self.env_values["mars_base_internal_humidity"]}% | '
                    f'외부 광량: {self.env_values["mars_base_external_illuminance"]} W/m² | '
                    f'CO₂: {self.env_values["mars_base_internal_co2"]}% | '
                    f'산소: {self.env_values["mars_base_internal_oxygen"]}%\n'
                )
        except Exception as e:
            print(f'로그 파일 저장 오류: {e}')

        return self.env_values


# 실행 예시
if __name__ == '__main__':
    ds = DummySensor()         # 인스턴스 생성
    ds.set_env()               # 랜덤 환경 설정
    env = ds.get_env()         # 정보 반환 및 로그 저장

    print('현재 환경 정보:')
    for key, value in env.items():
        print(f'{key}: {value}')
