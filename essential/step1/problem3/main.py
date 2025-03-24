import os
import sys
import pickle


class MarsInventoryManager:
    def __init__(self, base_dir):
        self.csv_file = os.path.join(base_dir, 'Mars_Base_Inventory_List.csv')
        self.danger_file = os.path.join(base_dir, 'Mars_Base_Inventory_danger.csv')
        self.binary_file = os.path.join(base_dir, 'Mars_Base_Inventory_List.bin')
        self.inventory = []

    def read_csv(self):
        '''1. CSV 파일의 원본 내용을 읽어 출력'''
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                print('\n--- CSV 파일 원본 내용 ---')
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print(f'Error: {self.csv_file} 파일이 존재하지 않습니다.')
            sys.exit(1)
        except Exception as e:
            print(f'CSV 읽기 오류 발생: {e}')
            sys.exit(1)

    def parse_csv_to_list(self):
        '''2. CSV 내용을 Python 리스트로 변환'''
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines[1:]:
                    parts = line.strip().split(',')
                    if len(parts) != 5:
                        continue
                    self.inventory.append(parts)
        except Exception as e:
            print(f'CSV 파싱 오류: {e}')
            sys.exit(1)

    def sort_by_flammability(self):
        '''3. 인화성이 높은 순으로 정렬'''
        try:
            self.inventory.sort(key=lambda x: float(x[4]), reverse=True)
        except Exception as e:
            print(f'정렬 오류: {e}')
            sys.exit(1)

    def print_dangerous_items(self):
        '''4. 인화성 ≥ 0.7 항목만 출력'''
        print('\n--- 위험 물질 목록 (인화성 ≥ 0.7) ---')
        for item in self.inventory:
            try:
                if float(item[4]) >= 0.7:
                    print(f'물질명: {item[0]}, 인화성 지수: {item[4]}')
            except ValueError:
                continue

    def save_dangerous_items_to_csv(self):
        '''5. 위험 항목을 별도 CSV로 저장'''
        try:
            with open(self.danger_file, 'w', encoding='utf-8') as file:
                file.write('Substance,Weight,Specific Gravity,Strength,Flammability\n')
                for item in self.inventory:
                    try:
                        if float(item[4]) >= 0.7:
                            file.write(','.join(item) + '\n')
                    except ValueError:
                        continue
        except Exception as e:
            print(f'CSV 저장 오류: {e}')

    def save_inventory_to_binary(self):
        '''6. 정렬된 전체 목록을 이진 파일로 저장'''
        try:
            with open(self.binary_file, 'wb') as file:
                pickle.dump(self.inventory, file)
        except Exception as e:
            print(f'이진 저장 오류: {e}')

    def load_and_print_from_binary(self):
        '''7. 이진 파일에서 읽어와 출력'''
        try:
            with open(self.binary_file, 'rb') as file:
                data = pickle.load(file)
                print('\n--- 이진 파일에서 불러온 정렬된 목록 ---')
                for item in data:
                    print(f'물질명: {item[0]}, 인화성 지수: {item[4]}')
        except Exception as e:
            print(f'이진 파일 읽기 오류: {e}')

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    manager = MarsInventoryManager(base_dir)

    manager.read_csv()               
    manager.parse_csv_to_list()                
    manager.sort_by_flammability()             
    manager.print_dangerous_items()            
    manager.save_dangerous_items_to_csv()      
    manager.save_inventory_to_binary()         
    manager.load_and_print_from_binary()       


if __name__ == '__main__':
    main()
