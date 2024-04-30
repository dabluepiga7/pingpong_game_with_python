import pygame
import random
import json

# Initialize pygame
pygame.init()

# Set up display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Player vs AI Ping Pong Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Paddles
paddle_width = 100
paddle_height = 20
player_paddle_x = width // 2 - paddle_width // 2
ai_paddle_x = width // 2 - paddle_width // 2
paddle_y = height - paddle_height - 10
paddle_speed = 8

# AI
ai_difficulty = 1
ai_difficulty_names = {1: "Easy", 2: "Medium", 3: "Hard"}
ai_paddle_speeds = [4, 6, 8]

# Ball
ball_size = 20
ball_x = width // 2 - ball_size // 2
ball_y = height // 2 - ball_size // 2
ball_speed_x = 5
ball_speed_y = 5

# Load fonts
font = pygame.font.Font(None, 36)

# Input variables
player_name = ""
choosing_name = False
choosing_difficulty = True

# Game setup
player_score = 0
ai_score = 0

# Leaderboard
leaderboard = []

# Timer
game_start_ticks = pygame.time.get_ticks()
game_duration = 60 * 1000  # 60 seconds in milliseconds

# Load leaderboard data from a JSON file (if it exists)
try:
    with open("leaderboard.json", "r") as file:
        leaderboard = json.load(file)
except FileNotFoundError:
    leaderboard = []

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    current_ticks = pygame.time.get_ticks()
    elapsed_time = current_ticks - game_start_ticks

    if elapsed_time >= game_duration:
        choosing_name = True
        choosing_difficulty = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if choosing_difficulty:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 200 <= mouse_x <= 300 and 300 <= mouse_y <= 340:
                    ai_difficulty = 1
                    choosing_difficulty = False
                elif 350 <= mouse_x <= 450 and 300 <= mouse_y <= 340:
                    ai_difficulty = 2
                    choosing_difficulty = False
                elif 500 <= mouse_x <= 600 and 300 <= mouse_y <= 340:
                    ai_difficulty = 3
                    choosing_difficulty = False
            elif choosing_name:
                if event.unicode == '\r' and player_name:
                    choosing_name = False

                elif event.unicode == '\b':
                    player_name = player_name[:-1]
                elif event.unicode.isalnum():
                    player_name += event.unicode
            else:
                if 350 <= pygame.mouse.get_pos()[0] <= 450 and 300 <= pygame.mouse.get_pos()[1] <= 340:
                    player_name = ""
                    player_score = 0
                    ai_score = 0
                    game_start_ticks = pygame.time.get_ticks()
                    ball_x = width // 2 - ball_size // 2
                    ball_y = height // 2 - ball_size // 2
                    ball_speed_x = random.choice([-5, 5])
                    ball_speed_y = random.choice([-5, 5])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_paddle_x > 0:
        player_paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and player_paddle_x < width - paddle_width:
        player_paddle_x += paddle_speed

    # AI opponent movement
    if ai_difficulty > 0:
        target_x = ball_x - paddle_width // 2
        if ai_difficulty == 2:  # Medium AI
            target_x = ball_x - paddle_width // 4
        elif ai_difficulty == 3:  # Hard AI
            target_x = ball_x

        if ai_paddle_x < target_x:
            ai_paddle_x += ai_paddle_speeds[ai_difficulty - 1]
        elif ai_paddle_x > target_x:
            ai_paddle_x -= ai_paddle_speeds[ai_difficulty - 1]

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with walls
    if ball_x <= 0 or ball_x >= width - ball_size:
        ball_speed_x = -ball_speed_x

    # Ball collision with paddles
    if (
        ball_y + ball_size >= paddle_y
        and ball_x + ball_size >= player_paddle_x
        and ball_x <= player_paddle_x + paddle_width
    ) or (
        ball_y <= paddle_height
        and ball_x + ball_size >= ai_paddle_x
        and ball_x <= ai_paddle_x + paddle_width
    ):
        ball_speed_y = -ball_speed_y

    # Ball out of bounds
    if ball_y >= height:
        ball_x = width // 2 - ball_size // 2
        ball_y = height // 2 - ball_size // 2
        ball_speed_x = random.choice([-5, 5])
        ball_speed_y = random.choice([-5, 5])
        if player_name:
            player_score += 1
            leaderboard.append({"name": player_name, "score": player_score, "difficulty": ai_difficulty_names[ai_difficulty]})
    elif ball_y <= 0:
        ball_x = width // 2 - ball_size // 2
        ball_y = height // 2 - ball_size // 2
        ball_speed_x = random.choice([-5, 5])
        ball_speed_y = random.choice([-5, 5])
        ai_score += 1
        leaderboard.append({"name": "AI", "score": ai_score, "difficulty": ai_difficulty_names[ai_difficulty]})

    # Clear the screen
    screen.fill(black)

    if choosing_difficulty:
        choose_difficulty_text = font.render("Choose AI Difficulty:", True, white)
        easy_button_text = font.render("Easy", True, white)
        medium_button_text = font.render("Medium", True, white)
        hard_button_text = font.render("Hard", True, white)
        screen.blit(choose_difficulty_text, (width // 2 - 130, 150))
        pygame.draw.rect(screen, white, (200, 300, 100, 40))
        pygame.draw.rect(screen, white, (350, 300, 100, 40))
        pygame.draw.rect(screen, white, (500, 300, 100, 40))
        screen.blit(easy_button_text, (220, 305))
        screen.blit(medium_button_text, (365, 305))
        screen.blit(hard_button_text, (520, 305))
    elif choosing_name:
        input_area_text = font.render("Enter Your Name:", True, white)
        name_text = font.render(player_name, True, white)
        screen.blit(input_area_text, (width // 2 - 100, height // 2 - 50))
        screen.blit(name_text, (width // 2 - 50, height // 2))
    else:
        # Draw paddles
        pygame.draw.rect(screen, blue, (player_paddle_x, paddle_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, red, (ai_paddle_x, 0, paddle_width, paddle_height))

        # Draw ball
        pygame.draw.ellipse(screen, white, (ball_x, ball_y, ball_size, ball_size))

        # Draw scores
        player_score_text = font.render(f"{player_name}: {player_score}", True, white)
        ai_score_text = font.render(f"AI: {ai_score}", True, white)
        screen.blit(player_score_text, (10, 10))
        screen.blit(ai_score_text, (width - 100, 10))

        # Draw timer
        remaining_time = max((game_duration - elapsed_time) // 1000, 0)
        timer_text = font.render(f"Time: {remaining_time}", True, white)
        screen.blit(timer_text, (width // 2 - 40, 10))

        # Draw play button
        play_button_text = font.render("PLAY", True, white)
        pygame.draw.rect(screen, white, (350, 300, 100, 40))
        screen.blit(play_button_text, (365, 305))

    pygame.display.flip()
    clock.tick(60)

# Display "Game Over" and leaderboard
screen.fill(black)
game_over_text = font.render("Game Over", True, white)
screen.blit(game_over_text, (width // 2 - 60, height // 2 - 20))
pygame.display.flip()

pygame.time.wait(3000)  # Show "Game Over" for 3 seconds

leaderboard.sort(key=lambda x: x["score"], reverse=True)

# Save leaderboard data to a JSON file
with open("leaderboard.json", "w") as file:
    json.dump(leaderboard, file)

screen.fill(black)
leaderboard_text = font.render("Leaderboard", True, white)
screen.blit(leaderboard_text, (width // 2 - 80, 50))

for idx, entry in enumerate(leaderboard):
    leaderboard_entry = f"{idx + 1}. {entry['name']} ({entry['difficulty']}): {entry['score']}"
    entry_text = font.render(leaderboard_entry, True, white)
    screen.blit(entry_text, (width // 2 - 120, 100 + idx * 40))

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
