import pygame, sys, random
from game import Plane, Missile
from settings import *
from helper import _spawn_missile, _check_all_collision, _blit_text_center, _blit_text_horizontal, _validate_log_in, _validate_log_in_input, _load_account, _store_new, _get_high_score, _change_high_score, _get_score, _save_score, _render_multi_line, _choose_question_easy, _choose_question_med, _choose_question_hard, Button, InputField
from menu import Menu

# score timer
INCREMENT_SCORE = pygame.USEREVENT
pygame.time.set_timer(INCREMENT_SCORE, 1000)

# current user
USER = 0

# preinitialized back and quit button
# used in multiple different menus
back = Button(5, 5, 50, 50, DARK_GREY, "<--", DARK_GREY, rect_width=10, font_color=DARK_GREY, font=m_font_sans, show_rect=False, outline_width=4)
qButton = Button(WIDTH - 55, 5, 50, 50, DARK_GREY, "Q", DARK_GREY, rect_width=10, font_color=DARK_GREY, font=m_font_sans, show_rect=False, outline_width=4)

# main game
def main(dif="easy"):
    player = Plane(150, HEIGHT / 2 - PLANE.get_height() / 2)

    # all missiles stored here
    missiles = []
    missiles += _spawn_missile()

    time = 1
    started = False
    starting_text = huge_font.render("Press Space to start the Game", 1, (50, 50, 50))

    # update window
    def redraw():
        win.fill(WHITE)
        win.blit(GAME_BG, (0, 0))

        player.draw()

        for missile in missiles:
            missile.draw()

    # main loop
    while 1:
        clock.tick(60) #60 fps

        # game over
        if player.lives <= 0:
            _change_high_score(USER, player.score)
            _save_score(USER, player.score)
            return restart_menu(player.score)

        # game
        if started:
            # move player
            player.move()

            # move missiles
            for missile in missiles[:]:
                missile.move()
                if missile.off_screen():
                    missiles.remove(missile)

            # collision with missiles or 20 sec mark
            if _check_all_collision(player, missiles) or time % 1200 == 0:
                # question if collision
                if dif == "easy":
                    q, solutions = _choose_question_easy()
                elif dif == "medium":
                    q, solutions = _choose_question_med()
                elif dif == "hard":
                    q, solutions = _choose_question_hard()
                if not popup_box(q, solutions):
                    player.lives -= 1
                time = 1
                missiles = []

            # update ui
            redraw()

            time += 1

        # pre-game
        else:
            redraw()

            _blit_text_center(starting_text)

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == INCREMENT_SCORE and started:
                player.score += 10
                missiles += _spawn_missile()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True

        pygame.display.update()

# all the menus
def menus():
    difficulty_menu = Menu(bg=MENU_BG, heading=huge_font.render("Choose your Difficulty", 1, GREY), buttons=[
    Button(WIDTH / 4 / 4, HEIGHT / 2 - WIDTH / 4 / 4, WIDTH / 4, WIDTH / 4 / 4, GREY_BLUE, "Easy", rect_width=50, font_color=GREY, font=m_font, outline_width=10, outline=(GREY_BLUE[0] - 25, GREY_BLUE[1] - 25, GREY_BLUE[2] - 25)),
    Button(WIDTH / 2 - WIDTH / 4 / 2, HEIGHT / 2 - WIDTH / 4 / 4, WIDTH / 4, WIDTH / 4 / 4, GREY_BLUE, "Medium", rect_width=50, font_color=GREY, font=m_font, outline_width=10, outline=(GREY_BLUE[0] - 25, GREY_BLUE[1] - 25, GREY_BLUE[2] - 25)),
    Button(WIDTH - WIDTH / 4 - WIDTH / 4 / 4, HEIGHT / 2 - WIDTH / 4 / 4, WIDTH / 4, WIDTH / 4 / 4, GREY_BLUE, "Hard", rect_width=50, font_color=GREY, font=m_font, outline_width=10, outline=(GREY_BLUE[0] - 25, GREY_BLUE[1] - 25, GREY_BLUE[2] - 25))
    ])

    start_menu = Menu(bg=MENU_BG, heading=huge_font.render("WINGMAN", 1, GREY), buttons=[
    Button(WIDTH / 4 / 4, HEIGHT - 30 - WIDTH / 4 / 4, WIDTH / 4, WIDTH / 4 / 4, GREY_BLUE, "Start", rect_width=50, font_color=GREY, font=m_font, outline_width=10, outline=(GREY_BLUE[0] - 25, GREY_BLUE[1] - 25, GREY_BLUE[2] - 25)),
    Button(WIDTH / 2 - WIDTH / 4 / 2, HEIGHT -30 - WIDTH / 4 / 4, WIDTH / 4, WIDTH / 4 / 4, GREY_BLUE, "Help", rect_width=50, font_color=GREY, font=m_font, outline_width=10, outline=(GREY_BLUE[0] - 25, GREY_BLUE[1] - 25, GREY_BLUE[2] - 25)),
    Button(WIDTH - WIDTH / 4 - WIDTH / 4 / 4, HEIGHT - 30 - WIDTH / 4 / 4, WIDTH / 4, WIDTH / 4 / 4, GREY_BLUE, "Game Log", rect_width=50, font_color=GREY, font=m_font, outline_width=10, outline=(GREY_BLUE[0] - 25, GREY_BLUE[1] - 25, GREY_BLUE[2] - 25))
    ])

    main_menu = Menu(bg=SIGN_BG, buttons=[
        Button(WIDTH / 2 - 200, HEIGHT / 2 - 80, 400, 60, WHITE, "Log In", rect_width=10, font_color=DARK_GREY, font=m_font, outline_width=5, outline=DARK_GREY, shadow=RED),
        Button(WIDTH / 2 - 200, HEIGHT / 2 + 20, 400, 60, WHITE, "Sign Up", rect_width=10, font_color=DARK_GREY, font=m_font, outline_width=5, outline=DARK_GREY, shadow=RED)
    ])

    play_menu = Menu(bg=MENU_BG)

    login_menu = Menu(bg=SIGN_BG)

    log_menu = Menu(bg=MENU_BG)

    main_menu.active = True
    sign_up = False

    # update ui
    def redraw():
        # draw only the menu that's active
        difficulty_menu.draw()
        start_menu.draw()
        main_menu.draw()

        if login_menu.active:
            login_menu.draw()
            b = log_in(sign_up)
            if b:
                start_menu.active = True
                login_menu.active = False
            else:
                login_menu.active = False
                main_menu.active = True

        if play_menu.active:
            play_menu.draw()
            if how_to_play():
                play_menu.active = False
                start_menu.active = True

        if log_menu.active:
            log_menu.draw()
            if game_log():
                log_menu.active = False
                start_menu.active = True

        if difficulty_menu.active:
            back.draw()
        if start_menu.active or main_menu.active:
            qButton.draw()

        pygame.display.update()

    while 1:
        clock.tick(30)

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # clickable parts of menus -> responses
                if difficulty_menu.click() is not None and difficulty_menu.active:
                    main("easy" if difficulty_menu.click() == 0 else "medium" if difficulty_menu.click() == 1 else "hard")
                if start_menu.click() == 0:
                    difficulty_menu.active = True
                    start_menu.active = False
                elif start_menu.click() == 1:
                    start_menu.active = False
                    play_menu.active = True
                elif start_menu.click() == 2:
                    start_menu.active = False
                    log_menu.active = True
                if main_menu.click() is not None and main_menu.active:
                    login_menu.active = True
                    main_menu.active = False
                    if main_menu.click() == 0:
                        sign_up = False
                    elif main_menu.click() == 1:
                        sign_up = True
                if back.click():
                    if difficulty_menu.active:
                        difficulty_menu.active = False
                        start_menu.active = True
                    elif login_menu.active:
                        login_menu.active = False
                        main_menu.active = True
                if qButton.click():
                    if main_menu.active or start_menu.active:
                        quit_popup()

            redraw()
# question popup
def popup_box(question, answers):
    # background
    box = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 200, 400, 400)
    # yellow filling
    filling = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 90, 400, 300)
    # smooth out corners
    overlap = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 90, 400, 20)

    # question
    question = font.render(question, 1, DARK_GREY)
    correct_answer = str(answers[0])
    random.shuffle(answers)
    # answer buttons
    buttons = [Button(WIDTH / 2 - 175, HEIGHT / 2 - 50, 150, 50, PINK, f"{answers[0]}", rect_width=50), Button(WIDTH / 2 + 25, HEIGHT / 2 - 50, 150, 50, PINK, f"{answers[1]}", rect_width=50), Button(WIDTH / 2 - 175, HEIGHT / 2 + 75, 150, 50, PINK, f"{answers[2]}", rect_width=50), Button(WIDTH / 2 + 25, HEIGHT / 2 + 75, 150, 50, PINK, f"{answers[3]}", rect_width=50)]

    while 1:
        clock.tick(30)

        # display box
        pygame.draw.rect(win, LIGHT_GREY, box, border_radius=20)
        pygame.draw.rect(win, YELLOW, filling, border_radius=20)
        pygame.draw.rect(win, YELLOW, overlap)

        _blit_text_horizontal(question, HEIGHT / 2 - 150)

        for button in buttons:
            button.draw()

        pygame.display.update()

        # listen for clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.click():
                        # right -> return True
                        # wrong -> return False
                        if button.real_text == correct_answer:
                            return True
                        return False


def restart_menu(score):
    # same sturcture as question popup
    box = pygame.Rect(WIDTH / 2 - 300, HEIGHT / 2 - 150, 600, 200)
    filling = pygame.Rect(WIDTH / 2 - 300, HEIGHT / 2 - 75, 600, 125)
    overlap = pygame.Rect(WIDTH / 2 - 300, HEIGHT / 2 - 75, 600, 20)

    score = font.render(f"Your Score was: {score}", 1, DARK_GREY)

    play_again = Button(WIDTH / 2 - 250, HEIGHT / 2 - 12.5, 175, 50, PINK, "Play Again", rect_width=50, font_color=GREY)
    back_to_menu = Button(WIDTH / 2 + 75, HEIGHT / 2 - 12.5, 175, 50, PINK, "Main Menu", rect_width=50, font_color=GREY)

    while 1:
        clock.tick(30)

        pygame.draw.rect(win, LIGHT_GREY, box, border_radius=20)
        pygame.draw.rect(win, YELLOW, filling, border_radius=20)
        pygame.draw.rect(win, YELLOW, overlap)

        _blit_text_horizontal(score, HEIGHT / 2 - 125)

        play_again.draw()
        back_to_menu.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again.click():
                    return main()
                elif back_to_menu.click():
                    return

# login functionality
def log_in(sign_up=False):
    # for redefining USER *globally*
    global USER
    # heading based on login/sign up
    if sign_up:
        heading = med_font_sans.render("Sign Up", 1, GREY)
    else:
        heading = med_font_sans.render("Login", 1, GREY)

    # background
    bg = pygame.Rect(WIDTH / 2 - 250, HEIGHT / 2 - 200, 500, 400)

    # inputs and buttons
    email = InputField(WIDTH / 2 - 225, HEIGHT / 2 - 50, 450, 50, MID_GREY, rect_width=50, outline_width=0, placeholder=small_font.render("Username/Email", 1, GREY))
    password = InputField(WIDTH / 2 - 225, HEIGHT / 2 + 25, 450, 50, MID_GREY, rect_width=50, outline_width=0, placeholder=small_font.render("Password", 1, GREY))
    sign_in = Button(WIDTH / 2 - 225, HEIGHT / 2 + 100, 450, 50, BLUE, "Sign In", rect_width=50, font=m_font_sans)

    error_message = None

    # response to submitting the input
    def sign_in_response():
        # validation
        if email.text != "" and password.text != "":
            if not sign_up:
                # try to load account
                loaded, message = _load_account(email.text, password.text)
                if not loaded:
                    # errors
                    error_message = mini_font.render(message, 1, RED)
                else:
                    # successfully loaded
                    return True, message
            else:
                # try to register account
                validation, message = _validate_log_in(email.text, password.text)
                if validation:
                    # try to store it
                    permit, user = _store_new(email.text, password.text)
                    if permit:
                        # successfully stored new account
                        return True, user + 1
                    else:
                        error_message = mini_font.render(user, 1, RED)
                else:
                    error_message = mini_font.render(message, 1, RED)
        else:
            error_message = mini_font.render("Both Inputs must be filled", 1, RED)

        # error -> display error message
        return error_message, None

    while 1:
        clock.tick(30)

        # update ui
        pygame.draw.rect(win, WHITE, bg, border_radius=20)
        win.blit(heading, (WIDTH / 2 - heading.get_width() / 2, HEIGHT / 2 - 150))
        email.draw()
        password.draw()
        sign_in.draw()

        back.draw()

        # display error
        if error_message:
            win.blit(error_message, (email.x + email.width / 2 - error_message.get_width() / 2, password.y + password.height + 12.5 - error_message.get_height() / 2))

        pygame.display.update()

        # event listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if email.click():
                    password.deactivate()
                    email.activate()
                elif password.click():
                    email.deactivate()
                    password.activate()
                elif back.click():
                    return False
                else:
                    password.deactivate()
                    email.deactivate()
                    if sign_in.click():
                        message, user = sign_in_response()
                        if message is True:
                            USER = user - 1
                            return True
                        else:
                            error_message = message
            # type event
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    message, user = sign_in_response()
                    if message is True:
                        USER = user - 1
                        return True
                    else:
                        error_message = message

                if event.key == pygame.K_BACKSPACE:
                    if email.active:
                        email.update_text(email.text[:-1])
                    elif password.active:
                        password.update_text(password.text[:-1])
                elif _validate_log_in_input(event.unicode):
                    if email.active:
                        email.update_text(email.text + event.unicode)
                    elif password.active:
                        password.update_text(password.text + event.unicode)

def quit_popup():
    # same sturcture as question popup
    box = pygame.Rect(WIDTH / 2 - 300, HEIGHT / 2 - 200, 600, 200)
    filling = pygame.Rect(WIDTH / 2 - 300, HEIGHT / 2 - 90, 600, 100)
    overlap = pygame.Rect(WIDTH / 2 - 300, HEIGHT / 2 - 90, 600, 20)

    question = font.render("Do you want to Quit the Game?", 1, DARK_GREY)

    yes = Button(WIDTH / 2 - 250, HEIGHT / 2 - 60, 175, 50, PINK, "Yes", rect_width=50, font_color=GREY)
    no = Button(WIDTH / 2 + 75, HEIGHT / 2 - 60, 175, 50, PINK, "No", rect_width=50, font_color=GREY)

    while 1:
        clock.tick(30)

        pygame.draw.rect(win, LIGHT_GREY, box, border_radius=20)
        pygame.draw.rect(win, YELLOW, filling, border_radius=20)
        pygame.draw.rect(win, YELLOW, overlap)

        _blit_text_horizontal(question, HEIGHT / 2 - 150)

        yes.draw()
        no.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes.click():
                    pygame.quit()
                    sys.exit()
                elif no.click():
                    return

def how_to_play():
    htp_heading = huge_font.render("How to Play", 1, WHITE)
    gm_heading = huge_font.render("Game Modes", 1, WHITE)

    texts = [
        _render_multi_line("To move the plane, press the arrow keys.", (WIDTH / 20, htp_heading.get_height() + 50), WIDTH / 2 - WIDTH / 20),
        _render_multi_line("You have to avoid incoming missiles.\nEvery time you get hit, you will have to answer a question. Depending on your choice, you'll either retain your life or lose it.", (WIDTH / 20, htp_heading.get_height() + 50), WIDTH / 2 - WIDTH / 20),
        _render_multi_line("A question will also pop up every 20 seconds.", (WIDTH / 20, htp_heading.get_height() + 50), WIDTH / 2 - WIDTH / 20),
        _render_multi_line("A tracker on the top right will record your score.", (WIDTH / 20, htp_heading.get_height() + 50), WIDTH / 2 - WIDTH / 20),
        _render_multi_line("You will recieve 3 lives in total.\nEvery time you lose a life, you will be respawned to the last checkpoint.", (WIDTH / 20, htp_heading.get_height() + 50), WIDTH / 2 - WIDTH / 20)
    ]

    easy = font.render("Easy - Addition and Subtraction", 1, (0,0,0))
    med = font.render("Medium - Multiplication and Division", 1, (0,0,0))
    hard = font.render("Hard - BODMAS Questions", 1, (0,0,0))

    while 1:
        win.blit(htp_heading, (WIDTH / 4 - htp_heading.get_width() / 2, 10))

        y_pos = 0
        for text, height in texts:
            for line in text:
                for word in line:
                    win.blit(word[0], (word[1][0], word[1][1] + y_pos))

            y_pos += height

        win.blit(gm_heading, (WIDTH * 0.75 - gm_heading.get_width() / 2, 10))
        win.blit(easy, (WIDTH / 2 + WIDTH / 20, gm_heading.get_height() + 50))
        win.blit(med, (WIDTH / 2 + WIDTH / 20, gm_heading.get_height() + 100))
        win.blit(hard, (WIDTH / 2 + WIDTH / 20, gm_heading.get_height() + 150))

        back.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.click():
                    return True

def game_log():
    # render text
    heading = huge_font.render("Game Log", 1, WHITE)
    game = m_font.render("Game", 1, BLACK)
    score = m_font.render("Score", 1, BLACK)

    # load and render last 10 games, high score
    last_10 = _get_score(USER)
    high =  med_font.render(f"High Score: {_get_high_score(USER)}", 1, BLACK)

    l10 = [font.render(str(i), 1, BLACK) for i in last_10]

    while 1:
        clock.tick(30)

        # draw text center horizontally
        _blit_text_horizontal(heading, 40)

        # top of table
        win.blit(game, (WIDTH / 5 - game.get_width() - 100, heading.get_height() + 20 + 70))
        pygame.draw.rect(win, BLACK, (WIDTH / 5 - game.get_width() - 110, heading.get_height() + 20 + 55, game.get_width() + 220 + score.get_width(), score.get_height() + 20), 3, 10)
        win.blit(score, (WIDTH / 5 + 100, heading.get_height() + 20 + 70))

        # valies of table
        for i, l in enumerate(l10):
            ng = font.render(str(i + 1), 1, BLACK)
            win.blit(ng, (WIDTH / 5 - game.get_width() / 2 - 100 - ng.get_width() / 2 - ng.get_width() / 2, heading.get_height() + 20 + 90 + score.get_height() + (ng.get_height() + 22) * i * 1.1))
            win.blit(l, (WIDTH / 5 + 100 + score.get_width() / 2 - l.get_width() / 2, heading.get_height() + 20 + 90 + score.get_height() + (l.get_height() + 22) * i * 1.1))
            pygame.draw.rect(win, BLACK, (WIDTH / 5 - game.get_width() - 110, heading.get_height() + 20 + 72 + 24 * i + score.get_height() + l.get_height() * i * 1.1, game.get_width() + 220 + score.get_width(), score.get_height() + 20), 3, 10)

        # high score
        win.blit(high, (WIDTH * 0.75 - high.get_width() / 2, heading.get_height() + 90))

        back.draw()

        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.click():
                    return True


# run if main file
if __name__ == "__main__":
    menus()
