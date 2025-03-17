import os
import sys

# 로그 파일 경로
LOG_FILE = 'mission_computer_main.log'
PROBLEM_LOG_FILE = 'problem_logs.log'
REPORT_FILE = 'log_analysis.md'

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

def analyze_logs(logs):
    '''로그 내용을 시간 역순으로 정렬 및 분석'''
    sorted_logs = sorted(logs, reverse=True)  # 시간 역순 정렬
    save_problem_logs(sorted_logs)  # 문제 로그 저장
    return sorted_logs

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

def write_report(problem_logs):
    '''로그 분석 결과를 Markdown 보고서로 저장'''
    with open(REPORT_FILE, 'w', encoding='utf-8') as file:
        file.write('# 사고 원인 분석 보고서\n\n')
        file.write('## 문제 로그\n\n')
        file.write('```log\n')
        file.writelines(problem_logs)
        file.write('```\n\n')
        file.write('## 분석 결과\n\n')
        file.write('사고의 원인은 로그에서 발견된 오류와 관련이 있습니다. 분석 결과:\n\n')
        for log in problem_logs:
            file.write(f'- {log}')

def main():
    check_python_installation()
    logs = read_log_file(LOG_FILE)
    sorted_logs = analyze_logs(logs)
    problem_logs = save_problem_logs(sorted_logs)
    write_report(problem_logs)
    for log in sorted_logs:
        print(log.strip())  # 로그 출력

if __name__ == '__main__':
    main()
