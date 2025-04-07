import random
import time
import json
import msvcrt  # Windows에서 키보드 입력 감지용 모듈

# -----------------------------
# DummySensor 클래스 정의
# -----------------------------
class DummySensor:
    def __init__(self):
        # 센서가 측정할 환경값들을 딕셔너리 형태로 초기화
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
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        '''현재 설정된 환경 값을 반환'''
        return self.env_values.copy()  # 외부에서 값 변경 못 하도록 복사본 반환


# -----------------------------
# MissionComputer 클래스 정의
# -----------------------------
class MissionComputer:
    def __init__(self, sensor):
        self.sensor = sensor  # DummySensor 인스턴스를 주입받음
        self.env_values = {}  # 현재 환경값 저장용
        self.history = []     # 5분 평균 계산을 위한 누적값 리스트

    def get_sensor_data(self):
        '''센서 데이터 반복 수집 및 출력'''
        print('실행 중입니다. 종료하려면 Enter 키를 누르세요.\n')

        while True:
            # 센서 값 갱신 및 가져오기
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()
            self.history.append(self.env_values)

            # JSON 형식으로 출력
            print('[실시간 환경 정보]')
            print(json.dumps(self.env_values, indent=4), '\n')

            # 5분마다 평균 출력 (5초 x 60 = 300초)
            if len(self.history) >= 60:
                self.print_average()
                self.history.clear()

            # 5초 동안 사용자 키 입력 체크
            print('5초 대기 중... 종료하려면 Enter를 누르세요.')
            if self.check_user_input():
                print('System stopped...')
                break

            # 다음 측정을 위해 5초 대기
            time.sleep(5)

    def print_average(self):
        '''5분 평균값 출력'''
        if not self.history:
            return

        print('[5분 평균 환경 정보]')
        avg_values = {}
        count = len(self.history)

        # 각 항목 평균 계산
        for key in self.env_values:
            total = sum(item[key] for item in self.history)
            avg_values[key] = round(total / count, 3)

        print(json.dumps(avg_values, indent=4), '\n')

    def check_user_input(self):
        '''5초 안에 엔터 키가 눌렸는지 확인 (Windows 전용)'''
        start = time.time()
        while time.time() - start < 5:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\r':  # 엔터 키
                    return True
            time.sleep(0.1)
        return False


# -----------------------------
# 프로그램 시작 부분
# -----------------------------
if __name__ == '__main__':
    ds = DummySensor()                    # DummySensor 인스턴스 생성
    RunComputer = MissionComputer(ds)     # MissionComputer 인스턴스화

    try:
        RunComputer.get_sensor_data()     # 센서 데이터 수집 루프 실행
    except KeyboardInterrupt:
        print('\nSystem stopped...')
