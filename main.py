from database import Database

def main():
    database = Database.load_database()
    while True:
        print("============================================")
        print("I : 아이템 추가", end=",  ")
        print("R : 아이템 수정", end=",  ")
        print("D : 아이템 삭제", end=",  ")
        print("S : 아이템 보기", end=",  ")
        print("M : 아이템 이동", end=",  ")
        print("F : 아이템 찾기", end=",  ")
        print("X : 종료")
        choice = input("원하는 작업을 선택하세요: ").upper()
        if choice == "I":
            Database.insert_item(database)
        elif choice == "R":
            Database.update_item(database)
        elif choice == "D":
            Database.delete_item(database)
        elif choice == "S":
            Database.show_item(database)
        elif choice == "M":
            Database.relocate_item(database)
        elif choice == "F":
            Database.find_item(database)
        elif choice == "X":
            Database.save_database(database)
            break
        else:
            print("잘못된 입력입니다. 다시 입력하세요.")

if __name__ == "__main__":
    main()
    


