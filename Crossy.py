
import pygame as p
import time

#Chicken Class
class Chicken(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 50
        self.y = HEIGHT / 2
        self.vel = 4
        self.width = 100
        self.height = 50


        self.chicken1 = p.image.load('Chicken1.png')
        self.chicken2 = p.image.load('Chicken2.png')
        self.chicken3 = p.image.load('Chicken3.png')
        self.chicken4 = p.image.load('Chicken4.png')
        self.chicken1 = p.transform.scale(self.chicken1, (self.width, self.height))
        self.chicken2 = p.transform.scale(self.chicken2, (self.width, self.height))
        self.chicken3 = p.transform.scale(self.chicken3, (self.width, self.height))
        self.chicken4 = p.transform.scale(self.chicken4, (self.width, self.height))
        self.image = self.chicken1
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        self.movement()
        self.correction()
        self.getCollision()
        self.rect.center = (self.x, self.y)
    
    def movement(self):
        keys = p.key.get_pressed()
        if keys[p.K_RIGHT]:
            self.x += self.vel
            self.image = self.chicken1
           

        elif keys[p.K_LEFT]:
            self.x -= self.vel
            self.image = self.chicken2
            
        if keys[p.K_UP]:
            self.y -= self.vel
            self.image = self.chicken3
            
        elif keys[p.K_DOWN]:
            self.y += self.vel
            self.image = self.chicken4
            
    def correction(self):
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2

        elif self.x + self.width / 2 > WIDTH:
            self.x = WIDTH - self.width / 2

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2

        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2

    def getCollision(self):
        carCheck = p.sprite.spritecollide(self, carGroup, False, p.sprite.collide_mask)
        if carCheck:
            Explode.explode(self.x, self.y)

#Car Class
class Car(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        if number == 1:
            self.x = 190
            self.image = p.image.load('SlowCar.png')
            self.vel = -4

        else:
            self.x = 460
            self.image = p.image.load('FastCar.png')
            self.vel = 5

        self.y = HEIGHT / 2
        self.width = 100
        self.height = 150
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        self.movement()
        self.rect.center = (self.x, self.y)

    def movement(self):
        self.y += self.vel

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2
            self.vel *= -1

        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2
            self.vel *= -1

#Screen Class
class Screen(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img1 = p.image.load('Scene.png')
        self.img2 = p.image.load('Winner.png')
        self.img3 = p.image.load('Loser.png')

        self.img1 = p.transform.scale(self.img1, (WIDTH, HEIGHT))
        self.img2 = p.transform.scale(self.img2, (WIDTH, HEIGHT))
        self.img3 = p.transform.scale(self.img3, (WIDTH, HEIGHT))

        self.image = self.img1
        self.x = 0
        self.y = 0

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = (self.x, self.y)

#Food Class
class Food(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number

        if self.number == 1:
            self.image = p.image.load('Seeds2.png')
            self.visible = False
            self.x = 50

        else:
            self.image = p.image.load('Seeds1.png')
            self.visible = True
            self.x = 580

        self.y = HEIGHT / 2
        self.image = p.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        if self.visible:
            self.collision()
            self.rect.center = (self.x, self.y)

    def collision(self):
        global SCORE, chicken

        gotFood = p.sprite.spritecollide(self, chickenGroup, False, p.sprite.collide_mask)
        if gotFood:
            self.visible = False

            if self.number == 1:
                Seeds1.visible = True
                if SCORE < 6:
                    SwitchLevel()

                else:
                    chickenGroup.empty()
                    DeleteOtherItems()
                    EndScreen(1)

            else:
                Seeds2.visible = True
                if SCORE < 6:
                    SwitchLevel()

                else:
                    chickenGroup.empty()
                    DeleteOtherItems()
                    EndScreen(1)
                

#Explosion Class
class Explosion(object):
    def __init__(self):
        self.cost = 1
        self.width = 140
        self.height = 140  
        self.image = p.image.load('Explosion'+ str(self.cost) + '.png')
        self.image = p.transform.scale(self.image, (self.width, self.height))


    def explode(self, x, y):
        x = x - self.width // 2
        y = y - self.height // 2
        DeleteChicken()

        while self.cost < 6:
            self.image = p.image.load('Explosion'+ str(self.cost) + '.png')
            self.image = p.transform.scale(self.image, (self.width, self.height))
            win.blit(self.image, (x, y))
            p.display.update()

            self.cost += 1
            time.sleep(0.3)

        DeleteOtherItems()
        EndScreen(0)

#Game Functions
def scoreDisplay():
    global gameOn
    if gameOn:
        scoreText = scoreFont.render('Level '+ str(SCORE) + ' / 6', True, (0, 0, 0))
        win.blit(scoreText, (255, 10))


def getFood():
    for f in Food:
        if not f.visible:
            f.kill()

        else:
            if not f.alive():
                foodGroup.add(f)


def SwitchLevel():
    global SCORE

    if slowCar.vel < 0:
        slowCar.vel -= 1

    else:
        slowCar.vel += 1

    if fastCar.vel < 0:
        fastCar.vel -= 1

    else:
        fastCar.vel += 1

    SCORE += 1


def DeleteChicken():
    global chicken

    chicken.kill()
    screenGroup.draw(win)
    carGroup.draw(win)
    foodGroup.draw(win)

    screenGroup.update()
    carGroup.update()
    foodGroup.update()

    p.display.update()


def DeleteOtherItems():
    carGroup.empty()
    foodGroup.empty()
    Food.clear()


def EndScreen(n):
    global gameOn

    gameOn = False

    if n == 0:
        s.image = s.img3

    elif n == 1:
        s.image = s.img2

#Global Game Methods
WIDTH = 640
HEIGHT = 480

p.init()

win = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('Crossy Road')
clock = p.time.Clock()

SCORE = 0
scoreFont = p.font.SysFont('Arial', 30, True)

s = Screen()
screenGroup = p.sprite.Group()
screenGroup.add(s)

chicken = Chicken()
chickenGroup = p.sprite.Group()
chickenGroup.add(chicken)

slowCar = Car(1)
fastCar = Car(2)
carGroup = p.sprite.Group()
carGroup.add(slowCar, fastCar)

Seeds2 = Food(1)
Seeds1 = Food(2)
foodGroup = p.sprite.Group()
foodGroup.add(Seeds2, Seeds1)
Food = [Seeds2, Seeds1]

Explode = Explosion()

gameOn = True
run = True
while run:
    clock.tick(60)
    for e in p.event.get():
        if e.type == p.QUIT:
            run = False

    screenGroup.draw(win)

    scoreDisplay()
    getFood()

    carGroup.draw(win)
    chickenGroup.draw(win)
    foodGroup.draw(win)

    carGroup.update()
    chickenGroup.update()
    foodGroup.update()

    screenGroup.update()

    p.display.update()

p.quit()



