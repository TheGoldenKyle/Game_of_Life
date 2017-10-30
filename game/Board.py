from random import *
from threading import Thread

import pygame

from game.Tile import *
from game.constants import *


class Board:

    def __init__(self, screen):
        self.screen = screen
        self.rows, self.columns, self.num_tiles = DIMENSIONS, DIMENSIONS, DIMENSIONS * DIMENSIONS  # Only set for square boards at the moment
        self.white_texture, self.black_texture, self.full_texture = None, None, None
        self.tile_locations_set = False
        self.tiles = list()
        self.create_tiles()
        self.pick_starting_randoms()

    def next_gen(self):
        self.render_tiles()
        self.check_gen()

    def create_tiles(self):
        for row in range(0, DIMENSIONS):
            row_list = list()
            for col in range(0, DIMENSIONS):
                tile = Tile()
                row_list.append(tile)
            self.tiles.append(row_list)

    def render_tiles(self):
        for row in range(0, DIMENSIONS):
            for col in range(0, DIMENSIONS):
                if self.tiles[row][col].occupied:
                    pygame.draw.rect(self.screen, (255, 255, 255), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                if not self.tile_locations_set:
                    self.tiles[row][col].rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.tiles[row][col].row = row
                    self.tiles[row][col].col = col

    def check_gen(self):  # Decides the state of each tile for the next iteration
        temp_list = list()
        self.check_neighbors()
        for row in range(0, DIMENSIONS):
            row_list = list()
            for col in range(0, DIMENSIONS):
                tile = self.tiles[row][col]
                alive_neighbors = tile.neighbors
                if tile.occupied:
                    if not (alive_neighbors == 2 or alive_neighbors == 3):
                        dead_tile = Tile()
                        row_list.append(dead_tile)
                    else:
                        alive_tile = Tile()
                        alive_tile.occupied = True
                        row_list.append(alive_tile)
                else:
                    if alive_neighbors == 3:
                        alive_tile = Tile()
                        alive_tile.occupied = True
                        row_list.append(alive_tile)
                    else:
                        dead_tile = Tile()
                        row_list.append(dead_tile)
            temp_list.append(row_list)
        self.tiles = temp_list

    def check_neighbors(self):
        split_tiles_list = self.chunks(self.tiles, THREADS)
        for i in range(0, THREADS):
            thread = Thread(target=self.check_neighbors_from_list, args=(self.tiles, split_tiles_list[i]))
            thread.start()

    def chunks(self, seq, num):  # For Multithreading: Break board into chunks
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out

    def check_neighbors_from_list(self, tiles_array, tiles_to_check): # Sets each tile's neighbors attribute to number of alive neighbors
        for row in tiles_to_check:
            for tile in row:
                row, col = tile.row, tile.col
                tile.neighbors = self.num_alive_neighbors(tiles_array, row, col)

    def num_alive_neighbors(self, tiles_array, row, col):  # Returns number of alive neighbors of cell at (row, col) in 2D Matrix (list)
        alive_neighbors = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if DIMENSIONS > i >= 0 and DIMENSIONS > j >= 0 and not (i == row and j == col) and tiles_array[i][j].occupied:
                    alive_neighbors += 1
        return alive_neighbors

    def pick_starting_randoms(self):  # Generates starting alive cells randomly
        chosen = list()  # Holds list of all tiles to randomly set as 'alive' on game start
        while len(chosen) < int(self.num_tiles*PERCENTAGE_STARTING_RANDOM/100):
            rand = randint(0, self.num_tiles - 1)  # Generates a random index (0, num_tiles - 1)
            if rand not in chosen:  # Make sure the same tile isn't chosen twice
                chosen.append(rand)
        i = 0
        for row in self.tiles:  # Sets chosen tiles to 'occupied'
            for tile in row:
                if i in chosen:
                    tile.occupied = True
                i += 1

    def render_fps(self, fps): # Renders FPS in top left corner (Right of Player score)
        self.screen.blit(fps, (10, 10))
