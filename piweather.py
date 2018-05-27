import display


def main():
    disp = display.DisplayDriver(screen_type="full_screen")
    # disp.update_daily_data()
    # disp.update_current_data()
    disp.run()


if __name__ == "__main__":
    main()
