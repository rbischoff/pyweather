import pygame
import os

DEFAULT_DRIVERS = ('fbcon', 'directfb', 'svgalib', 'Quartz')
DEFAULT_SIZE = (1024, 600)
DEFAULT_SCREEN = 'no_frame'


class DisplayDriver:

    def __init__(self, drivers=DEFAULT_DRIVERS, size=DEFAULT_SIZE, screen_type=DEFAULT_SCREEN, borders=(5, 5),
                 border_width=3):
        """DisplayDriver class is the class that build the base display for use in the weather
        app.  Argument descriptions: drivers is a tuple of strings with available SDL_VIDEODRIVER
        environmental varaibles; size is a tuple of two integers describing the x, y size of the
        screen; screen_type is a string value that corresponds to the pygame constants for
        dispay.set_mode
        """

        formats = {'no_frame': pygame.NOFRAME, 'full_screen': pygame.FULLSCREEN, 'double_buff': pygame.DOUBLEBUF,
                   'hw_surface': pygame.HWSURFACE, 'open_GL': pygame.OPENGL, 'resizable': pygame.RESIZABLE}

        self._drivers = drivers
        self._size = size
        self._borders = borders
        self._border_width = border_width
        self._format = formats[screen_type]
        self._screen = None

        self.errors = []

    def __draw_screen(self):
        """This function is intended to be used by the display_start function.
        It attempts to build the blank screen and raises an error if it fails."""

        self._screen = pygame.display.set_mode(self._size, self._format)

        if not self._screen:
            raise AssertionError('Screen not defined')

        self._screen.fill((0, 0, 0))
        pygame.font.init()
        pygame.mouse.set_visible(0)
        pygame.display.update()

    def __get_driver(self):
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
            raise AssertionError('No video driver available for use!')

    def __draw_frames(self):
        """This function should be called by the display_start function only. It renders the frames for the display"""
        xmin = self._borders[0]
        ymin = self._borders[1]
        xmax = self._size[0] - xmin
        ymax = self._size[1] - ymin
        line_width = self._border_width
        line_color = (255, 255, 255)

        # Horizontal line settings
        hz = (0.1, 0.5, 0.58)

        # Vertical line settings
        vt = (0.33, 0.66, 0.2, 0.4, 0.6, 0.8)

        # Draw Screen Border
        pygame.draw.line(self._screen, line_color, (xmin, xmin), (xmax, xmin), line_width)  # Top
        pygame.draw.line(self._screen, line_color, (xmin, xmin), (xmin, ymax), line_width)  # Left
        pygame.draw.line(self._screen, line_color, (xmin, ymax), (xmax, ymax), line_width)  # Bottom
        pygame.draw.line(self._screen, line_color, (xmax, ymin), (xmax, ymax), line_width)  # Right Edge

        # Draw Inner Frames
        # Horizontal lines (1, 2, 3)
        for h in hz:
            pygame.draw.line(self._screen, line_color, (xmin, ymax * h), (xmax, ymax * h), line_width)

        # Vertical lines (1, 2)
        for i in range(2):
            v = vt[i]
            pygame.draw.line(self._screen, line_color, (xmax * v, ymax * hz[2]), (xmax * v, ymax * hz[0]), line_width)

        # Vertical lines (3 - 6)
        for i in range(2, len(vt)):
            v = vt[i]
            pygame.draw.line(self._screen, line_color, (xmax * v, ymax), (xmax * v, ymax * hz[2]), line_width)

    def display_start(self):
        """display_start is the main initializer for the display it makes calls to many other
        internal functions in order do build the dispay as defined in the initialization of the
        DispayDriver class."""

        try:
            self.__get_driver()
            self.__draw_screen()
            self.__draw_frames()
            pygame.display.update()
        except AssertionError as err:
            print(err)
            quit()


# Test block.  ditch this when done building the display
new_display = DisplayDriver()
new_display.display_start()


while True:
    pygame.time.wait(100)
