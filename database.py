import csv

# database는 아이템의 이름이 key, 아이템의 개수가 value, 아이템의 위치가 location인 딕셔너리로 구성되어 있다.
class Location:
    def __init__(self, stack, column, shelf):
        self.stack = stack
        self.column = column
        self.shelf = shelf

    def __str__(self):
        return f"(스택 : {self.stack}, 열 : {self.column}, 선반 : {self.shelf})"
    
    def __eq__(self, other):
        return self.stack == other.stack and self.column == other.column and self.shelf == other.shelf

class Database:
    def __init__(self):
        self.data = {}

    def insert(self, key, value, location: Location):
        self.data[key] = {'count': value, 'location': location}

    def get(self, key):
        return self.data.get(key)
    
    def update(self, key, value, location: Location):
        if key in self.data:
            self.data[key]['count'] = value
            self.data[key]['location'] = location

    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def show(self):
        return self.data
    
    def relocate(self, key, location: Location):
        if key in self.data:
            self.data[key]['location'] = location

    @staticmethod
    def parse_location(location_str):
        parts = location_str.replace(" ", "").split(',')
        if len(parts) != 3:
            raise ValueError("형식은 x,y,z 여야 합니다.")
        try:
            stack, column, shelf = map(int, parts)
        except ValueError:
            raise ValueError("모든 값은 정수여야 합니다.")
        return Location(stack, column, shelf)

    @staticmethod
    def insert_item(database):
        key = input("아이템의 이름을 입력하세요: ")
        if not key:
            print("아이템의 이름을 입력하지 않았습니다. 다시 시도해주세요.")
            return
        if database.get(key):
            print("아이템이 이미 존재합니다.")
            item = database.get(key)
            location = item['location']
            print(f"아이템: {key}, 수량: {item['count']}, 위치: {location.stack}, {location.column}, {location.shelf}")
        else:
            value = int(input("아이템의 개수를 입력하세요: "))
            location_str = input("아이템의 위치를 입력하세요 (예: stack, column, shelf): ")
            location = Database.parse_location(location_str)
            database.insert(key, value, location)
            print("아이템이 성공적으로 추가되었습니다.")

    @staticmethod
    def update_item(database):
        try:
            key = input("아이템의 이름을 입력하세요: ")
            if not key:
                raise ValueError("아이템의 이름을 입력하지 않았습니다.")
            if not database.get(key):
                raise ValueError("아이템이 데이터베이스에 존재하지 않습니다.")
            value_str = input("아이템의 개수를 입력하세요: ")
            if not value_str.isdigit():
                raise ValueError("아이템의 개수를 입력하지 않았습니다.")
            value = int(value_str)
            location_str = input("아이템의 위치를 입력하세요 (예: stack,column,shelf): ")
            location = Database.parse_location(location_str)
            database.update(key, value, location)
            print("아이템이 성공적으로 업데이트되었습니다.")
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print("잘못된 입력입니다. 숫자를 입력해주세요.")
            elif str(e) == "아이템의 이름을 입력하지 않았습니다.":
                print("아이템의 이름을 입력하지 않았습니다. 다시 시도해주세요.")
            elif str(e) == "아이템이 데이터베이스에 존재하지 않습니다.":
                print("아이템이 데이터베이스에 존재하지 않습니다. 다시 시도해주세요.")
            elif str(e) == "아이템의 개수를 입력하지 않았습니다.":
                print("아이템의 개수를 입력하지 않았습니다. 다시 시도해주세요.")
            else:
                print("잘못된 입력입니다. 위치를 올바르게 입력해주세요.")
            return

    @staticmethod
    def delete_item(database):
        try:
            key = input("아이템의 이름을 입력하세요: ")
            database.delete(key)
            print("아이템이 성공적으로 삭제되었습니다.")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            return
        
    @staticmethod
    def show_item(database):
        items = database.show()
        if not items:
            print("데이터베이스가 비어 있습니다.")
        else:
            print("\n{:<15} {:<10} {:<20}".format("아이템", "수량", "위치 (스택, 열, 선반)"))
            print("-" * 50)
            for item, details in items.items():
                location = details['location']
                print("{:<15} {:<10} {:<20}".format(
                    item, 
                    details['count'], 
                    f"{location.stack}, {location.column}, {location.shelf}"
                ))
            print()

    @staticmethod
    def relocate_item(database):
        try:
            key = input("아이템의 이름을 입력하세요: ")
            location_str = input("아이템의 위치를 입력하세요 (예: stack,column,shelf): ")
            location = Database.parse_location(location_str)
            database.relocate(key, location)
            print("아이템이 성공적으로 재배치되었습니다.")
        except ValueError:
            print("잘못된 입력입니다. 위치를 올바르게 입력해주세요.")
            return

    @staticmethod
    def find_item(database):
        key = input("아이템의 이름을 입력하세요: ")
        item = database.get(key)
        if item:
            print(f"아이템: {key}, 수량: {item['count']}, 위치: {item['location'].stack}, {item['location'].column}, {item['location'].shelf}")
        else:
            print("아이템이 존재하지 않습니다.")

    # 프로그램이 종료 되면 database의 모든 데이터를 CSV 파일에 저장하는 함수를 만든다.
    @staticmethod
    def save_database(database):
        with open("database.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["key", "count", "stack", "column", "shelf"])
            for key, value in database.data.items():
                location = value['location']
                writer.writerow([key, value['count'], location.stack, location.column, location.shelf])
        print("데이터베이스가 성공적으로 저장되었습니다.")

    # 프로그램이 실행 되면 database.csv 파일을 읽어서 database를 초기화하는 함수를 만든다.
    @staticmethod
    def load_database():
        database = Database()
        try:
            with open("database.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    key = row["key"]
                    count = int(row["count"])
                    location = Location(int(row["stack"]), int(row["column"]), int(row["shelf"]))
                    database.insert(key, count, location)
        except FileNotFoundError:
            print("데이터베이스 파일이 없습니다. 새로운 데이터베이스를 생성합니다.")
        return database
