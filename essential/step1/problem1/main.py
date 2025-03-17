import os
import sys

# 현재 스크립트가 위치한 디렉토리를 기준으로 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일이 위치한 폴더
LOG_FILE = os.path.join(BASE_DIR, 'mission_computer_main.log')
PROBLEM_LOG_FILE = os.path.join(BASE_DIR, 'problem_logs.log')
REPORT_FILE = os.path.join(BASE_DIR, 'log_analysis.md')

def check_python_installation():
    '''Python 실행 확인'''
    print('Hello Mars')

def read_log_file(filename):
    '''로그 파일을 읽어 출력 (예외 처리 포함)'''
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            logs = file.readlines()
        return logs
    except FileNotFoundError:
        print(f'Error: {filename} 파일을 찾을 수 없습니다.')
        sys.exit(1)
    except Exception as e:
        print(f'파일 읽기 오류 발생: {e}')
        sys.exit(1)

def sort_reverse(logs):
    '''로그 내용을 시간 역순으로 정렬'''
    return sorted(logs, reverse=True)

def save_problem_logs(logs):
    ''''Mission completed' 이전 로그 저장 중단'''
    problem_logs = []
    for log in logs:
        if 'Mission completed' in log:
            break  # 'Mission completed'가 포함된 로그가 나오면 저장 중단
        problem_logs.append(log)
    
    with open(PROBLEM_LOG_FILE, 'w', encoding='utf-8') as file:
        file.writelines(problem_logs)
        
    return problem_logs

def write_report(logs, problem_logs):
    '''로그 분석 결과를 Markdown 보고서로 저장'''
    with open(REPORT_FILE, 'w', encoding='utf-8') as file:
        file.write('# 사고 원인 분석 보고서\n\n')
        file.write('## 전체 로그\n\n')
        file.write('```log\n')
        file.writelines(logs)
        file.write('```\n\n')
        file.write('## 분석 결과\n\n')
        file.write('Mission completed 출력 이후를 사고 원인으로 간주.\n\n')
        file.write('사고 원인 로그:\n')
        for log in problem_logs:
            file.write(f'- {log}')


check_python_installation()
logs = read_log_file(LOG_FILE)
sorted_logs = sort_reverse(logs)
problem_logs = save_problem_logs(sorted_logs)
write_report(logs, problem_logs)
for log in logs:
    print(log.strip())  # 로그 출력
for log in sorted_logs:
    print(log.strip())  # 로그 역순 출력

