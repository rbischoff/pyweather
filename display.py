import pygame
import os

DEFAULT_DRIVERS = ('fbcon', 'directfb', 'svgalib', 'Quartz')
DEFAULT_SIZE = (800, 400)
DEFAULT_SCREEN = 'no_frame'


class DisplayDriver:

    def __init__(self, drivers=DEFAULT_DRIVERS, size=DEFAULT_SIZE, screen_type=DEFAULT_SCREEN):

        formats = {'no_frame': pygame.NOFRAME, 'full_screen': pygame.FULLSCREEN}

        self._drivers = drivers
        self._size = size
        self._format = formats[screen_type]
        self._screen = None

    def __draw_screen(self):
        self._screen = pygame.display.set_mode(self._size, self._format)

        if not self._screen:
            raise AssertionError('Screen not defined')

        self._screen.fill((0, 0, 0))
        pygame.font.init()
        pygame.mouse.set_visible(0)
        pygame.display.update()

    def display_start(self):

        has_driver = False
        for driver in self._drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print('Driver: {} not loaded.'.format(driver))
                continue
            print('Driver: {} used.'.format(driver))
            has_driver = True
            break

        if not has_driver:
            raise Exception('No video driver available for use!')

        try:
            self.__draw_screen()
        except AssertionError as err:
            print(str(err))
            quit()


# Test block.  ditch this when done building the display
new_display = DisplayDriver()
new_display.display_start()
while True:
    pygame.time.wait(100)
