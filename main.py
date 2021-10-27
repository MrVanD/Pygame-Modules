from enum import Enum

import pygame
import pygame.freetype
from pygame.sprite import RenderUpdates
from pygame.sprite import Sprite

# Import games here
import DodgeAltered

# Initialise pygame
pygame.init()

# Set window and font sizes
WIDTH = 700
HEIGHT = 500
FONT_SIZE = 30

# Same colours but defined in a dictionary
colours = {"BLACK": (0, 0, 0),
           "WHITE": (255, 255, 255),
           "RED": (255, 0, 0),
           "GREEN": (0, 255, 0),
           "BLUE": (0, 0, 255),
           }

# Setup the screen size and the window name
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Mr van's Dodge Game")


# *** Define Classes Here ***
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


# Game States
class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    LEVEL_PICKER = 2
    NEXT_LEVEL = 3
    DODGE = 4

# *** Define Functions Here ***

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    # Returns a surface with text written on it.
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen)

        if game_state == GameState.LEVEL_PICKER:
            game_state = pick_level(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = play_level(screen, player)

        if game_state == GameState.NEXT_LEVEL:
            player.curent_level += 1
            game_state = play_level(screen, player)

        if game_state == GameState.DODGE:
            game_state = play_game(screen, GameState.DODGE)


def title_screen(screen):
    start_btn = UIElement(
        center_position=(WIDTH / 2, (HEIGHT / 2) + 2 * FONT_SIZE),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Pick Level",
        action=GameState.LEVEL_PICKER,
    )

    quit_btn = UIElement(
        center_position=(WIDTH / 2, (HEIGHT / 2) + 4 * FONT_SIZE),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(start_btn, quit_btn)
    return game_loop(screen, buttons)


def pick_level(screen):
    pick_lvl_btn = UIElement(
        center_position=(WIDTH / 2, HEIGHT / 2),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Start Level",
        action=GameState.NEWGAME,
    )

    dodge_btn = UIElement(
        center_position=(100, 100),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Dodge",
        action=GameState.DODGE,
    )

    return_btn = UIElement(
        center_position=(WIDTH / 2, HEIGHT / 2 + FONT_SIZE * 4),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Return to main menu",
        action=GameState.TITLE,
    )

    buttons = RenderUpdates(pick_lvl_btn, dodge_btn, return_btn)
    return game_loop(screen, buttons)


def play_level(screen, player):
    return_btn = UIElement(
        center_position=(WIDTH / 2, HEIGHT / 2),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text="Return to main menu",
        action=GameState.TITLE,
    )

    nextlevel_btn = UIElement(
        center_position=(400, 400),
        font_size=FONT_SIZE,
        bg_rgb=colours["BLUE"],
        text_rgb=colours["WHITE"],
        text=f"Next level ({player.curent_level + 1})",
        action=GameState.NEXT_LEVEL,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn)
    return game_loop(screen, buttons)


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


def play_game(screen, game):
    if game == GameState.DODGE:
        DodgeAltered.main(screen,colours)

    pygame.display.flip()
    return GameState.LEVEL_PICKER


# Run the main menu
if __name__ == "__main__":
    main()
