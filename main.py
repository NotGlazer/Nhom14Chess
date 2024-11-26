"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""
import asyncio
import pygame as p
import sys
import ChessEngine
import ChessAI
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

async def title_screen(screen):
    """
    Display the title screen with options for single-player, multiplayer, and bot vs bot.
    """
    # Fill the screen with black
    screen.fill(p.Color("black"))

    # Load the background image
    bg_image = p.image.load("images/background.png")
    
    # Get the original dimensions of the image
    original_width, original_height = bg_image.get_size()

    # Calculate scaling factors
    scale_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH) / original_width
    scale_y = BOARD_HEIGHT / original_height

    # Use the smaller scale factor to maintain aspect ratio
    scale = min(scale_x, scale_y)

    # Calculate new dimensions
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # Scale the image
    bg_image = p.transform.scale(bg_image, (new_width, new_height))

    # Calculate position to center the image
    bg_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH) // 2 - new_width // 2
    bg_y = BOARD_HEIGHT // 2 - new_height // 2

    # Blit the background image centered
    screen.blit(bg_image, (bg_x, bg_y))

    # Fonts
    font = p.font.SysFont("Helvetica", 32, True, False)
    title_font = p.font.SysFont("Helvetica", 80, True, False)
    title_text = title_font.render("CHESS GAME", True, p.Color("White"))
    nhom14_font = p.font.SysFont("Helvetica", 24, True, False)
    nhom14_text = nhom14_font.render("Nhóm 14", True, p.Color("Black"))
    single_text = font.render("Singleplayer", True, p.Color("white"))
    multi_text = font.render("Multiplayer", True, p.Color("white"))
    bot_vs_bot_text = font.render("Bot vs Bot", True, p.Color("white"))

    # Center title text
    title_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH) // 2 - title_text.get_width() // 2
    title_y = BOARD_HEIGHT // 4 - title_text.get_height() // 2

    # Create semi-transparent black box behind the title text
    box_color = (0, 0, 0, 128)  # RGBA for black with 50% opacity
    title_box = p.Surface((title_text.get_width() + 20, title_text.get_height() + 10), p.SRCALPHA)
    title_box.fill(box_color)

    # Blit the title box and then the title text on top
    screen.blit(title_box, (title_x - 10, title_y - 5))
    screen.blit(title_text, (title_x, title_y))

    # Position and render Nhóm 14 text
    nhom14_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH) // 2 - nhom14_text.get_width() // 2
    nhom14_y = title_y + title_text.get_height() + 5  # 5 pixels below the title
    screen.blit(nhom14_text, (nhom14_x, nhom14_y))

    # Position the options
    single_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH) // 2 - single_text.get_width() // 2
    single_y = BOARD_HEIGHT // 2 - single_text.get_height() // 2
    multi_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH) // 2 - multi_text.get_width() // 2
    multi_y = BOARD_HEIGHT // 2 + single_text.get_height() + 10
    bot_vs_bot_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH) // 2 - bot_vs_bot_text.get_width() // 2
    bot_vs_bot_y = multi_y + multi_text.get_height() + 30

    # Create semi-transparent black boxes behind the options
    single_box = p.Surface((single_text.get_width() + 20, single_text.get_height() + 10), p.SRCALPHA)
    single_box.fill(box_color)
    multi_box = p.Surface((multi_text.get_width() + 20, multi_text.get_height() + 10), p.SRCALPHA)
    multi_box.fill(box_color)
    bot_vs_bot_box = p.Surface((bot_vs_bot_text.get_width() + 20, bot_vs_bot_text.get_height() + 10), p.SRCALPHA)
    bot_vs_bot_box.fill(box_color)

    # Blit the boxes and then the text on top
    screen.blit(single_box, (single_x - 10, single_y - 5))
    screen.blit(single_text, (single_x, single_y))
    screen.blit(multi_box, (multi_x - 10, multi_y - 5))
    screen.blit(multi_text, (multi_x, multi_y))
    screen.blit(bot_vs_bot_box, (bot_vs_bot_x - 10, bot_vs_bot_y - 5))
    screen.blit(bot_vs_bot_text, (bot_vs_bot_x, bot_vs_bot_y))

    p.display.flip()

    # Event loop for title screen
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = p.mouse.get_pos()
                # Check if single player is clicked
                if single_x <= mouse_x <= single_x + single_text.get_width() and single_y <= mouse_y <= single_y + single_text.get_height():
                    return "single"  # Single player selected
                # Check if multiplayer is clicked
                elif multi_x <= mouse_x <= multi_x + multi_text.get_width() and multi_y <= mouse_y <= multi_y + multi_text.get_height():
                    return "multi"  # Multiplayer selected
                # Check if bot vs bot is clicked
                elif bot_vs_bot_x <= mouse_x <= bot_vs_bot_x + bot_vs_bot_text.get_width() and bot_vs_bot_y <= mouse_y <= bot_vs_bot_y + bot_vs_bot_text.get_height():
                    return "bot_vs_bot"  # Bot vs Bot selected
        await asyncio.sleep(0)


def button_info(screen):
    note_font = p.font.SysFont("helvetica", 18, True, False)
    
    # Hotkey text and their corresponding flags
    hotkey_actions = {
        "U: Undo": "undo_flag",
        "L: Load": "load_flag",
        "S: Save": "save_flag",
        "E: Exit": "exit_flag",
        "R: Reset": "reset_flag"
    }
    
    # Starting position for the text (bottom-right corner)
    x, y = screen.get_width() - 10, screen.get_height() - 10
    
    # Store button dimensions (x, y, width, height) for each action
    button_dimensions = {}

    # Render each line of the hotkey text and make clickable
    for action, flag in hotkey_actions.items():
        text_surface = note_font.render(action, True, (255, 255, 255))  # Render the text
        text_rect = text_surface.get_rect()
        
        # Set position for text
        text_rect.bottomright = (x, y)
        
        # Create a semi-transparent background rectangle
        box_rect = text_rect.inflate(10, 5)  # Slightly larger than the text
        box_rect.bottomright = text_rect.bottomright
        
        # Store button dimensions (x, y, width, height)
        button_dimensions[flag] = box_rect
        
        # Draw the semi-transparent box (button background)
        semi_transparent_surface = p.Surface((box_rect.width, box_rect.height))
        semi_transparent_surface.set_alpha(25)  # 10% opacity
        semi_transparent_surface.fill((255, 255, 255))  # White color
        screen.blit(semi_transparent_surface, box_rect.topleft)  # Draw the box on screen
        
        # Draw the text on the screen
        screen.blit(text_surface, text_rect)
        
        # Move the y-position up for the next line
        y -= box_rect.height + 5  # Add spacing between options
    
    return button_dimensions



async def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    flags = {
        "save_flag": False,
        "load_flag": False,
        "undo_flag": False,
        "reset_flag": False,
        "exit_flag": False
    }

    # Display title screen and set player mode
    game_mode = await title_screen(screen)

    # Set player types based on game mode
    if game_mode == "single":
        player_one = True  # Player one is human
        player_two = False  # Player two is AI (bot)
    elif game_mode == "multi":
        player_one = True  # Player one is human
        player_two = True  # Player two is also human
    elif game_mode == "bot_vs_bot":
        player_one = False  # Player one is bot
        player_two = False  # Player two is also bot

    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False
    animate = False
    loadImages()
    running = True
    square_selected = ()
    player_clicks = []
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)


    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()

                        # Check for mouse click and update flags based on button dimensions
            if e.type == p.MOUSEBUTTONDOWN and e.button == 1:  # Left-click
                mouse_pos = p.mouse.get_pos()
                button_dimensions = button_info(screen)
                
                # Check if the mouse is inside any button's rectangle
                for flag, rect in button_dimensions.items():
                    if rect.collidepoint(mouse_pos):
                        flags[flag] = True  # Set the corresponding flag to True
            # mouse handler
            if e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_s:  # Save the game when 'S' is pressed
                    game_state.saveGame()
                    print("Game saved!")

                if e.key == p.K_l:  # Load the game when 'L' is pressed
                    try:
                        game_state.loadGame()
                        valid_moves = game_state.getValidMoves()  # Recalculate valid moves after loading
                        square_selected = ()  # Reset the selection state
                        player_clicks = []    # Reset player clicks
                        move_made = False     # No move has been made immediately after loading
                        animate = False       # No animation to process
                        game_over = False     # Reset game over state
                        print("Game loaded!")
                    except FileNotFoundError:
                        print("No saved game found! Press 'S' to save a game first.")
                if e.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_e:  # Exit and return to title screen when 'E' is pressed
                        # Display title screen and set player mode
                    game_mode = await title_screen(screen)

                    # Set player types based on game mode
                    if game_mode == "single":
                        player_one = True  # Player one is human
                        player_two = False  # Player two is AI (bot)
                    elif game_mode == "multi":
                        player_one = True  # Player one is human
                        player_two = True  # Player two is also human
                    elif game_mode == "bot_vs_bot":
                        player_one = False  # Player one is bot
                        player_two = False  # Player two is also bot
                    game_state = ChessEngine.GameState()  # Reset the game state
                    valid_moves = game_state.getValidMoves()  # Recalculate valid moves after reset
                    square_selected = ()  # Reset selected square
                    player_clicks = []  # Reset player clicks
                    move_made = False  # No move has been made immediately after reset
                    animate = False  # No animation to process
                    game_over = False  # Reset game over state
                    ai_thinking = False  # Reset AI thinking state
                    move_undone = False  # Reset move undone state

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                # Calculate the AI move directly in the main thread
                ai_move = ChessAI.findBestMove(game_state, valid_moves)
                if ai_move is None:
                    ai_move = ChessAI.findRandomMove(valid_moves)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                await animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if not game_over:
            drawMoveLog(screen, game_state, move_log_font)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stalemate:
            game_over = True
            drawEndGameText(screen, "Stalemate")

        if flags["save_flag"]:
            game_state.saveGame()
            print("Game saved!")
            flags["save_flag"] = False 

        if flags["load_flag"]:  # Load the game when 'L' is pressed
            try:
                flags["load_flag"] = False
                game_state.loadGame()
                valid_moves = game_state.getValidMoves()  # Recalculate valid moves after loading
                square_selected = ()  # Reset the selection state
                player_clicks = []    # Reset player clicks
                move_made = False     # No move has been made immediately after loading
                animate = False       # No animation to process
                game_over = False     # Reset game over state
                print("Game loaded!")
            except FileNotFoundError:
                print("No saved game found! Press 'S' to save a game first.")
        if flags["undo_flag"]:  # undo when 'z' is pressed
            flags["undo_flag"] = False
            game_state.undoMove()
            move_made = True
            animate = False
            game_over = False
            if ai_thinking:
                move_finder_process.terminate()
                ai_thinking = False
            move_undone = True
        if flags["reset_flag"]:  # reset the game when 'r' is pressed
            flags["reset_flag"] = False
            game_state = ChessEngine.GameState()
            valid_moves = game_state.getValidMoves()
            square_selected = ()
            player_clicks = []
            move_made = False
            animate = False
            game_over = False
            if ai_thinking:
                move_finder_process.terminate()
                ai_thinking = False
            move_undone = True
        if flags["exit_flag"]:   # Exit and return to title screen when 'E' is pressed
                # Display title screen and set player mode
            flags["exit_flag"] = False
            game_mode = await title_screen(screen)

            # Set player types based on game mode
            if game_mode == "single":
                player_one = True  # Player one is human
                player_two = False  # Player two is AI (bot)
            elif game_mode == "multi":
                player_one = True  # Player one is human
                player_two = True  # Player two is also human
            elif game_mode == "bot_vs_bot":
                player_one = False  # Player one is bot
                player_two = False  # Player two is also bot
            game_state = ChessEngine.GameState()  # Reset the game state
            valid_moves = game_state.getValidMoves()  # Recalculate valid moves after reset
            square_selected = ()  # Reset selected square
            player_clicks = []  # Reset player clicks
            move_made = False  # No move has been made immediately after reset
            animate = False  # No animation to process
            game_over = False  # Reset game over state
            ai_thinking = False  # Reset AI thinking state
            move_undone = False  # Reset move undone state

        button_info(screen)
        clock.tick(MAX_FPS)
        p.display.flip()
        await asyncio.sleep(0)


def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawMoveLog(screen, game_state, font):
    """
    Draws the move log.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


async def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)



if __name__ == "__main__":
    asyncio.run(main())
