import pygame

# init pygame
pygame.init()

# clock
clock = pygame.time.Clock()

# display
yourDisplay = pygame.display.Info()
win = pygame.display.set_mode((yourDisplay.current_w, yourDisplay.current_h-60))

WIDTH, HEIGHT = win.get_width(), win.get_height()

# imgs
PLANE = pygame.transform.flip(pygame.image.load("images/plane.png"), True, False)
PLANE_RATIO = PLANE.get_height() / PLANE.get_width()
PLANE = pygame.transform.scale(PLANE, (HEIGHT / 5, HEIGHT /5 * PLANE_RATIO))

HEART = pygame.transform.scale(pygame.image.load("images/heart.png"), (60, 50))

MISSILE = pygame.transform.rotate(pygame.image.load("images/missile.png"), 90)
MISSILE_RATIO = MISSILE.get_height() / MISSILE.get_width()
MISSILE = pygame.transform.scale(MISSILE, (HEIGHT / 7, HEIGHT / 7 * MISSILE_RATIO))

GAME_BG = pygame.transform.scale(pygame.image.load("images/pixel_sky_2.jpg"), (WIDTH, HEIGHT))
MENU_BG = pygame.transform.scale(pygame.image.load("images/pixel_sky_1.png"), (WIDTH, HEIGHT))
SIGN_BG = pygame.transform.scale(pygame.image.load("images/sign_up.jpg"), (WIDTH, HEIGHT))

# colors
DARK_GREY = (40, 40, 40)
WHITE = (255, 255, 255)
GREY_BLUE = (216,228,252)
GREY = (80, 80, 80)
LIGHT_GREY = (248,244,244)
YELLOW = (240,188,68)
PINK = (255,220,204)
BLUE = (48,172,236)
MID_GREY = (150, 150, 150)
RED = (228,88,44)
BLACK = (0, 0, 0)

# fonts
huge_font = pygame.font.Font("fonts/pixel.ttf", 70)
med_font = pygame.font.Font("fonts/pixel.ttf", 50)
m_font = pygame.font.Font("fonts/pixel.ttf", 40)
font = pygame.font.Font("fonts/pixel.ttf", 30)
med_font_sans = pygame.font.SysFont("fonts/pixel.ttf", 60)
m_font_sans =pygame.font.SysFont("sans-serif", 40)
small_font = pygame.font.SysFont("sans-serif", 30)
mini_font = pygame.font.SysFont("sans-serif", 20)