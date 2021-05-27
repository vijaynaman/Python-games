import pygame
import random
import os
pygame.init()
def play(song):
    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

window=pygame.display.set_mode((600,600))
pygame.display.set_caption("snakes game")
font=pygame.font.SysFont(None,40)
def prtscore(text,color,x,y):
    screen_text=font.render(text,True,color)
    window.blit(screen_text,[x,y])
def plotsnake(window,white,snk_lst,length,breadth):
    for x,y in snk_lst:
        pygame.draw.rect(window, white, [x, y, length, breadth])
def welocome():
    black = (0, 0, 0)
    red = (255, 0, 0)
    image=pygame.image.load("bgimg.jpeg")
    image=pygame.transform.scale(image,(600,600)).convert_alpha()
    clock = pygame.time.Clock()
    fps = 60
    exit_wel=False
    window.fill(black)
    window.blit(image,(0,0))
    prtscore("welcome to snakes",red,150,250)
    prtscore("press enter to play",red,149,280)
    while not exit_wel:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_wel = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
        pygame.display.update()
        clock.tick(fps)
def gameloop():
    close_game = False
    game_over = False
    snk_lst = []
    snakelen = 1
    white = (255, 255, 255)
    red = (255, 0, 0)
    black = (0, 155, 0)
    green = (0, 0, 0)
    snake_x = 150
    food_x = random.randrange(20, 580, 5)
    food_y = random.randrange(20, 580, 5)
    snake_y = 150
    length = 15
    breadth = 15
    velocity_x = 0
    velocity_y = 0
    n = 2
    score = 0
    clock = pygame.time.Clock()
    fps = 60
    image = pygame.image.load("gamebg.jpg")
    image = pygame.transform.scale(image, (600, 600)).convert_alpha()
    image2 = pygame.image.load("gameover.jpg")
    image2 = pygame.transform.scale(image, (600, 600)).convert_alpha()
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt","r") as f:
        highscore=f.read()
    while not close_game:
        if game_over:
            with open("highscore.txt", "w") as f:

                f.write(str(highscore))
            window.fill(green)
            prtscore("Game Over!!! ", red, 200, 200)
            prtscore("press enter to play again", red, 150, 250)
            prtscore(f"score:{score}", red, 230, 275)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welocome()
                if event.type == pygame.QUIT:
                    close_game = True
                    pygame.quit()
                    quit()
        else:
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    close_game=True
                if event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        play("click1.mp3")
                        velocity_x=n
                        velocity_y=0
                    if event.key == pygame.K_LEFT:
                        play("click1.mp3")
                        velocity_x= -n
                        velocity_y = 0
                    if event.key == pygame.K_DOWN:
                        play("click2.mp3")
                        velocity_x = 0
                        velocity_y = n
                    if event.key == pygame.K_UP:
                        play("click2.mp3")
                        velocity_x = 0
                        velocity_y = -n
                    if event.key == pygame.K_q:
                        score+=5
                    if event.key == pygame.K_z:
                        n-=1
            if abs(food_x-snake_x)<=5 and abs(food_y-snake_y)<=5:
                play("eat.mp3")
                score+=1
                n+=1
                food_x = random.randrange(20, 580,5)
                food_y = random.randrange(20, 580,5)
                snakelen+=5
            snake_x+=velocity_x
            snake_y +=velocity_y
            window.fill(black)
            window.blit(image,(0,0))
            prtscore(f"score:{score}",red,0,0)
            prtscore(f"highscore:{highscore}", red, 400, 0)
            if score>int(highscore):
                highscore=score
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_lst.append(head)
            if len(snk_lst)>snakelen:
                del snk_lst[0]
            if head in snk_lst[:-1]:
                play("hit.mp3")
                game_over=True
            plotsnake(window,green,snk_lst,length,breadth)
            pygame.draw.rect(window,red,[food_x,food_y,15,15])
            if snake_x <= 0 or snake_x >= 600 or snake_y <= 0 or snake_y >= 600:
                play("hit.mp3")
                game_over = True
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()
welocome()
