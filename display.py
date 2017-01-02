import pygame
import os
import time
from random import randint
from system_data import SystemData
from settings import ICON_BASE_DIR, ICON_DICTIONARY

DEFAULT_DRIVERS = ('fbcon', 'directfb', 'svgalib', 'Quartz')
DEFAULT_SIZE = (1024, 600)
DEFAULT_SCREEN = 'no_frame'


class DisplayDriver:

    def __init__(self, drivers=DEFAULT_DRIVERS, size=DEFAULT_SIZE, screen_type=DEFAULT_SCREEN, borders=(5, 5),
                 border_width=3, line_color=(255, 255, 255), font='freesans', font_color=(255, 255, 255),
                 icons=ICON_DICTIONARY):
        """DisplayDriver class is the class that build the base display for use in the weather
        app.  Argument descriptions: drivers is a tuple of strings with available SDL_VIDEODRIVER
        environmental varaibles; size is a tuple of two integers describing the x, y size of the
        screen; screen_type is a string value that corresponds to the pygame constants for
        dispay.set_mode
        """

        formats = {'no_frame': pygame.NOFRAME, 'full_screen': pygame.FULLSCREEN, 'double_buff': pygame.DOUBLEBUF,
                   'hw_surface': pygame.HWSURFACE, 'open_GL': pygame.OPENGL, 'resizable': pygame.RESIZABLE}

        self._system_data = SystemData()
        self._drivers = drivers
        self._size = size
        self._borders = borders
        self._border_width = border_width
        self._line_color = line_color
        self._font = font
        self._font_color = font_color
        self._format = formats[screen_type]
        self._icons = icons
        self._base_dir = os.getcwd() + ICON_BASE_DIR
        self._scale_icons = True
        self._xmax = self._size[0] - self._borders[0]
        self._ymax = self._size[1] - self._borders[1]
        self._screen = None

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

    def __draw_frames(self):
        """This function should be called by the display_start function only. It renders the frames for the display"""
        xmin = self._borders[0]
        ymin = self._borders[1]
        xmax = self._xmax
        ymax = self._ymax
        line_width = self._border_width

        # Horizontal line settings
        hz = (0.1, 0.5, 0.58)

        # Vertical line settings
        vt = (0.33, 0.66, 0.2, 0.4, 0.6, 0.8)

        self._screen.fill((0, 0, 0))

        # Draw Screen Border
        pygame.draw.line(self._screen, self._line_color, (xmin, xmin), (xmax, xmin), line_width)  # Top
        pygame.draw.line(self._screen, self._line_color, (xmin, xmin), (xmin, ymax), line_width)  # Left
        pygame.draw.line(self._screen, self._line_color, (xmin, ymax), (xmax, ymax), line_width)  # Bottom
        pygame.draw.line(self._screen, self._line_color, (xmax, ymin), (xmax, ymax), line_width)  # Right Edge

        # Draw Inner Frames
        # Horizontal lines (1, 2, 3)
        for h in hz:
            pygame.draw.line(self._screen, self._line_color, (xmin, ymax * h), (xmax, ymax * h), line_width)

        # Vertical lines (1, 2)
        for j in range(2):
            v = vt[j]
            pygame.draw.line(self._screen, self._line_color, (xmax * v, ymax * hz[2]),
                             (xmax * v, ymax * hz[0]), line_width)

        # Vertical lines (3 - 6)
        for j in range(2, len(vt)):
            v = vt[j]
            pygame.draw.line(self._screen, self._line_color, (xmax * v, ymax), (xmax * v, ymax * hz[2]), line_width)

    def __display_datetime(self):

        th = 0.07  # Time Text Height
        sh = 0.03  # Seconds Text Height
        dh = 0.06  # Date Text Height
        tm_y = 10  # Time Y Position
        tm_y_sm = 15  # Time & Date Y Position Small
        dt_y = 13

        tfont = pygame.font.SysFont(self._font, int(self._ymax * th), bold=1)  # Time Font
        dfont = pygame.font.SysFont(self._font, int(self._ymax * dh), bold=1)  # Date Font
        sfont = pygame.font.SysFont(self._font, int(self._ymax * sh), bold=1)  # Small Font for Seconds

        tm1 = time.strftime("%H:%M", time.localtime())  # Time
        tm2 = time.strftime("%S", time.localtime())  # Seconds
        dt1 = time.strftime("%d %b %y").upper()  # Date

        rtm1 = tfont.render(tm1, True, self._font_color)
        (tx1, ty1) = rtm1.get_size()
        rtm2 = sfont.render(tm2, True, self._font_color)
        (tx2, ty2) = rtm2.get_size()
        rdt1 = dfont.render(dt1, True, self._font_color)
        (dx1, dy1) = rdt1.get_size()

        tp = self._xmax / 2 - (tx1 + tx2) / 2
        dp = self._xmax - (dx1 + (self._borders[1] * 2))
        self._screen.blit(rtm1, (tp, tm_y))
        self._screen.blit(rtm2, (tp + tx1 + 3, tm_y_sm))
        self._screen.blit(rdt1, (dp, dt_y))

    def __get_signal_icon(self):
        sig_no = self._system_data.ws.sig_strength
        return self._base_dir + self._icons['sig{}'.format(sig_no)]

    def __display_connected(self):
        xmin = self._borders[0]
        ymin = self._borders[1]
        station_scale = 0.35
        signal_scale = 0.25

        station_icon = pygame.image.load_extended(self._base_dir + self._icons['weather_station']).convert_alpha()
        signal_icon = pygame.image.load_extended(self.__get_signal_icon()).convert_alpha()
        (stix, stiy) = station_icon.get_size()
        (sgix, sgiy) = signal_icon.get_size()

        if self._scale_icons:
            station_icon = pygame.transform.scale(station_icon, (int(stix * station_scale), int(stiy * station_scale)))
            (stix, stiy) = station_icon.get_size()
            signal_icon = pygame.transform.scale(signal_icon, (int(sgix * signal_scale), int(sgiy * signal_scale)))

        self._screen.blit(station_icon, (xmin * 2, ymin))
        self._screen.blit(signal_icon, (stix + 14, ymin + 9))

    def __display_forecasts(self):

        days = 5
        hz = (0.1, 0.5, 0.58)
        vt = (0.33, 0.66, 0.2, 0.4, 0.6, 0.8)
        vdiff = vt[4] - vt[3]
        yo = self._ymax * hz[2] + 5
        vc = 0 + vdiff / 2  # Y center

        th = 0.045          # Text Height
        rpth = 0.08         # Rain Present Text Height
        gp = 5              # Line Spacing Gap

        font = pygame.font.SysFont(self._font, int(self._ymax * th), bold=1)
        lgfont = pygame.font.SysFont(self._font, int(self._ymax * rpth), bold=1)

        for j in range(days):
            vci = vc + (j * vdiff)
            today = self._system_data.forecasts.forecasts[j]
            header = font.render(today.day, True, self._line_color)
            temps = font.render(today.low_temp + ' / ' + today.high_temp, True, self._line_color)
            rain = lgfont.render(today.rain + '%', True, self._line_color)
            icon = pygame.image.load_extended(self._base_dir +
                                              self._system_data.weather_icons[today.icon]).convert_alpha()

            (hx, hy) = header.get_size()
            (tx, ty) = temps.get_size()
            (rx, ry) = rain.get_size()
            (ix, iy) = icon.get_size()

            if self._scale_icons:
                icon = pygame.transform.scale(icon, (int(ix * 1.15), int(iy * 1.15)))
                (ix, iy) = icon.get_size()

            if iy < 104:
                ye = (104 - iy) / 2
            else:
                ye = 0

            self._screen.blit(header, (self._xmax * vci - hx / 2, yo))
            self._screen.blit(icon, (self._xmax * vci - ix / 2, hy + yo + ye + (gp * 2)))
            self._screen.blit(temps, (self._xmax * vci - tx / 2, self._ymax - (ry + ty + (gp * 2))))
            self._screen.blit(rain, (self._xmax * vci - rx / 2, self._ymax - (ry + gp)))

    def display_start(self):
        """display_start is the main initializer for the display it makes calls to many other
        internal functions in order do build the dispay as defined in the initialization of the
        DispayDriver class."""

        try:
            self.__get_driver()
            self.__draw_screen()
            self.__draw_frames()
            self.__display_datetime()
            self.__display_connected()
            self.__display_forecasts()
            pygame.display.update()
        except AssertionError as err:
            print(err)
            quit()

    def update_diplay(self):
        try:
            self.__draw_frames()
            self.__display_datetime()
            self.__display_connected()
            self.__display_connected()
            self.__display_forecasts()
            pygame.display.update()
        except AssertionError as err:
            print("Update Error + {}".format(str(err)))


# Test block.  ditch this when done building the display

day_list = ['Today', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
wind_dir = ['N', 'E', 'W', 'S', 'NE', 'NW', 'SE', 'SW', 'NNE', 'ENE', 'NNW', 'WNW', 'SSE', 'ESE', 'SSW', 'WSW']

new_display = DisplayDriver()
new_display.display_start()

for i in range(5):
    low = randint(0, 90)
    day = new_display._system_data.forecasts.forecasts[i]
    day.update_day(day=day_list[i], low_temp=str(low), high_temp=str(randint(low, 90)), feels_like=str(randint(0, 90)),
                   icon=randint(0, 47), wind_speed=str(randint(0, 30)), bara=str(randint(0, 30)),
                   wind_dir=wind_dir[randint(0, 15)], rain=str(randint(0, 100)))

i = 0
w = 0
while True:
    pygame.time.wait(1000)
    new_display._system_data.ws.sig_strength = (i % 5)
    new_display._system_data.forecasts.forecasts[0].icon = (i % 47)
    i += 1
    new_display.update_diplay()
