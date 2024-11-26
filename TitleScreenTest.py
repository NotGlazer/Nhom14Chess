import pygame as p
import sys

# Constants for screen dimensions
BOARD_WIDTH = 512
MOVE_LOG_PANEL_WIDTH = 250
SCREEN_WIDTH = BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH
SCREEN_HEIGHT = BOARD_WIDTH

def title_screen(screen):
    """
    Display the title screen with options for single-player and multiplayer.
    """
    screen.fill(p.Color("white"))
    font = p.font.SysFont("Helvetica", 32, True, False)

    # Title text
    title_text = font.render("Chess Game", True, p.Color("black"))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # Single Player button
    single_text = font.render("Single Player", True, p.Color("blue"))
    single_rect = single_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(single_text, single_rect)

    # Multiplayer button
    multi_text = font.render("Multiplayer", True, p.Color("blue"))
    multi_rect = multi_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(multi_text, multi_rect)

    p.display.flip()

    # Wait for user to click a button
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                if single_rect.collidepoint(mouse_pos):
                    return False  # Single-player
                elif multi_rect.collidepoint(mouse_pos):
                    return True   # Multiplayer

def main():
    p.init()
    screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    p.display.set_caption("Chess Game - Title Screen")
    
    player_two = title_screen(screen)
    print("Multiplayer selected:", player_two)  # This will print True if Multiplayer is selected, else False
    
    p.quit()

if __name__ == "__main__":
    main()
