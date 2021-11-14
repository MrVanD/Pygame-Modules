from enum import Enum

import pygame
import pygame.freetype
from pygame.locals import *
from pygame.sprite import RenderUpdates
from pygame.sprite import Sprite
import os
import time

# Import games here
import DodgeAltered
import Dodge
import Shmup
import TowerDefense


### Current known limitations ###
# changing players without closing the game will probably result in the old character score changes not being saved.

# Initialise pygame
pygame.init()

# Set window and font sizes
WIDTH = 640
HEIGHT = 480
FONT_SIZE = 30

# Same colours but defined in a dictionary
colours = {"BLACK": (0, 0, 0),
           "WHITE": (255, 255, 255),
           "RED": (255, 0, 0),
           "GREEN": (0, 255, 0),
           "BLUE": (0, 0, 255),
           "ORANGE":(255, 165, 0),
           }

# Setup the screen size and the window name
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Year 9 Rec Coding Games Library - 2021")

# *** Define Classes Here *** #
class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        self.mouse_over = False
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()


    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player:
    def __init__(self, score=0, lives=3, current_level=1):
        self.score = score
        self.lives = lives
        self.curent_level = current_level



# To add a game.
# 1. Import the game.
# 2. Add its name and a unique identifier to the Game List.
# 3. Add access programming to the Main Loop.
# 4. Add a button to the level picker screen.
# 5. Add a function call in the Play Game definition.

# To do: Automate the addition of new games to reduce complexity on user end.


# Game States
class GameState(Enum):
    QUIT = -1
    TITLE = 0
    LEVEL_PICKER = 1
    CHARACTER_PICKER = 2
    NewCharacter = 3
    ChooseCharacter = 4

    # Game List
    DODGE = 10
    DODGEALTERED = 11
    SHMUP = 12
    TOWERDEFENSE = 13


# *** Define Functions Here *** #

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    # Returns a surface with text written on it.
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

# Main code running the game
def main():
    # Open the character list and store it as a dictionary
    character_list = {}                                             # Create the dictionary and make it empty
    name_list = []
    with open("Character List.txt", "r") as file:                        # Open up the character file
        try:
            for line in file:                                       # Iterate over each line
                character, dodge, shmup, td = line.split("|")       # Split up each line into idividual blocks
                shmup = int(shmup)                                  # Set each score to an integer
                dodge = int(dodge)
                td = int(td)
                games = [dodge,shmup,td]                            # Collate all scores into an array
                character_list[character] = games                   # Add data to the character dictionary
                name_list.append(character)
        except:
            print("failed")                                         # If the attempt to read fails (i.e. no lines)
    player = {}
    player["name"] = name_list[0]
    player["dodge"] = 0
    player["shmup"] = 0
    player["td"] = 0
    # Set the initial Game State
    game_state = GameState.TITLE
    loop = True
    # Check for which game state is currently running
    while loop == True:
        # Display the Title screen
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.LEVEL_PICKER:
            game_state = pick_level(screen)

        if game_state == GameState.CHARACTER_PICKER:
            player = pick_character(screen)
            game_state = title_screen(screen)

        # Quit the game
        if game_state == GameState.QUIT:
            loop = False

        # Game Access List
        if game_state == GameState.DODGE:
            player = play_game(screen, GameState.DODGE, player)
            game_state = GameState.LEVEL_PICKER
        if game_state == GameState.DODGEALTERED:
            player = play_game(screen, GameState.DODGEALTERED, player)
            game_state = GameState.LEVEL_PICKER
        if game_state == GameState.SHMUP:
            player = play_game(screen, GameState.SHMUP, player)
            game_state = GameState.LEVEL_PICKER
        if game_state == GameState.TOWERDEFENSE:
            player = play_game(screen, GameState.TOWERDEFENSE, player)
            game_state = GameState.LEVEL_PICKER

        # If a game state is undefined or unexpected, return to the title screen.
        else:
            game_state = title_screen(screen)

    new_scores = [player["dodge"],player["shmup"],player["td"]]
    character_list[player["name"]] = new_scores                     # Update scores of the specific player

    with open("Character List.txt", 'w') as file:               # Open the character file.
        for character in character_list:                        # Loop through each character
            # Add each character with their scores and correct formatting
            entry = character+"|"+\
                    str(character_list[character][0])+"|"+\
                    str(character_list[character][1])+"|"+\
                    str(character_list[character][2])+"\n"
            file.write(entry)                                   # Write the character
    # Generate a new entry for the character list
    pygame.quit()


def title_screen(screen):
    pickcha_btn = UIElement(
        center_position=(WIDTH / 2, (HEIGHT / 2) - (FONT_SIZE*3)),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Pick Character",
        action=GameState.CHARACTER_PICKER,
    )

    picklvl_btn = UIElement(
        center_position=(WIDTH / 2, (HEIGHT / 2) - FONT_SIZE),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Pick Level",
        action=GameState.LEVEL_PICKER,
    )

    quit_btn = UIElement(
        center_position=(WIDTH / 2, (HEIGHT / 2) + FONT_SIZE),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(pickcha_btn,picklvl_btn, quit_btn)
    return game_loop(screen, buttons)


def pick_level(screen):
    dodgealtered_btn = UIElement(
        center_position=(WIDTH/2, FONT_SIZE*2),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Dodge - Altered",
        action=GameState.DODGEALTERED,
    )

    dodge_btn = UIElement(
        center_position=(WIDTH/2, FONT_SIZE *3),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Dodge",
        action=GameState.DODGE,
    )

    shmup_btn = UIElement(
        center_position=(WIDTH/2, FONT_SIZE *4),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Shmup",
        action=GameState.SHMUP,
    )

    td_btn = UIElement(
        center_position=(WIDTH/2, FONT_SIZE *5),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Tower Defense",
        action=GameState.TOWERDEFENSE,
    )

    return_btn = UIElement(
        center_position=(WIDTH / 2, HEIGHT - FONT_SIZE * 2),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Return to main menu",
        action=GameState.TITLE,
    )

    buttons = RenderUpdates(dodgealtered_btn, dodge_btn, shmup_btn, td_btn, return_btn)
    return game_loop(screen, buttons)

def pick_character(screen):
    return_btn = UIElement(
        center_position=(WIDTH / 2, HEIGHT - FONT_SIZE * 2),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Return to main menu",
        action=GameState.TITLE,
    )

    # A button to create a new character
    new_cha_btn = UIElement(
        center_position=(WIDTH / 2, HEIGHT/2 - FONT_SIZE * 3),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Create New Character",
        action=GameState.NewCharacter,
    )

    # A button to choose an existing character
    cho_cha_btn = UIElement(
        center_position=(WIDTH / 2, HEIGHT/2 - FONT_SIZE),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Pick Existing Character",
        action=GameState.ChooseCharacter,
    )

    buttons = RenderUpdates(return_btn,new_cha_btn, cho_cha_btn)
    return characters(screen, buttons)

def characters(screen, buttons):
    player = {}                                                                     # Set up player
    player["name"] = None
    player["dodge"] = 0
    player["shmup"] = 0
    player["td"] = 0
    # Loop until action is taken
    while True:
        mouse_up = False                                                            # Reset mouse state to unclicked
        for event in pygame.event.get():                                            # Check for a right mouse click
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(colours["BLUE"])                                                # Reset the background screen colour
        # Check if a button was pressed
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                if button.action == GameState.TITLE:                                # If the button pressed was return
                    return player
                else:
                    # Get a list of existing characters and their scores and write them to a dictionary
                    character_list = {}                                             # Create the dictionary and make it empty
                    with open("Character List.txt") as file:                        # Open up the character file
                        try:
                            for line in file:                                       # Iterate over each line
                                character, dodge, shmup, td = line.split("|")       # Split up each line into idividual blocks
                                shmup = int(shmup)                                  # Set each score to an integer
                                dodge = int(dodge)
                                td = int(td)
                                games = [dodge,shmup,td]                            # Collate all scores into an array
                                character_list[character] = games                   # Add data to the character dictionary
                        except:
                            print("failed")                                         # If the attempt to read fails (i.e. no lines)

                    # Create a new character
                    if button.action == GameState.NewCharacter:                     # Check if button was for a new character
                        loop = True                                                 # Set loop to run
                        new_cha_text = "New Character Name"                         # Set temporary new character name
                        instr_txt = "Type a name then press enter to add."          # Set the instructions
                        font = pygame.font.SysFont(None, 48)                        # Set the font
                        instr = font.render(instr_txt, True, colours["RED"])        # Create the render of the instructions
                        rect_inst = instr.get_rect()                                # Get the rectangle of the instructions
                        rect_inst.center = (WIDTH/2, HEIGHT/2)                      # Set the center of the rectangle
                        # Loop while creating a new character
                        while loop == True:
                            for event in pygame.event.get():                        # Get event list
                                if event.type == KEYDOWN:                           # If the event list contains a keydown action
                                    if event.key == K_RETURN:                       # If that action is the return key
                                        if new_cha_text in character_list:          # If the name is already in the character list
                                            print("Character already exists")       # Handler for if the character already exists
                                        else:
                                            character_list[new_cha_text] =[0,0,0]   # Set new character and give basic game stats
                                            player["name"] = new_cha_text
                                        loop = False                                # Break out of loop
                                    elif event.key == K_BACKSPACE:                  # If key is backspace
                                        if len(new_cha_text) > 0:                   # Check that character name isn't less than 1
                                            new_cha_text = new_cha_text[:-1]        # Remove the last character from the string
                                    elif event.key == K_ESCAPE:                     # If the escape key is pressed
                                        print("escape") # Remove: Temp Code
                                        loop = False
                                    else:
                                        new_cha_text += event.unicode               # Add the character to the string
                                        if new_cha.get_rect().width > WIDTH-48:     # If length of name is longer than the screen size
                                            new_cha_text = new_cha_text[:-1]        # Trim down the name.
                            # Display the new character name and a cursor
                            new_cha = font.render(new_cha_text, True, colours["RED"])
                            new_cha_rect = new_cha.get_rect()                       # Create a rectangle with the name
                            new_cha_rect.topleft = (20, 20)                         # Set where the rectangle will spawn
                            new_cha_rect.size=new_cha.get_size()
                            cursor = Rect(new_cha_rect.topright,                    # Set the cursor size
                                          (3, new_cha_rect.height))
                            cursor.topleft = new_cha_rect.topright                  # Set where te cursor is
                            screen.fill(colours["BLUE"])                            # Refresh the screen
                            screen.blit(new_cha, new_cha_rect)                      # Display the editable name
                            screen.blit(instr, rect_inst)                           # Display the instructions
                            if time.time() % 1 > 0.5:                               # Blink the cursor
                                pygame.draw.rect(screen, colours["RED"], cursor)
                            pygame.display.update()
                        # Save the character to the file
                        with open("Character List.txt", 'w') as file:               # Open the character file.
                            for character in character_list:                        # Loop through each character
                                # Add each character with their scores and correct formatting
                                entry = character+"|"+\
                                        str(character_list[character][0])+"|"+\
                                        str(character_list[character][1])+"|"+\
                                        str(character_list[character][2])+"\n"
                                file.write(entry)                                   # Write the character

                    # If the user wants to choose an existing character
                    elif button.action == GameState.ChooseCharacter:
                        chosen = False                                              # Setup loop
                        char_height = FONT_SIZE                                     # Set character height
                        font = pygame.font.SysFont(None, 48)                        # Set the font
                        instruction = "Choose your character and press enter."      # Create instructions
                        answer = ""                                                 # Create initial answer
                        # Loop while choosing a new character
                        while chosen == False:
                            screen.fill(colours["BLUE"])                            # Refresh the screen with a blue fill
                            char_index = 1                                          # Set character index to 1
                            char_names = []
                            # Loop over each character in the dictionary and display them on the screen.
                            for character in character_list:
                                text = str(char_index)+". "+character               # Assemble character display
                                new_cha = font.render(text, True, colours["RED"])   # Render the character
                                rect_text = new_cha.get_rect()                      # Create the box for the character
                                rect_text.center = (WIDTH/2, char_height*char_index)    # Set where the centre of the box is
                                screen.blit(new_cha, rect_text)                     # Update the screen with the character
                                char_names.append(character)
                                char_index += 1                                     # Increase the character index by 1
                            instr = font.render(instruction, True, colours["RED"])  # Create the render of the instructions
                            rect_inst = instr.get_rect()                            # Get the rectangle of the instructions
                            rect_inst.center = (WIDTH/2, HEIGHT - FONT_SIZE*2)      # Set the center of the rectangle
                            # Handle button presses
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == pygame.K_BACKSPACE:             # If the backspace key is pressed
                                        if len(answer) > 0:
                                            answer = answer[:-1]
                                    elif event.key == K_RETURN:                     # If the enter key is pressed
                                        if len(answer) >0 and len(answer) <= len(str(char_index)):      # If the answer provided matches the character index
                                            # Character chosen, return the character chosen
                                            chosen = True
                                            index = int(answer)-1
                                            # Set new character and give basic game stats
                                            player["name"] = char_names[index]
                                            player["dodge"] = character_list[char_names[index]][0]
                                            player["shmup"] = character_list[char_names[index]][1]
                                            player["td"] = character_list[char_names[index]][2]
                                        else:
                                            print("error in chosen character")
                                    else:
                                        answer += event.unicode
                                        # If length of name is longer than the screen size, trim down the name.
                                        if ans.get_rect().width > WIDTH-48:
                                            answer = answer[:-1]
                            # Generate the render and box for the answer
                            ans = font.render(answer, True, colours["RED"])
                            rect_ans = ans.get_rect()
                            rect_ans.center = (WIDTH/2, HEIGHT-FONT_SIZE)

                            # Update the display
                            cursor = Rect(rect_inst.topright, (3, rect_inst.height))          # Set where the cursor is set
                            cursor.topleft = rect_ans.topright
                            screen.blit(instr, rect_inst)
                            screen.blit(ans, rect_ans)

                            if time.time() % 1 > 0.5:
                                pygame.draw.rect(screen, colours["RED"], cursor)
                            pygame.display.update()

        buttons.draw(screen)
        pygame.display.flip()



def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(colours["BLUE"])

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action


        buttons.draw(screen)
        pygame.display.flip()

# Run the assigned game, pass the screen and colours list through to the chosen games code.
def play_game(screen, game, player):
    game_txt = ""
    score = 0
    if game == GameState.DODGE:
        game_txt = "dodge"
        screen = pygame.display.set_mode((700,500), pygame.RESIZABLE)       # Set screen to Dodge's custom size
        score = Dodge.main(screen, colours)
    if game == GameState.DODGEALTERED:
        game_txt = "dodge-altered"
        screen = pygame.display.set_mode((700,500), pygame.RESIZABLE)       # Set screen to Dodge - Altered's custom size
        score = DodgeAltered.main(screen,colours)
    if game == GameState.SHMUP:
        game_txt = "shmup"
        screen = pygame.display.set_mode((400,600), pygame.RESIZABLE)       # Set screen to Shmup's custom size
        score = Shmup.main(screen,colours)
    if game == GameState.TOWERDEFENSE:
        game_txt = "td"
        screen = pygame.display.set_mode((600,400), pygame.RESIZABLE)       # Set screen to Tower Defense's custom size
        score = TowerDefense.main(screen)

    if player[game_txt] < score:
            player[game_txt] = score
    screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)      # Reset screen to menu standard
    pygame.display.flip()
    return player


# Run the main menu
if __name__ == "__main__":
    main()
