import pygame
import random

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Visually Attractive Ping Pong Game")

# Colors

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Paddle

paddle_width = 100
paddle_height = 20
paddle_x = width // 2 - paddle_width // 2
ai_paddle_x = width //2 -paddle_width // 2
paddle_y = height - paddle_height - 10
paddle_speed = 8

# AI

ai_difficulty = 1
ai_paddle_speeds = [4, 6, 8]

# Ball

ball_size = 20
ball_x = width // 2 - ball_size // 2
ball_y = height // 2 - ball_size // 2
ball_speed_x = 5
ball_speed_y = 5

# Loading fonts
font = pygame.font.Font(None, 36)

# Game setup
choosing_difficulty = True
choosing_name = True
player_name = ""
player_score = 0
ai_score = 0
leaderboard = []
    
# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if choosing_name:
                player_name += event.unicode
            elif choosing_difficulty:
                if event.unicode in ("1", "2", "3"):
                    ai_difficulty = int(event.unicode)
                    choosing_difficulty = False
                
    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
        
    if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
        paddle_x += paddle_speed
        
    # AI opponent movement
    if ai_difficulty > 0:           # Easy AI
        target_x = ball_x - paddle_width // 2
        if ai_difficulty == 2:      # Medium AI
            target_x = ball_x - paddle_width // 4
        elif ai_difficulty == 3:    # Hard AI
            target_x = ball_x
            
        if ai_paddle_x < target_x:
            ai_paddle_x += ai_paddle_speeds[ai_difficulty - 1]
        elif ai_paddle_x > target_x:
            ai_paddle_x -= ai_paddle_speeds[ai_difficulty - 1]
        
    # Moving the ball
    
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Ball collision with Walls
    if ball_x <= 0 or ball_x >= width - ball_size:
        ball_speed_x = -ball_speed_x
        
    # Ball collision with paddle
    
    if (
        ball_y + ball_size >= paddle_y
        and ball_x + ball_size >= paddle_x
        and ball_x <= paddle_x + paddle_width
    ) or (
        ball_y <= paddle_height
        and ball_x + ball_size >= ai_paddle_x
        and ball_x <= ai_paddle_x + paddle_width
    ):
        ball_speed_y = -ball_speed_y
        
    # Ball out of bounds (reset)
    if ball_y >= height:
        ball_x = width // 2 - ball_size // 2
        ball_y = height // 2 - ball_size // 2
        ball_speed_x = random.choice([-5, 5])
        ball_speed_y = random.choice([-5, 5])
        leaderboard.append({"name":player_name, "score":player_score})
    elif ball_y <= 0:
        ball_x = width // 2 - ball_size // 2
        ball_y = height // 2 - ball_size // 2
        ball_speed_x = random.choice([-5, 5])
        ball_speed_y = random.choice([-5, 5])
        leaderboard.append({"name":player_name, "score":player_score})
    
        
    # Clear the screen
    screen.fill(black)
    
    # Draw paddle
    pygame.draw.rect(screen, blue, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, red, (ai_paddle_x, 0, paddle_width, paddle_height))

    # Draw ball
    pygame.draw.ellipse(screen, red, (ball_x, ball_y, ball_size, ball_size))
    
    # Draw scores
    player_score_text = font.render(f" {player_name}: {player_score}", True, white)
    ai_score_text = font.render(f" AI: {ai_score}", True, white)
    screen.blit(player_score_text, (10, 10))
    screen.blit(ai_score_text, (width - 100, 10))
    
    pygame.display.flip()
    clock.tick(60)

# Display leaderboard after the game
leaderboard = [
    {"Name: ":player_name, "Score: ": player_score},
    {"Name: ":"AI", "Score: ": ai_score},
]

leaderboard.sort(key=lambda x: x["score"], reverse=True)

screen.fill(black)
leaderboard_text = font.render("Leaderboard", True, white)
screen.blit(leaderboard_text, (width // 2 - 80, 50))

for idx, entry in enumerate(leaderboard):
    leaderboard_entry = f"{idx + 1}. {entry['name']}: {entry['score']}"
    entry_text = font.render(leaderboard_entry, True, white)
    screen.blit(entry_text, (width // 2 - 80, 100 - idx * 40))
    
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
