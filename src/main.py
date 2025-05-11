from menus.main_menu import MainMenu, MainMenuChoice
# from menus.wallet_menu import wallet_menu, WalletMenuChoice


def main():
    while True:
        menu = MainMenu()

        while True:
            should_exit = menu.display()
            if should_exit:
                break


if __name__ == '__main__':
    main()
