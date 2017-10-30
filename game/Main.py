import sys

from pygame.locals import *

from game.Board import *
from game.constants import *


class Main:

    def __init__(self):
        pygame.init()  # Initiate Pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game of Life")
        self.board = Board(self.screen)
        self.running = True  # Start process as running so game loop begins
        self.paused = True  # Start game paused
        self.run()  # Game loop

    def run(self):
        while self.running:  # Check that the game is running
            for event in pygame.event.get():
                if event.type == QUIT:  # If window closed, end process
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # If 'Enter' key clicked, toggle whether game is paused
                        if self.paused:
                            self.paused = False
                        else:
                            self.paused = True
                    if event.key == pygame.K_BACKSPACE: # If 'Backspace' key clicked, step forward one iteration
                        self.board.check_gen()
                    if event.key == pygame.K_TAB:  # DEBUG FEATURE: Tab key will display (in console) how many alive neighbors the hovered-over cell has
                        x, y = pygame.mouse.get_pos()
                        for row in range(0, DIMENSIONS):
                            for col in range(0, DIMENSIONS):
                                if self.board.tiles[row][col].rect.collidepoint(x, y):
                                    print(self.board.num_alive_neighbors(self.board.tiles, row, col))
                if event.type == MOUSEBUTTONDOWN:  # Will set hovered-over cell to 'alive'
                    x, y = event.pos
                    for row in self.board.tiles:
                        for tile in row:
                            if tile.rect.collidepoint(x, y):
                                tile.occupied = True
            self.next_gen()  # Draw screen once per cycle

    def next_gen(self):
        self.screen.fill((0, 0, 0)) # Cover screen with black
        self.board.render_tiles() # Render tiles
        if not self.paused:  # Game is still technically running when paused. Only move forward iterations if not paused.
            self.board.check_gen()  # Step forward one iteration per cycle, if not paused
        pygame.display.update()  # Redraw screen

m = Main()
