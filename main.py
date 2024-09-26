from sys import exit
import updater
import argparse

from utility.main import Main


def check_for_update():
    """Function to check for update!"""
    print("Checking for updates")
    updater.main()


def argument():
    parser = argparse.ArgumentParser(description="Check for updates to the application.")
    
    # The flag --update, if present, sets the value to True, otherwise False.
    parser.add_argument('--update', action='store_true', help="Whether to update or not!", required=False)

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    if not argument().update:
        check_for_update()
    else:
        print("Update skipped!")
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
