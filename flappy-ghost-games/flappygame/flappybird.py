import random
import sys
import pygame
from pygame.locals import *
FPS=32
SCREENWIDTH=450
SCREENHEIGHT=700
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("flappy ghost ")
GROUNDY = SCREENHEIGHT*0.8
GAME_IMAGES = {}
GAME_MUSIC = {}
PLAYER=f"items/images/mouth.png"
BACKGROUND="items/images/background.png"
PIPE="items/images/pipe.png"
def play(song):
    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
def welcomescreen():
    welcomex=0
    welcomey=0
    playerx=int(SCREENWIDTH-270)
    playery=int(SCREENHEIGHT-480)
    while True:
        screen.blit(pygame.transform.scale(GAME_IMAGES["message"],(SCREENWIDTH,SCREENHEIGHT)),(welcomex,welcomey))
        screen.blit(GAME_IMAGES["player"],(playerx,playery))
        pygame.display.update()
        fpsclock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT or(event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                game()
                return
def gmover(score):
    while True:
        screen.blit(pygame.transform.scale(GAME_IMAGES["gameover"], (SCREENWIDTH, SCREENHEIGHT)), (0, 0))
        prt(f"your score:{score}",(255,0,0),int(SCREENWIDTH/3),0)
        prt("press enter to play again",(255,0,0),int(SCREENWIDTH/7),int(SCREENHEIGHT/2))
        pygame.display.update()
        fpsclock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_RETURN):
                welcomescreen()
                return
def game():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENHEIGHT/2)
    newpipe1= getrandompipe()
    newpipe2= getrandompipe()
    upperpipe = [
        {'x' : SCREENWIDTH+200,'y': newpipe1[0]["y"]},
        {'x': SCREENWIDTH+200+SCREENWIDTH/2,'y': newpipe2[0]["y"]},
                ]
    lowerpipe = [
        {"x":SCREENWIDTH+200,"y":newpipe1[1]["y"]},
        {"x":SCREENWIDTH+200+SCREENWIDTH/2,"y":newpipe2[1]["y"]},
                ]
    gh1=[
        {"x":int(SCREENWIDTH*1.5),"y":int(GROUNDY)},]
    gh2=[{"x":SCREENWIDTH*2,"y":int(GROUNDY)},
        ]
    ghspeed = -1
    pipevel = -4
    playervely=-9
    playermaxvel=10
    playerminvel=-8
    playeraccy=1
    playerflapaccv=-8
    playerflapped=False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or(event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                if playery>0:
                    playervely = playerflapaccv
                    playerflapped == True
                    play(GAME_MUSIC["wing"])
        crashtest = iscollide(playerx,playery,upperpipe,lowerpipe)
        if crashtest:
            gmover(score)
            return
        playermidpos= playerx+GAME_IMAGES["player"].get_width()/2
        for pipe in upperpipe:
            pipemidpos = pipe["x"] + GAME_IMAGES["pipe"][0].get_width()/2
            if pipemidpos<= playermidpos<pipemidpos+4:
                score+=1
                print(f"your score is {score}")
                play(GAME_MUSIC["point"])
        if playervely<playermaxvel and not playerflapped:
            playervely+=playeraccy
        if playerflapped:
            playerflapped = False
        playerheight=GAME_IMAGES["player"].get_height()
        playery=playery+min(playervely,GROUNDY-playery-playerheight)

        for g in zip(gh1,gh2):
            g[0]["x"]+=ghspeed
            g[1]["x"]+=ghspeed

        if 0 == gh1[0]["x"]:
            gh1.append({"x":1.5*SCREENWIDTH,"y":int(GROUNDY)})
            gh2.append({"x":2*SCREENWIDTH,"y":int(GROUNDY)})
        if gh1[0]["x"]<-GAME_IMAGES["ghosts"][0].get_width():
            gh1.pop(0)
        if gh2[0]["x"]<-GAME_IMAGES["ghosts"][1].get_width():
            gh2.pop(0)
        for upper,lower in zip(upperpipe,lowerpipe):
            upper["x"]+=pipevel
            lower["x"]+=pipevel
        if 0 < upperpipe[0]["x"] < 5:
            newpipe=getrandompipe()
            upperpipe.append(newpipe[0])
            lowerpipe.append(newpipe[1])
        if upperpipe[0]["x"]<-GAME_IMAGES["pipe"][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)
        screen.blit(GAME_IMAGES["background"], (0, 0))
        for upper,lower in zip(upperpipe,lowerpipe):
            screen.blit(GAME_IMAGES["pipe"][0], (int(upper["x"]), int(upper["y"])))
            screen.blit(GAME_IMAGES["pipe"][1], (int(lower["x"]), int(lower["y"])))
        screen.blit(GAME_IMAGES["base"], (0, int(GROUNDY)))
        for g in zip(gh1,gh2):
            screen.blit(GAME_IMAGES["ghosts"][0], (int(g[0]["x"]), int(g[0]["y"])))
            screen.blit(GAME_IMAGES["ghosts"][1], (int(g[1]["x"]), int(g[1]["y"])))
        screen.blit(GAME_IMAGES["player"], (int(playerx), int(playery)))
        mydigit = [ int(x) for x in list(str(score))]
        width=0
        for digit in mydigit:
            width+=GAME_IMAGES["numbers"][digit].get_width()
        xoffset = (SCREENWIDTH-width)/2
        for digit in mydigit:
            screen.blit(GAME_IMAGES["numbers"][digit],(int(xoffset),int(SCREENHEIGHT*0.12)))
            xoffset += GAME_IMAGES["numbers"][digit].get_width()
        pygame.display.update()
        fpsclock.tick(FPS)
def iscollide(playerx,playery,upperpipe,lowerpipe):
    if playery> GROUNDY-62 or playery < 0:
        play(GAME_MUSIC["swoosh"])
        return True
    for pipe in upperpipe:
        pipeheight=GAME_IMAGES["pipe"][0].get_height()
        if (playery<pipeheight+pipe["y"] and abs(playerx-pipe["x"]) < GAME_IMAGES["pipe"][0].get_width()-50):
            play(GAME_MUSIC["swoosh"])
            return True
    for pipe in lowerpipe:
        if (playery+GAME_IMAGES["player"].get_height()>pipe["y"]+20 and abs(playerx-pipe["x"])< GAME_IMAGES["pipe"][0].get_width()-50):
            play(GAME_MUSIC["swoosh"])
            return True
def getrandompipe():
    '''genereate  two pipe 1 rotated and 1 straight pipe'''
    pipeheight=GAME_IMAGES["pipe"][0].get_height()
    offset=int(SCREENHEIGHT/2.5)
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_IMAGES["base"].get_height()-1.3*offset))
    pipex=SCREENWIDTH+10
    y1 = pipeheight-y2+offset*0.45
    pipe=[{"x":pipex,"y":-y1},{"x":pipex,"y":y2}]
    return pipe
def prt(text,color,x,y):
    screen_text=font.render(text,True,color)
    screen.blit(screen_text,[x,y])
if __name__ == '__main__':
    pygame.init()
    fpsclock=pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    pygame.display.set_caption("Flappy Ghost")
    GAME_IMAGES["numbers"]=(pygame.transform.scale(pygame.image.load("items/images/0.png"),(40,40)).convert_alpha(),
                            pygame.transform.scale(pygame.image.load("items/images/1.png"),(40,40)).convert_alpha(),
                            pygame.transform.scale(pygame.image.load("items/images/2.png"),(40,40)).convert_alpha(),
                            pygame.transform.scale(pygame.image.load("items/images/3.png"),(40,40)).convert_alpha(),
                            pygame.transform.scale(pygame.image.load("items/images/4.png"),(40,40)).convert_alpha(),
                            pygame.transform.scale(pygame.image.load("items/images/5.png"),(40,40)).convert_alpha(),
                            pygame.transform.scale(pygame.image.load("items/images/6.png"),(40,40)).convert_alpha(),
                            pygame.transform.scale(pygame.image.load("items/images/7.png"),(40,40)).convert_alpha(),
                            pygame.transform.scale(pygame.image.load("items/images/8.png"),(40,40)).convert_alpha(),
                            pygame.transform.scale(pygame.image.load("items/images/9.png"),(40,40)).convert_alpha())
    GAME_IMAGES["message"] =pygame.image.load("items/images/welcome.jpg").convert_alpha()
    GAME_IMAGES["gameover"] =pygame.image.load("items/images/gameover.jpg").convert_alpha()
    GAME_IMAGES["ghosts"] =(pygame.transform.scale(pygame.image.load("items/images/ghost.png"),(int(SCREENWIDTH/3),int(SCREENHEIGHT-SCREENHEIGHT*0.8))).convert_alpha(),
                             pygame.transform.scale(pygame.image.load("items/images/ghost1.png"),(int(SCREENWIDTH/3),int(SCREENHEIGHT-SCREENHEIGHT*0.8))).convert_alpha())
    GAME_IMAGES["base"] =pygame.transform.scale(pygame.image.load("items/images/base.jpg"),(SCREENWIDTH,int(SCREENHEIGHT-SCREENHEIGHT*0.8))).convert_alpha()
    GAME_IMAGES["background"] =pygame.transform.scale(pygame.image.load(BACKGROUND),(SCREENWIDTH,int(SCREENHEIGHT*0.8))).convert_alpha()
    GAME_IMAGES["player"] =pygame.transform.scale(pygame.image.load(PLAYER),(60,60)).convert_alpha()
    GAME_IMAGES["pipe"] =(pygame.transform.scale(pygame.transform.rotate(pygame.image.load(PIPE),180),(int(SCREENWIDTH/5),int(SCREENHEIGHT/1.3))).convert_alpha(),
                          pygame.transform.scale(pygame.image.load(PIPE),(int(SCREENWIDTH/5),int(SCREENHEIGHT/1.3))).convert_alpha())

    GAME_MUSIC["hit"]="items/music/hit.mp3"
    GAME_MUSIC["point"]="items/music/point.mp3"
    GAME_MUSIC["swoosh"]="items/music/eat.mp3"
    GAME_MUSIC["wing"]="items/music/click1.mp3"

    welcomescreen()



