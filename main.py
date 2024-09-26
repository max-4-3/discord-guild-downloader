from sys import exit
import updater

from utility.main import Main

def check_for_update():
    """Function to check for update!"""
    print("Checking for updates")
    updater.main()

if __name__ == '__main__':
    check_for_update()
    main = Main()
    while True:
        try:
            if not main.confirmation():
                break
            main.showOptions()
            if input("Retry? (y/n): \n").lower().strip() in ["y", "yes"]:
                main.retry()
            else:
                break
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            print(f"Something went wrong: {repr(e)}")
            if input("Retry? (y/n): \n").lower().strip() in ["y", "yes"]:
                main.retry()
            else:
                break
