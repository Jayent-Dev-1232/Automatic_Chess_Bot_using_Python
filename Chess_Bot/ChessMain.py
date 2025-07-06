"""
This is the main driver file. It will be responsible for handling user input and displaying the current GameState.
"""
import pygame as p

from Chess_Bot import ChessEngine

# 400 is a good choice for having high resolution and high quality
WIDTH = HEIGHT = 512
# Dimension of a chess board is 8X8.
DIMENSION = 8
# The square size of one block in the chess board is width or height by dimension
SQ_SIZE = HEIGHT // DIMENSION
# Maximum FPS is used later on in animations.
MAX_FPS = 15
IMAGES = {}

"""
Initializing a global directory for images and remember this will be called exactly once.
"""
def load_images():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # NOTE : We can access an image by saying "IMAGES['wp']"


"""
This the main driver for our code. This will handle all user input and updating the graphics.
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    # Flag variable for when a move is made.
    move_made = False
    print(gs.board)
    # This can be run once before the while loop.
    load_images()
    running = True
    # No particular square is selected, it just keeps track of the last click of the user. (tuple : (row, col))
    sq_selected = ()
    # This keeps track of players click. ( two tuples : [(6,4) first click on pawn and then (4,4) to move the pawn to this square.])
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                # This gives the (x, y) location of the mouse.
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                # If the player selects the same square twice then it should be deselected.
                if sq_selected == (row, col):
                    # This is a deselector function.
                    sq_selected = ()
                    # This clears any clicks stored in the list and resets it.
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    # Appends the click location for both 1st and 2nd clicks into the list.
                    player_clicks.append(sq_selected)
                # After the player has made two clicks
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    # Print the starting square and ending square moves in Rank-File notations.
                    print(move.get_chess_notation())
                    # Makes the move after getting starting square and ending square location.
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        # Resets all the clicks made to empty to take other moves input.
                        sq_selected = ()
                        player_clicks = []
                    else:
                        player_clicks = [sq_selected]
            # Key Handlers
            elif e.type == p.KEYDOWN:
                # Undo the move when 'z' is pressed.
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Responsible for all the graphics within a current Game State.
"""
def draw_game_state(screen, gs):
    # Draw squares on the board.
    draw_board(screen)
    # Draw pieces on the top of the board.
    draw_pieces(screen, gs.board)

"""
Draw squares on the board. Remember that the top left corner of the chess board from both black and white side is light colored square.
"""
def draw_board(screen):
    colors = [p.Color("white"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draw the pieces on the board using current GameState.board
"""
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()