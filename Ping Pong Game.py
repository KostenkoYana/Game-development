import pygame
import sys
import random
import time
import csv
import datetime


def write_results_to_csv(_filename, _score_left, _score_right, _playtime):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, _score_left, _score_right, _playtime])


def resetBall():  # Returns the ball to the central position
    # Reset the ball to the center
    ball.x = WIDTH // 2 - BALL_RADIUS
    ball.y = HEIGHT // 2 - BALL_RADIUS
    # Changing the direction of the ball
    BALL_SPEED[0] = -BALL_MAIN_SPEED[0]
    # Random selection of the direction of movement of the ball vertically
    BALL_SPEED[1] = random.choice([-BALL_MAIN_SPEED[1], BALL_MAIN_SPEED[1]])


# Initialization Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MENU_FONT_SIZE = 48
SCORE_FONT_SIZE = 36
GAME_TIME_LIMIT = 31  #  Game time + 1 second to start
SPEED_MULTIPLIER = 1.05  # 1 - speed does not increase

BALL_MAIN_SPEED = [5, 5]
BALL_SPEED = BALL_MAIN_SPEED.copy()
PADDLE_SPEED = 7
# Creating a game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pingpong by Yana Kostenko")

# Creation of objects
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
paddle_left = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

clock = pygame.time.Clock()

# Counting points
score_left = 0
score_right = 0

# Timer
start_time = time.time()

# The menu option is selected
selected_option = "Start"
elapsed_time = 0

# Game state index (0 - menu, 1 - game, 2 - final screen)
game_state = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # When exiting (closing the program)
            write_results_to_csv('game_results.csv', score_left, score_right, f"{elapsed_time:.3f}")
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_state == 0:

                    if selected_option == "Start":
                        # Start a new game
                        game_state = 1  # Changing the state of the game on a game-by-game basis
                        resetBall()
                        score_left = 0
                        score_right = 0
                        start_time = time.time()

                    elif selected_option == "Quit":
                        # Quit the game
                        pygame.quit()
                        sys.exit()

                elif game_state == 2:
                    if event.key == pygame.K_RETURN:
                        game_state = 0
                        write_results_to_csv('game_results.csv', score_left, score_right, f"{elapsed_time:.3f}")

            elif event.key == pygame.K_UP:
                # Processing of the "up" key in the menu
                if selected_option == "Start":
                    selected_option = "Quit"
                elif selected_option == "Quit":
                    selected_option = "Start"
            elif event.key == pygame.K_DOWN:
                # Processing of the "down" key in the menu
                if selected_option == "Start":
                    selected_option = "Quit"
                elif selected_option == "Quit":
                    selected_option = "Start"

    if game_state == 1:  # Game
        # Checking the end of the game by time
        elapsed_time = time.time() - start_time
        if elapsed_time >= GAME_TIME_LIMIT:
            game_state = 2  # Changing the game state to the final screen

        keys = pygame.key.get_pressed()

        # Left racket control
        if keys[pygame.K_w] and paddle_left.top > 0:
            paddle_left.y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle_left.bottom < HEIGHT:
            paddle_left.y += PADDLE_SPEED

        # Control with the right racket
        if keys[pygame.K_UP] and paddle_right.top > 0:
            paddle_right.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle_right.bottom < HEIGHT:
            paddle_right.y += PADDLE_SPEED

        # The logic of ball movement
        ball.x += BALL_SPEED[0]
        ball.y += BALL_SPEED[1]

        # Bounce of the ball from the walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_SPEED[1] = -BALL_SPEED[1]

        # Bounce of the ball from rackets
        if ball.colliderect(paddle_left) or ball.colliderect(paddle_right):
            BALL_SPEED[0] = -BALL_SPEED[0] * SPEED_MULTIPLIER

        # Check win or lose
        if ball.left <= 0:
            # The player on the right gets a point
            score_right += 1
            # Reset the ball to the center
            resetBall()
        elif ball.right >= WIDTH:
            # The player on the left gets a point
            score_left += 1
            # Reset the ball to the center
            resetBall()

        # Displaying objects on the screen
        screen.fill(BLACK)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.rect(screen, WHITE, paddle_left)
        pygame.draw.rect(screen, WHITE, paddle_right)

        # Point display
        font = pygame.font.Font(None, SCORE_FONT_SIZE)
        score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - 50, 20))

        # Timer display
        timer_font = pygame.font.Font(None, SCORE_FONT_SIZE)
        timer_display = timer_font.render(f"Time: {int(GAME_TIME_LIMIT - elapsed_time)}", True, WHITE)
        screen.blit(timer_display, (10, 10))

    elif game_state == 2:  # Final screen
        # Displaying the results of the game after the end of the timer
        screen.fill(BLACK)
        menu_font = pygame.font.Font(None, MENU_FONT_SIZE)
        result_text = menu_font.render(f"   Game over! {score_left} - {score_right}", True, WHITE)
        continue_text = menu_font.render(f"     Press Enter to go to the menu", True, WHITE)
        screen.blit(result_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        screen.blit(continue_text, (WIDTH // 2 - 300, HEIGHT // 2 - 20))

    elif game_state == 0:  # main menu

        # Displaying the main menu or game results
        screen.fill(BLACK)
        menu_font = pygame.font.Font(None, MENU_FONT_SIZE)

        start_text = menu_font.render("Start", True, WHITE)
        quit_text = menu_font.render("Exit", True, WHITE)

        # Displaying the selected menu option (we highlight the selected option)
        if selected_option == "Start":
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 60, HEIGHT // 2 - 60, 120, 60), 2)
        else:
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 60, HEIGHT // 2 + 10, 120, 60), 2)

        if selected_option == "Quit":
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 60, HEIGHT // 2 + 10, 120, 60), 2)
        else:
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 60, HEIGHT // 2 - 60, 120, 60), 2)

        screen.blit(start_text, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
        screen.blit(quit_text, (WIDTH // 2 - 50, HEIGHT // 2 + 30))

    # Screen refresh
    pygame.display.flip()

    # FPS installation
    clock.tick(FPS)
