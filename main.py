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
    ### Remove this when player is fully implemented
    player = {GameState.SHMUP:16}
    print(player)
    '''
    # Initialise the character list.
    # Check if the character file exists, if it does not, make it.
    if not os.path.exists("Character List.txt"):            # Check if the character list exists
        file = open("Character List.txt", "x")              # If it does not, create it
        file.close()                                        # Close the character list
    '''
    # Set the initial Game State
    game_state = GameState.TITLE

    # Check for which game state is currently running
    while True:
        # Display the Title screen
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.LEVEL_PICKER:
            game_state = pick_level(screen)

        if game_state == GameState.CHARACTER_PICKER:
            game_state = pick_character(screen)

        # Quit the game
        if game_state == GameState.QUIT:
            pygame.quit()
            return
        # Game Access List
        if game_state == GameState.DODGE:
            game_state = play_game(screen, GameState.DODGE, player)
        if game_state == GameState.DODGEALTERED:
            game_state = play_game(screen, GameState.DODGEALTERED, player)
        if game_state == GameState.SHMUP:
            game_state = play_game(screen, GameState.SHMUP, player)
        if game_state == GameState.TOWERDEFENSE:
            game_state = play_game(screen, GameState.TOWERDEFENSE, player)

        # If a game state is undefined or unexpected, return to the title screen.
        else:
            game_state = title_screen(screen)


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
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(colours["BLUE"])

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                if button.action == GameState.TITLE:
                    return ui_action
                else:
                    # Get a list of existing characters and write them to a dictionary
                    character_list = {}             # Create the dictionary and make it empty
                    with open("Character List.txt") as file:
                        try:
                            for line in file:                                       # Iterate over each line
                                character, shmup, dodge, td = line.split("|")       # Split up each line into idividual blocks
                                shmup = int(shmup)                                  # Set each score to an integer
                                dodge = int(dodge)
                                td = int(td)
                                games = [shmup,dodge,td]                            # Collate all scores into an array
                                character_list[character] = games                   # Add data to the character dictionary
                        except:
                            print("failed")
                    if button.action == GameState.NewCharacter:
                        loop = True                                             # Set loop to run
                        temp_name_txt = "New Character Name"                    # Set temporary name
                        instr_txt = "Type a name then press enter to add."      # Set the instructions
                        font = pygame.font.SysFont(None, 48)                    # Set the font
                        img = font.render(temp_name_txt, True, colours["RED"])  # Create a render of the name
                        instr = font.render(instr_txt, True, colours["RED"])    # Create the render of the instructions
                        rect = img.get_rect()                                   # Create a rectangle with the name
                        rect.topleft = (20, 20)                                 # Set where the rectangle will spawn
                        cursor = Rect(rect.topright, (3, rect.height))          # Set where the cursor is set
                        rect_inst = instr.get_rect()                            # Get the rectangle of the instructions
                        rect_inst.center = (WIDTH/2, HEIGHT/2)                  # Set the center of the rectangle
                        # Loop while creating a new name
                        while loop == True:
                            for event in pygame.event.get():                    # Get event list
                                if event.type == KEYDOWN:                       # If the event list contains a keydown action
                                    if event.key == K_RETURN:                   # If that action is the return key
                                        if temp_name_txt in character_list:     # If the name is already in the character list
                                            print("Character already exists")
                                        else:
                                            character_list[temp_name_txt] =[0,0,0]
                                        loop = False
                                    elif event.key == K_BACKSPACE:
                                        if len(temp_name_txt) > 0:
                                            temp_name_txt = temp_name_txt[:-1]
                                    else:
                                        temp_name_txt += event.unicode
                                        # If length of name is longer than the screen size, trim down the name.
                                        if img.get_rect().width > WIDTH-48:
                                            print(img.get_rect().width)
                                            temp_name_txt = temp_name_txt[:-1]
                                    img = font.render(temp_name_txt, True, colours["RED"])
                                    rect.size=img.get_size()
                                    cursor.topleft = rect.topright
                            screen.fill(colours["BLUE"])
                            screen.blit(img, rect)
                            screen.blit(instr, rect_inst)
                            if time.time() % 1 > 0.5:
                                pygame.draw.rect(screen, colours["RED"], cursor)
                            pygame.display.update()
                        # Loop through the character list dictionary to save the character to the file
                        with open("Character List.txt", 'w') as file:           # Open the character file.
                            for character in character_list:
                                print(character)
                                print(character_list[character])
                                entry = character+"|"+\
                                        str(character_list[character][0])+"|"+\
                                        str(character_list[character][1])+"|"+\
                                        str(character_list[character][2])+"\n"
                                file.write(entry)

                    elif button.action == GameState.ChooseCharacter:
                        # Create a dictionary with the character details.
                        with open("Character List.txt", "r") as file:
                            for line in file:                                       # Iterate over each line
                                character, shmup, dodge, td = line.split("|")       # Split up each line into individual blocks
                                shmup = int(shmup)                                  # Set each score to an integer
                                dodge = int(dodge)
                                td = int(td)
                                games = [shmup,dodge,td]                            # Collate all scores into an array
                                character_list[character] = games                   # Add data to the character dictionary
                        # Create a loop until a character choice is made
                        chosen = False
                        # Setup some variables and statics
                        char_height = FONT_SIZE
                        font = pygame.font.SysFont(None, 48)                    # Set the font
                        # Create instructions
                        instruction = "Choose your character and press enter."
                        answer = ""
                        while chosen == False:
                            # Refresh the screen with a blue fill
                            screen.fill(colours["BLUE"])
                            # Loop over each character in the dictionary and display them on the screen.
                            char_index = 1
                            for character in character_list:
                                text = str(char_index)+". "+character
                                img = font.render(text, True, colours["RED"])
                                rect_text = img.get_rect()
                                rect_text.center = (WIDTH/2, char_height*char_index)
                                screen.blit(img, rect_text)
                                char_index += 1
                            # Output instructions and set instruction box size
                            instr = font.render(instruction, True, colours["RED"])    # Create the render of the instructions
                            rect_inst = instr.get_rect()                            # Get the rectangle of the instructions
                            rect_inst.center = (WIDTH/2, HEIGHT - FONT_SIZE*2)                  # Set the center of the rectangle
                            # Handle button presses
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == pygame.K_BACKSPACE:
                                        if len(answer) > 0:
                                            answer = answer[:-1]
                                    elif event.key == K_RETURN:
                                        if len(answer) == 1:
                                            # Character chosen, return the character chosen
                                            chosen = True
                                        else:
                                            print("error in chosen character")
                                    else:
                                        answer += event.unicode
                                        # If length of name is longer than the screen size, trim down the name.
                                        if ans.get_rect().width > WIDTH-48:
                                            print(ans.get_rect().width)
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



                """
                # Run the code to deal with the buttons presses
                if button.action == GameState.NewCharacter:                 # Create a new character
                    loop = True                                             # Set loop to run
                    temp_name_txt = "New Character Name"                    # Set temporary name
                    instr_txt = "Type a name then press enter to add."      # Set the instructions
                    font = pygame.font.SysFont(None, 48)                    # Set the font
                    img = font.render(temp_name_txt, True, colours["RED"])  # Create a render of the name
                    instr = font.render(instr_txt, True, colours["RED"])    # Create the render of the instructions
                    rect = img.get_rect()                                   # Create a rectangle with the name
                    rect.topleft = (20, 20)                                 # Set where the rectangle will spawn
                    cursor = Rect(rect.topright, (3, rect.height))          # Set where the cursor is set
                    rect_inst = instr.get_rect()                            # Get the rectangle of the instructions
                    rect_inst.center = (WIDTH/2, HEIGHT/2)                  # Set the center of the rectangle
                    char_lst = {}
                    while loop == True:
                        # Create a character list
                        # Open the character profile list
                        with open("Character List.txt") as file:
                            # Loop through all lines of the text
                            for line in file:
                                # If a character is found, add it to the list
                                if "=" in line:
                                    character = line[:-11]                   # Remove the = from the name
                                    char_lst[character] = "Shmup - 0\n"
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == K_RETURN:         # If 'enter' is pressed.
                                        # Open the character list
                                        list_keys = char_lst.keys()
                                        #print("Key List")
                                        #print(list_keys)
                                        if len(list_keys) < 1:
                                            # add the character to the temporary list
                                            char_lst[temp_name_txt] = "Shmup - 0"+'\n'
                                            #print(char_lst)
                                        for key in list_keys:
                                            #print("Key")
                                            #print(key)
                                            # Check if character exists in the keys.
                                            if key == temp_name_txt:
                                                # Print that the character exists
                                                print("Character Exists")       # Change this to a splash screen
                                                # Exit the character creation
                                                loop = False
                                            else:
                                                # add the character to the temporary list
                                                char_lst[temp_name_txt] = "Shmup res - 0\n"
                                                print(char_lst)
                                                break
                                        loop =False
                                    if event.key == K_BACKSPACE:
                                        if len(temp_name_txt) > 0:
                                            temp_name_txt = temp_name_txt[:-1]
                                    else:
                                        temp_name_txt += event.unicode
                                        # If length of name is longer than the screen size, trim down the name.
                                        if img.get_rect().width > WIDTH-48:
                                            print(img.get_rect().width)
                                            temp_name_txt = temp_name_txt[:-1]
                                    img = font.render(temp_name_txt, True, colours["RED"])
                                    rect.size=img.get_size()
                                    cursor.topleft = rect.topright
                            screen.fill(colours["BLUE"])
                            screen.blit(img, rect)
                            screen.blit(instr, rect_inst)
                            if time.time() % 1 > 0.5:
                                pygame.draw.rect(screen, colours["RED"], cursor)
                            pygame.display.update()


                        if loop == False:
                            print("loop = false")
                            print(char_lst)
                            with open("Character List.txt", "w") as file:
                                file.write("Character List:\n")
                                list_keys = char_lst.keys()
                                for key in list_keys:
                                    file.write(key+"="+char_lst[key]+"\n")

                elif button.action == GameState.ChooseCharacter:            # Choose an existing character.
                    # Create a character list
                    char_list={}
                    with open("Character List.txt", 'r') as file:
                        for line in file:
                            print(line)
                            if "=" in line:
                                print("got here")
                                character, shmup = line.split("=")
                                char_list[character] = shmup
                        print(char_list)
                
                else:
                    return ui_action
                """

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
    if game == GameState.DODGE:
        screen = pygame.display.set_mode((700,500), pygame.RESIZABLE)       # Set screen to Dodge's custom size
        Dodge.main(screen, colours)
    if game == GameState.DODGEALTERED:
        screen = pygame.display.set_mode((700,500), pygame.RESIZABLE)       # Set screen to Dodge - Altered's custom size
        DodgeAltered.main(screen,colours)
    if game == GameState.SHMUP:
        screen = pygame.display.set_mode((400,600), pygame.RESIZABLE)       # Set screen to Shmup's custom size
        new_score = Shmup.main(screen,colours)
        if player[game] < new_score:
            player[game] = new_score
    if game == GameState.TOWERDEFENSE:
        screen = pygame.display.set_mode((600,400), pygame.RESIZABLE)       # Set screen to Tower Defense's custom size
        TowerDefense.main(screen)

    screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)      # Reset screen to menu standard
    pygame.display.flip()
    return GameState.LEVEL_PICKER


# Run the main menu
if __name__ == "__main__":
    main()
