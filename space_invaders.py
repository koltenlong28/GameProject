import pygame
import random
import sys
import os

os.system('clear')

width,height = 800, 600
playersize = 50
enmysize = 50
bulletsize = 15
fps = 60
bulletspeed = 10
white = (255, 255, 255)
black = (0, 0, 0)


backgroundimagepath = os.path.join(os.path.dirname(__file__), 'background.jpg')

def initializepygame():
    pygame.init()
    return pygame.display.set_mode((width, height)), pygame.font.SysFont(None, 48)

backgroundimage = pygame.image.load(backgroundimagepath)
backgroundimage = pygame.transform.scale(backgroundimage, (width, height))

shipimagepath = os.path.join(os.path.dirname(__file__), 'ship.png')
alienimagepath = os.path.join(os.path.dirname(__file__), 'alien.png')
lazerimagepath = os.path.join(os.path.dirname(__file__), 'lazer.png')

shipimage = pygame.image.load(shipimagepath)
alienimage = pygame.image.load(alienimagepath)
lazerimage = pygame.image.load(lazerimagepath)

shipimage = pygame.transform.scale(shipimage, (playersize, playersize))
alienimage = pygame.transform.scale(alienimage, (enmysize, enmysize))
lazerimage = pygame.transform.scale(lazerimage, (bulletsize, bulletsize))

class Player:
    def __init__(self):
        self.rect = pygame.Rect(width // 2 - playersize // 2, height - playersize - 10, playersize, playersize)
        self.speed = 5

class Game:
    def __init__(self):
        self.screen, self.font = initializepygame()
        self.player = Player()
        self.enemies = []
        self.enmyspeed = 0.7
        self.enmyspawnrate = 22
        self.bullets = []
        self.shootcooldown = 0
        self.gameover = False
        self.score = 0
        self.gamerunning = False



    def drawbackground(self):
        self.screen.blit(backgroundimage, (0, 0))

    def drawplayer(self):
        self.screen.blit(shipimage, self.player.rect)

    def drawenemies(self):
        for enmy in self.enemies:
            self.screen.blit(alienimage, enmy)

    def drawbullets(self):
        for bullet in self.bullets:
            self.screen.blit(lazerimage, bullet)

    def displaygameover(self):
        gameovertext = self.font.render("game over", True, white)
        self.screen.blit(gameovertext, (width // 2 - 100, height // 2 - 25))

    def displayhighestscore(self, username):
        with open('playerdata.dat', 'r') as file:
            for line in file:
                storedusername, password, storedscore = line.strip().split(',')
                if storedusername == username:
                    highestscoretext = self.font.render(f"highest score: {storedscore}", True, white)
                    self.screen.blit(highestscoretext, (width // 2 - 120, height // 2 + 25))

    def displaytopscores(self):
        topscorestext = self.font.render("top 5 players", True, white)
        self.screen.blit(topscorestext, (width // 2 - 100, height // 2 + 75))

        with open('playerdata.dat', 'r') as file:
            scores = [line.strip().split(',') for line in file]
            sortedscores = sorted(scores, key=lambda x: int(x[2]), reverse=True)
            
            for i, entry in enumerate(sortedscores[:5]):
                scoretext = self.font.render(f"{entry[0]}: {entry[2]}", True, white)
                self.screen.blit(scoretext, (width // 2 - 100, height // 2 + 125 + i * 25))

    def updatescore(self, username):
        userdata = []

        with open('playerdata.dat', 'r') as file:
            for line in file:
                storedusername, password, storedscore = line.strip().split(',')
                print(storedscore)
                storedscore = int(storedscore)
                if storedusername == username:
                    storedscore = max(storedscore, self.score)
                userdata.append(f"{storedusername},{password},{storedscore}\n")

        with open('playerdata.dat', 'w') as file:
            file.writelines(userdata)

    def minimizewindow(self):
        pygame.display.iconify()

    def login(self):
        username = input("enter username: ")
        password = input("enter password: ")

        with open('playerdata.dat', 'r') as file:
            for line in file:
                storedusername, storedpassword, score = line.strip().split(',')
                if username == storedusername:
                    if password == storedpassword:
                        print(f"login success. hello {username}. your highest score is {score}")
                        self.minimizewindow()
                        return True, username, int(score)
                    else:
                        print("incorrect password.")
                        return False, "", 0

        print("username not found. do you want to create a new account? (y/n)")
        choice = input().lower()

        if choice == 'y':
            self.createaccount(username, password)
            return True, username, 0
        else:
            print("login canceled.")
            return False, "", 0

    def createaccount(self, username, password):
        score = 0
        with open('playerdata.dat', 'a') as file:
            file.write(f"{username},{password},{score}\n")

        print("account created successfully!")

    def mainloop(self, username):
        self.gamerunning = True

        while self.gamerunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()




            if not self.gameover:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and self.player.rect.left > 0:
                    self.player.rect.x -= self.player.speed
                if keys[pygame.K_RIGHT] and self.player.rect.right < width:
                    self.player.rect.x += self.player.speed

                if keys[pygame.K_SPACE] and self.shootcooldown == 0:
                    bullet = pygame.Rect(
                        self.player.rect.centerx - bulletsize // 2,
                        self.player.rect.y - bulletsize,
                        bulletsize,
                        bulletsize
                    )
                    self.bullets.append(bullet)
                    self.shootcooldown = 15

                if self.shootcooldown > 0:
                    self.shootcooldown -= 1

                if random.randint(1, self.enmyspawnrate) == 1:
                    enmy = pygame.Rect(random.randint(0, width - enmysize), 0, enmysize, enmysize)
                    self.enemies.append(enmy)

                for enmy in self.enemies:
                    enmy.y += self.enmyspeed
                    if enmy.y > height:
                        self.gameover = True

                for bullet in self.bullets:
                    bullet.y -= bulletspeed
                    if bullet.y < 0:
                        self.bullets.remove(bullet)

                for bullet in self.bullets:
                    for enmy in self.enemies:
                        if bullet.colliderect(enmy):
                            self.bullets.remove(bullet)
                            self.enemies.remove(enmy)
                            self.score += 100

                for enmy in self.enemies:
                    if self.player.rect.colliderect(enmy):
                        self.gameover = True

                self.drawbackground()
                self.drawplayer()
                self.drawenemies()
                self.drawbullets()

                pygame.display.flip()

                pygame.time.Clock().tick(fps)
            else:
                self.screen.fill(black)
                self.updatescore(username)
                self.displaygameover()
                self.displayhighestscore(username)
                self.displaytopscores()
                pygame.display.flip()
                pygame.time.delay(5000) 
                 

                self.gamerunning = False

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gameinstance = Game()
    loggedin, username, _ = gameinstance.login()

    if loggedin:
        gameinstance.mainloop(username)
