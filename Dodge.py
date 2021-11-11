import pygame  # Imports pygame and other libraries
import random

# Required Global Variables
WIDTH = 700
HEIGHT = 500
BLACK = (0, 0, 0)  # Define the rgb colour for black


# *** Define Classes Here ***
class FallingObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.timeCreated = pygame.time.get_ticks()
        self.image = pygame.Surface([30, 30])
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = 0

    def setImage(self, graphicSelected):
        fallingObjectImage = pygame.image.load(graphicSelected)
        self.image.blit(fallingObjectImage, (0, 0))

    def moveFallingObjects(self, distance):
        if self.rect.y <= HEIGHT:
            self.rect.y = self.rect.y + distance

    def deleteFallingObjects(self, oldscore):
        if self.rect.y > HEIGHT:
            self.kill()
            newscore = oldscore + 1
            return newscore
        else:
            return oldscore


class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 30])
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = 315
        self.rect.y = HEIGHT - 30

        self.image.blit(pygame.image.load("Dodge res/Apple.png"), (0, 0))

    def moveCharacter(self, movement):
        if self.rect.x >= 5 and self.rect.x <= 645:
            self.rect.x = self.rect.x + movement
        if self.rect.x < 5:
            self.rect.x = 5
        if self.rect.x > 645:
            self.rect.x = 645


# -------- Main Program Loop -----------
def main(screen, colours):
    clock = pygame.time.Clock()  # Used to manage how fast the screen updates
    font = pygame.font.Font(None, 36)
    background_image = pygame.image.load("Dodge res/OrchardBackground.jpg").convert()
    next_apple = pygame.time.get_ticks() + 2500

    charactersGroup = pygame.sprite.Group()
    character = Character()
    charactersGroup.add(character)

    # Setup player and game states
    movement = 0
    score = 0
    lives = 3
    done = False

    allFallingObjects = pygame.sprite.Group()

    while done == False:
        for event in pygame.event.get():  # Check for an event (mouse click, key press)
            if event.type == pygame.QUIT:  # If user clicked close window
                done = True  # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:  # If user pressed a key
                if event.key == pygame.K_LEFT:  # If user pressed the left key
                    movement = -5  # Move to the left 5 pixels
                if event.key == pygame.K_RIGHT:  # If pressed the right key
                    movement = 5  # Move to the right 5 pixels
                if event.key == pygame.K_ESCAPE:  # If pressed the escape key
                    done = True  # Flag that we are to exit
            if event.type == pygame.KEYUP:  # If a key is released
                movement = 0  # Set movement to nothing

        # Update sprites here
        if pygame.time.get_ticks() > next_apple:
            next_object = FallingObject()
            next_object.setImage("Dodge res/Apple.png")
            allFallingObjects.add(next_object)
            next_apple = pygame.time.get_ticks() + 1500

        # Loop through each object, making them fall
        for eachObject in (allFallingObjects.sprites()):
            eachObject.moveFallingObjects(5)  # move each falling apple downwards
            score = eachObject.deleteFallingObjects(score)  # Increase the score if the object is deleted

        # Move the character based on the key define movement
        character.moveCharacter(movement)

        # Create a list of any sprites, two groups, that have collided
        collisions = pygame.sprite.groupcollide(allFallingObjects, charactersGroup, True, False)
        if len(collisions) > 0:
            lives = lives - 1  # Reduce the number of lives by 1

        # Exit the game if the number of lives drops below 1
        if lives <= 0:
            done = True

        screen.blit(background_image, [0, 0])  # Refresh the screen
        allFallingObjects.draw(screen)  # Draw the falling apples
        charactersGroup.draw(screen)  # Draw the player character
        score_img = font.render("Score: " + str(score), 1, colours["GREEN"])  # Render the score
        if lives == 3:
            txt_col = colours["GREEN"]
        elif lives == 2:
            txt_col = colours["ORANGE"]
        elif lives == 1:
            txt_col = colours["RED"]
        lives_img = font.render("Lives: " + str(lives), 1, txt_col)  # Render the lives
        screen.blit(score_img, (10, 10))  # Display the score
        screen.blit(lives_img, (10, 30))  # Disply the remaining lives
        pygame.display.flip()  # Go ahead and update the screen with what we've drawn.
        clock.tick(30)  # Limit game to 30 frames per second

    # End game, return to the level picker screen
    return
