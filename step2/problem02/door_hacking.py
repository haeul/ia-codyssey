import os

# Caesar 복호화 함수
def caesar_cipher_decode(target_text):
    keywords = ['mars', 'emergency', 'base', 'mission', 'oxygen']  # 보너스 과제용 키워드
    found = False

    for shift in range(1, 26):  # 1~25까지 시도
        decoded = ''

        for char in target_text:
            if 'a' <= char <= 'z':
                decoded += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                decoded += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decoded += char

        print(f'[{shift}] {decoded}')

        # 보너스 과제: 키워드 자동 탐지
        lower_decoded = decoded.lower()
        for keyword in keywords:
            if keyword in lower_decoded:
                print(f'\n[✓] 키워드 "{keyword}" 발견됨. 추천 shift: {shift}\n')
                found = True
                break

        if found:
            break


# password.txt 파일에서 문자열을 읽는다
def read_password():
    try:
        with open('password.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print('[-] password.txt 파일이 존재하지 않습니다.')
        return None
    except Exception as e:
        print(f'[-] 파일 읽기 오류: {e}')
        return None


# result.txt 파일로 저장
def save_result(result_text):
    try:
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write(result_text)
        print('[✓] result.txt 파일로 저장 완료.')
    except Exception as e:
        print(f'[-] 저장 실패: {e}')


# 메인 실행부
def main():
    password = read_password()
    if not password:
        return

    print('\n[*] 카이사르 복호화 결과:')
    caesar_cipher_decode(password)

    try:
        choice = input('\n[?] 올바르게 해독된 shift 번호를 입력하세요 (없으면 Enter): ')
        if choice.isdigit():
            shift = int(choice)
            result = ''

            for char in password:
                if 'a' <= char <= 'z':
                    result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                elif 'A' <= char <= 'Z':
                    result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                else:
                    result += char

            print(f'\n[✓] 최종 해독 결과: {result}')
            save_result(result)
        else:
            print('[!] 저장 없이 종료합니다.')

    except Exception as e:
        print(f'[-] 입력 오류: {e}')


if __name__ == '__main__':
    main()
