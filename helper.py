# helper functions and classes
import pandas as pd
import random, pygame, csv, ast
from settings import *
from game import Missile
import matplotlib.pyplot as plt

# Helper functions for the game
def _custom_round(x, base=10):
    return base * round(x/base)

# spawn missile at random locations
def _spawn_missile():
    missiles = []
    sections = [(0, round(HEIGHT / 4)), (round(HEIGHT / 4) + 1, round(HEIGHT / 2)), (round(HEIGHT / 2) + 1, round(HEIGHT * 0.75)), (round(HEIGHT * 0.75) + 1, HEIGHT - MISSILE.get_height())]
    for i in range(len(sections)):
        if random.randint(0,2):
            missiles.append(Missile(random.randint(WIDTH, WIDTH + MISSILE.get_width()), random.randint(sections[i][0], sections[i][1])))

    return missiles

# check if player collides with any missile
def _check_all_collision(player, missiles):
    for missile in missiles:
        if player.collision(missile.mask, missile.x, missile.y):
            return True
    return False

# draw text in center of screen
def _blit_text_center(text):
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

# draw text horizontal center
def _blit_text_horizontal(text, hp):
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, hp))

# validate and register new account
def _store_new(login, password):
    if _check_exists(login):
        return False, "Username/Email already exists"

    with open("data/database.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")

        writer.writerow([login, password, [], 0])

        df = pd.read_csv("data/database.csv")
        return True, len(df)

# validate and load new account
def _load_account(login, password):
    f = False
    with open("data/database.csv", "r", newline="") as file:
        reader = csv.reader(file, delimiter=";")

        for i, line in enumerate(reader):
            if line[0] == login:
                f = True
                if line[1] == password:
                    return True, i
                
    return False, "Wrong Mail" if not f else "Wrong Password"

# check if account exists
def _check_exists(login):
    with open("data/database.csv", "r") as file:
        reader = csv.reader(file, delimiter=";")
        for line in reader:
            if line[0] == login:
                return True
    return False

# validate log in
def _validate_log_in(login, password):
    if not len(password) >= 8:
        return False, "Password Length must be >= 8"

    return True, ""

# validate log in input
def _validate_log_in_input(s):
    if s.isalpha() or s.isdigit():
        return True
    if s in ["@", ".", "!", "$", "?", "=", "(", ")", "/", "%", "-", "_", ":"]:
        return True
    return False

# get user score from database
def _get_score(user):
    df = pd.read_csv("data/database.csv", sep=";")

    cur_scores = df.iloc[user]["scores"]
    if cur_scores != "[]":
        return ast.literal_eval(cur_scores)
    return []

# save score in last 10 games
def _save_score(user, new_score):
    df = pd.read_csv("data/database.csv", sep=";")

    cur_scores = df.iloc[user]["scores"]
    if cur_scores != "[]":
        cur_scores = ast.literal_eval(cur_scores)
    else:
        cur_scores = []
    cur_scores = cur_scores[1:] if len(cur_scores) >= 10 else cur_scores
    cur_scores.append(new_score)
    print(cur_scores)
    df.loc[user, "scores"] = f"{cur_scores}"

    df.to_csv("data/database.csv", index=False, sep=";")

# get user high score from database
def _get_high_score(user):
    df = pd.read_csv("data/database.csv", sep=";")

    return int(df.iloc[user]["high"])

# change high score in database
def _change_high_score(user, new_high):
    df = pd.read_csv("data/database.csv", sep=";")

    cur_high = int(df.iloc[user]["high"])
    if new_high > cur_high:
        df.loc[user, "high"] = str(new_high)

        df.to_csv("data/database.csv", index=False, sep=";")

# render long text into multiple lines
def _render_multi_line(text, pos, max_width, font=font):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x, y = pos
    tx = []
    height = 0
    for line in words:
        ln = []
        for word in line:
            word_surface = font.render(word, 1, (0,0,0))
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height * 1.5
                height += word_height * 1.5
            ln.append([word_surface, (x,y)])
            x += word_width + space
        x = pos[0]
        y += word_height * 1.5
        height += word_height * 1.5
        tx.append(ln)

    return tx, height + word_height * 1

# choose an easy question
def _choose_question_easy():
    # addition or subtraction
    if random.randint(0, 1):
        # easy or more difficult
        r = random.randint(0,2)
        if not r:
            # difficult
            n1 = random.randint(1, 255)
            n2 = random.randint(1, 255)
        elif r == 1:
            # medium
            n1 = _custom_round(random.randint(0, 250))
            n2 = _custom_round(random.randint(0, 250))
        elif r == 2:
            # easy
            n1 = random.randint(0, 10)
            n2 = random.randint(0, 10)

        solutions = [n1 + n2, n1 + n2 - random.randint(1, 25), n1 + n2 + random.randint(1, 25), n1 + n2 + random.randint(1,5)]
        q = f"What is {n1} + {n2}?"

    else:
        r = random.randint(0,2)
        if not r:
            n1 = random.randint(1, 255)
            n2 = random.randint(1, n1)
        elif r == 1:
            n1 = _custom_round(random.randint(0, 250))
            n2 = _custom_round(random.randint(0, n1))
        elif r == 2:
            n1 = random.randint(0, 10)
            n2 = random.randint(0, n1)

        solutions = [n1 - n2, n1 - n2 - random.randint(1, 25), n1 - n2 + random.randint(1, 25), n1 - n2 - random.randint(1,5)]
        q = f"What is {n1} - {n2}?"

    return q, solutions

# choose a medium question
def _choose_question_med():
    # multiplication or division
    if random.randint(0, 1):
        # easy or more difficult
        r = random.randint(0,2)
        if not r:
            # difficult
            n1 = random.randint(1, 50)
            if n1 % 5 == 0:
                n2 = random.randint(1, 10)
            else:
                n2 = random.choice([2,4,5,10])
        elif r == 1:
            # medium
            n1 = random.randint(0,15)
            n2 = random.randint(0,6)
        elif r == 2:
            # easy
            n1 = _custom_round(random.randint(0, 50))
            n2 = random.choice([2,4,5,10])

        solutions = [n1 * n2, n1 * n2 - random.randint(1, 25), n1 * n2 + random.randint(1, 25), n1 * n2 + random.randint(1,5)]
        q = f"What is {n1} * {n2}?"

    else:
        # division
        r = random.randint(0,2)
        if not r:
            n1 = random.randint(1, 50)
            n2 = random.choice([i for i in range(1, 50) if n1 % i == 0])
        elif r == 1:
            n1 = _custom_round(random.randint(0, 250), 10)
            n2 = random.choice([2,5,10])
        elif r == 2:
            n1 = _custom_round(random.randint(0,500))
            n2 = 5

        solutions = [int(n1 / n2), int(n1 / n2) - random.randint(1, 3), int(n1 / n2) + random.randint(1, 3), int(n1 / n2) + random.randint(1,2)]
        q = f"What is {n1} / {n2}?"

    return q, solutions

# hard
def _choose_question_hard():
    # brackets or multiplication/division
    if random.randint(0,1):
        if random.randint(0,1):
            # square root
            n1 = random.randint(0,25)
            solutions = [int(n1 ** 2), int(n1 ** 2) - random.randint(1, 25), int(n1 ** 2) + random.randint(1, 25), int(n1 ** 2) + random.randint(1,10)]
            q = f"What is {n1}^2?"

            return q, solutions
        else:
            # brackets
            r = random.randint(0,2)
            if not r:
                # brackets addition + multiplication
                n1 = random.randint(0,25)
                n2 = random.randint(0,25)
                n3 = random.randint(1,5)

                solutions = [(n1 + n2) * n3, (n1 + n2) * n3 - random.randint(1, 25), (n1 + n2) * n3 + random.randint(1, 25), (n1 + n2) * n3 + random.randint(1,10)]
                q = f"What is ({n1} + {n2}) * {n3}?"
            elif r == 1:
                # brackets subtraction + multiplication
                n1 = random.randint(0,25)
                n2 = random.randint(1,n1)
                n3 = random.randint(1,5)

                solutions = [(n1 - n2) * n3, (n1 - n2) * n3 - random.randint(1, 25), (n1 - n2) * n3 + random.randint(1, 25), (n1 - n2) * n3 + random.randint(1,10)]
                q = f"What is ({n1} - {n2}) * {n3}?"
            else:
                # brackets square root + addition
                n1 = random.randint(0,25)
                n2 = random.randint(0,25-n1)
                n3 = random.randint(1, 75)

                solutions = [(n1 + n2)**2 + n3, (n1 + n2)**2 + n3 - random.randint(1, 25), (n1 + n2)**2 + n3 + random.randint(1, 25), (n1 + n2)**2 + n3 + random.randint(1,10)]
                q = f"What is ({n1} + {n2})^2 + {n3}?"
            
            return q, solutions
    else:
        return _choose_question_med()

# helper classes
# Buttons
class Button(pygame.Rect):
    def __init__(self, x, y, width, height, color, text, outline=None, outline_width=3, rect_width=0, font_color=WHITE, font=font, shadow=None, shadow_size=5, show_rect=True):
        super().__init__(x, y, width, height)
        self.color = color
        self.outline = outline
        self.outline_width = outline_width
        self.rect_width = rect_width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = font.render(text, 1, font_color)
        self.real_text = text
        self.shadow = shadow
        self.shadow_size = shadow_size
        self.show_rect = show_rect

    def draw(self):
        if self.shadow:
            pygame.draw.rect(win, self.shadow, (self.rect.x + self.shadow_size, self.y + self.shadow_size, self.rect.width, self.rect.height), border_radius=self.rect_width)
        if self.show_rect:
            pygame.draw.rect(win, self.color, self.rect, 0, self.rect_width)
        win.blit(self.text, (self.rect.x + self.width / 2 - self.text.get_width() / 2, self.rect.y + self.height / 2 - self.text.get_height() / 2))
        if self.outline:
            pygame.draw.rect(win, self.outline, self.rect, self.outline_width, self.rect_width)

    def click(self):
        m = pygame.mouse.get_pos()
        if self.rect.collidepoint(m):
            return True
        return False

# Input Fields
class InputField:
    def __init__(self, x, y, width, height=None, color=WHITE, rect_width=0, outline_width=2, font=small_font, placeholder=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height if height else font.render("Test", 1, GREY).get_height() * 1.2
        
        self.color = color
        self.rect_width = rect_width
        self.outline_width = outline_width
        self.font = font
        self.placeholder = placeholder if placeholder else font.render("", 1, DARK_GREY)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = ""
        self.active = False
        self.text_surf = self.font.render(self.text, 1, DARK_GREY)

        self.time = 0
        self.cursor_active = False
        self.cursor = pygame.Rect(self.x + 15 + self.text_surf.get_width() + 1, self.y + self.rect.height / 2 - self.text_surf.get_height() * 0.55, 3, self.text_surf.get_height() * 1.1)

    def draw(self):
        pygame.draw.rect(win, self.color, self.rect, self.outline_width, self.rect_width)
        if self.text == "" and not self.active:
            win.blit(self.placeholder, (self.x + 15, self.y + self.rect.height / 2 - self.placeholder.get_height() / 2))
        else:
            if self.active:
                self.draw_cursor()
            win.blit(self.text_surf, (self.x + 15, self.y + self.rect.height / 2 - self.text_surf.get_height() / 2))


    def update_text(self, new_text):
        self.text = new_text
        self.text_surf = self.font.render(self.text, 1, GREY)
        self.cursor.x = self.x + 15 + self.text_surf.get_width() + 1

    def click(self):
        m = pygame.mouse.get_pos()
        if self.rect.collidepoint(m):
            return True
        return False

    def activate(self):
        self.active = True
        #self.color = RED

    def deactivate(self):
        self.active = False
        self.time = 0
        self.cursor_active = True
        #self.color = BLACK

    def draw_cursor(self):
        self.time += 1

        if self.time >= 15:
            self.time = 0
            self.cursor_active = not self.cursor_active

        if self.cursor_active:
            pygame.draw.rect(win, DARK_GREY, self.cursor)