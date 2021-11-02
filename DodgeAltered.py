import pygame                               # Imports pygame and other libraries
import random

# Define Classes (sprites) here

#pygame.init()                               # Pygame is initialised (starts running)

WIDTH = 700
HEIGHT = 500

BLACK    = (   0,   0,   0)                 # Define some colors using rgb values.  These can be
WHITE    = ( 255, 255, 255)                 # used throughout the game instead of using rgb values.
RED      = ( 255, 0, 0)
GREEN    = (0, 255, 0)
BLUE     = (0, 0, 255)

#screen = pygame.display.set_mode([WIDTH,HEIGHT])
#pygame.display.set_caption("Mr van's Dodge Game")         # Name your window
# Basic Pygame Structure

# *** Define Classes Here ***

class FallingObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.timeCreated = pygame.time.get_ticks()
        self.image = pygame.Surface([30,30])
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0,HEIGHT)

    def setImage(self, graphicSelected):
        fallingObjectImage = pygame.image.load(graphicSelected)
        self.image.blit(fallingObjectImage,(0,0))

    def moveFallingObjects(self, distance):
        if self.rect.x <= WIDTH:
            self.rect.x = self.rect.x - distance

    def deleteFallingObjects(self, oldscore):
        if self.rect.x < 0:
            self.kill()
            newscore = oldscore + 1
            return newscore
        else:
            return oldscore


class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30])
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = 310
        self.rect.y = 420

        self.image.blit(pygame.image.load("Apple.png"),(0,0))

    def moveCharacter(self, movement):
        if self.rect.x >= 5 and self.rect.x <= 645:
            self.rect.x = self.rect.x + movement
        if self.rect.x < 5:
            self.rect.x = 5
        if self.rect.x > 645:
            self.rect.x = 645

    def moveVert(self, jump):
        if self.rect.y < HEIGHT and self.rect.y > 0:
            self.rect.y = self.rect.y + jump
        if self.rect.y > HEIGHT:
            self.rect.y = HEIGHT-15
        if self.rect.y <=0:
            self.rect.y = 15

# -------- Main Program Loop -----------
def main(screen, colours):
    print('got here')
    clock = pygame.time.Clock()                 # Used to manage how fast the screen updates

    font =  pygame.font.Font(None, 36)
    background_image = pygame.image.load("OrchardBackground.jpg").convert()
    nextApple = pygame.time.get_ticks() + 2500

    charactersGroup = pygame.sprite.Group()
    character = Character()
    charactersGroup.add(character)

    movement = 0
    jump = 0
    jump_distance = -10
    grav = 2
    vel = 0
    score = 0
    lives = 3
    difficulty = 0
    done = False

    allFallingObjects = pygame.sprite.Group()

    while done == False:
        for event in pygame.event.get():        # Check for an event (mouse click, key press)
            if event.type == pygame.QUIT:       # If user clicked close window
                done = True                     # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movement = -5-difficulty
                if event.key == pygame.K_RIGHT:
                    movement = 5+difficulty
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_SPACE:
                    jump = jump_distance
            if event.type == pygame.KEYUP:
                movement = 0
                jump = 0

        # Update sprites here
        if pygame.time.get_ticks() > nextApple:
            nextObject = FallingObject()
            nextObject.setImage("Apple.png")
            allFallingObjects.add(nextObject)
            nextApple = pygame.time.get_ticks() + 1500

        for eachObject in (allFallingObjects.sprites()):
            eachObject.moveFallingObjects(5)

            score = eachObject.deleteFallingObjects(score)

        character.moveCharacter(movement)
        if jump == 0:
            vel = vel + grav
            character.moveVert(vel)
        else:
            vel = 0
            character.moveVert(jump)

        # Create a list of any sprites, two groups, that have collided
        collisions = pygame.sprite.groupcollide(allFallingObjects,charactersGroup,True,False)
        if len(collisions)> 0:
            lives = lives -1

        if lives <= 0:
            done = True

        screen.blit(background_image, [0,0])
        allFallingObjects.draw(screen)
        charactersGroup.draw(screen)
        scoreImg = font.render("Score: " + str(score),1, GREEN)     # Render the score
        livesImg = font.render("Lives: " + str(lives),1, GREEN)
        screen.blit(scoreImg, (10,10))                  # Display the score
        screen.blit(livesImg, (10,30))
        pygame.display.flip()                   # Go ahead and update the screen with what we've drawn.
        clock.tick(30)                          # Limit to 20 frames per second

    return 2
