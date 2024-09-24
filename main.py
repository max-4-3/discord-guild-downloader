from sys import exit

from utility.main import Main

if __name__ == '__main__':
    main = Main()
    while True:
        try:
            if not main.confirmation():
                break
            main.showOptions()
            if input("Retry? (y/n): \n").lower().strip() in ["y", "yes"]:
                continue
            else:
                break
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            print(f"Something went wrong: {repr(e)}")
            if input("Retry? (y/n): \n").lower().strip() in ["y", "yes"]:
                continue
            else:
                break
