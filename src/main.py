from menus.main_menu import MainMenu


def main():
    while True:
        menu = MainMenu()

        while True:
            should_exit = menu.display()
            if should_exit:
                break


if __name__ == '__main__':
    main()
