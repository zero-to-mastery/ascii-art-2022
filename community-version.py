## Community Version
from time import sleep
from random import choice


def handle_image_print(image_ascii):
    """This function should be run at the end of handle_image_converstion() on line 56 in place of print(image_ascii)"""

    verbs = [
        "Articulating", "Coordinating", "Gathering", "Powering up", "Clicking on", "Backing up", "Extrapolating", "Authenticating", "Recovering", "Finalizing", "Testing", "Upgrading"
    ]

    nouns = [
        "scope", "lunch", "meetings", "skeletons", "devices", "margins", "bookmarks", "CPUs", "folders", "emails", "disks", "JPEGs", "ROMs", "Viruses"
    ]

    print("Turning your image into ASCII art...")
    sleep(1)
    for i in range(4):
        print(f"{choice(verbs)} {choice(nouns)}...")
        sleep(1)
    print("Here we go...!")
    sleep(1)
    print()
    print(image_ascii)


if __name__ == '__main__':
    # print(handle_image_print.__doc__)
    handle_image_print("test")
