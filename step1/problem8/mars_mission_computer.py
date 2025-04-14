import random
import time
import json
import platform
import os
import psutil


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
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        return self.env_values.copy()


class MissionComputer:
    def __init__(self, sensor):
        self.sensor = sensor
        self.env_values = {}
        self.history = []
        self.setting = self.load_settings()

    def load_settings(self):
        '''setting.txt에서 출력 설정을 읽어옴'''
        setting_path = 'setting.txt'
        settings = {
            'os': True,
            'os_version': True,
            'cpu_type': True,
            'cpu_cores': True,
            'memory_total_mb': True
        }
        try:
            if os.path.exists(setting_path):
                with open(setting_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=')
                            if key in settings:
                                settings[key] = value.lower() == 'true'
        except Exception as e:
            print(f'[경고] setting.txt 로딩 중 오류 발생: {e}')
        return settings

    def get_sensor_data(self):
        self.sensor.set_env()
        self.env_values = self.sensor.get_env()
        print('[실시간 환경 정보]')
        print(json.dumps(self.env_values, indent=4), '\n')

    def get_mission_computer_info(self):
        try:
            raw_info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': os.cpu_count(),
                'memory_total_mb': round(psutil.virtual_memory().total / (1024 * 1024), 2)
            }

            filtered_info = {
                key: value for key, value in raw_info.items() if self.setting.get(key, True)
            }

            print('[미션 컴퓨터 시스템 정보]')
            print(json.dumps(filtered_info, indent=4), '\n')

        except Exception as e:
            print(f'[에러] 시스템 정보 수집 실패: {e}')

    def get_mission_computer_load(self):
        try:
            load = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent
            }
            print('[미션 컴퓨터 실시간 부하]')
            print(json.dumps(load, indent=4), '\n')
        except Exception as e:
            print(f'[에러] 시스템 부하 수집 실패: {e}')


if __name__ == '__main__':
    ds = DummySensor()
    runComputer = MissionComputer(ds)

    runComputer.get_sensor_data()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
