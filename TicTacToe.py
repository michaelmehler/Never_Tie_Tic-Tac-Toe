import pygame 
import sys
import random
from Linked_List import Linked_List 

WINDOW_SIZE = 825 
CELL_SIZE = WINDOW_SIZE // 3
INF = float('inf') #using this instead of None as it allows for adding up the values in the grid 
vec2 = pygame.math.Vector2 #creates an alias name for the Vector2 object that is a two-d array specific to pygame
CELL_CENTER = vec2(CELL_SIZE / 2) 

class TicTacToe:

    def __init__(self, game: 'Game'): #the : 'Game' makes it so the paramater game can only be of type Game and the apostrophes inidcate that the Game class has not been defined but is defined down below
        self.game = game 
        self.board_image = self.get_scaled_image(path='board.png', resolution=[WINDOW_SIZE] * 2) 
        self.x_image = self.get_scaled_image(path='x.png', resolution= [CELL_SIZE] * 2) 
        self.o_image = self.get_scaled_image(path='o.png', resolution=[CELL_SIZE] * 2)
        self.game_arr = [[INF, INF, INF], #creates a data structure for the board that will store the game pieces
                         [INF, INF, INF], #will be made up of 0s and 1s
                         [INF, INF, INF]] 
        self.player = random.randint(0,1) #selects randomly what player will start first 
        self.line_indices_array = [[(0,0), (0,1), (0,2)], #creates an array that holds eight lists that contain the three coordinates that form a winning line
                                   [(1,0), (1,1), (1,2)], 
                                   [(2,0), (2,1), (2,2)],
                                   [(0,0), (1,0), (2,0)],
                                   [(0,1), (1,1), (2,1)],
                                   [(0,2), (1,2), (2,2)],
                                   [(0,0), (1,1), (2,2)],
                                   [(0,2), (1,1), (2,0)]] 
        self.winner = None
        self.font = pygame.font.SysFont('Verdana', CELL_SIZE // 4, True)
        self.piece_tracker = Linked_List() 
        
    def check_winner(self):
        for line_indices in self.line_indices_array: #iterates over the array holding the eight lists of tuples in a line
            sum_line = sum([self.game_arr[i][j] for i, j in line_indices]) #calculates the sum of the values on the game board at the tuples in the line list 
            if sum_line == 0:       #This portion of code checks if the sum_line is equal to 0 or 3 as this two values indicated that
                self.winner = 'O'   #on the board there were three 0s or 1s in a row forming a line indicating a winner 
                self.winner_line = [vec2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER, 
                                    vec2(line_indices[2][::-1]) * CELL_SIZE + CELL_CENTER] 
            if sum_line == 3:       #Since X is denoted on the board by the value 1 then a value of 3 indicates a win for X
                self.winner = 'X' 
                self.winner_line = [vec2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER, #creates a variable that holds two 2D vectors that indicate the 
                                    vec2(line_indices[2][::-1]) * CELL_SIZE + CELL_CENTER] #start and end points of the winner line 

    def run_game_process(self):
        current_cell = vec2(pygame.mouse.get_pos()) // CELL_SIZE #gets position of the mouse and creates a 2d vector of the mouse position which is adjusted to fit in the cell by being divided by CELL_SIZE
        col, row = map(int, current_cell) #creates a col and row variable holding the respective indexes of where the mouse is 
        left_click = pygame.mouse.get_pressed()[0] #boolean variable - is true if mouse is clicked and false if not
        if left_click and self.game_arr[row][col] == INF and not self.winner: #checks left_click is true and the grid cell is empty
            self.game_arr[row][col] = self.player #updates the cell to be the value of player (either true or false) which indicates that a player has made a move in that cell
            self.player = not self.player #assigns player to be the oposite boolean value indicating it is the other players turn
            self.piece_tracker.append_element((row,col)) 
        self.check_winner() 
        if len(self.piece_tracker) == 9 and self.winner == None:
            row, col = self.piece_tracker.get_element_at(0)
            self.piece_tracker.remove_element_at(0) 
            self.game_arr[row][col] = INF  
    
    def draw_objects(self):
        for y, row in enumerate(self.game_arr):
            for x, obj in enumerate(row):
                if obj != INF: 
                    self.game.screen.blit(self.x_image if obj else self.o_image, vec2(x,y) * CELL_SIZE) # puts the correct image onto the board and in the correct place
     
    def draw_winner(self):
        if self.winner: #  where line goes    color   start and end points   width of line 
            pygame.draw.line(self.game.screen, 'green', *self.winner_line, CELL_SIZE // 8) 
            label = self.font.render(f'Player {"XO"[self.player]} wins!', True, 'white', 'black')
            self.game.screen.blit(label, (WINDOW_SIZE // 2 - label.get_width() // 2, WINDOW_SIZE // 4)) 

    def draw(self):
        self.game.screen.blit(self.board_image, (0,0)) 
        self.draw_objects() 
        self.draw_winner()  

    @staticmethod
    def get_scaled_image(path, resolution):
        image = pygame.image.load(path) #loads the specified image in as a image in the pygame 
        return pygame.transform.smoothscale(image, resolution) #scales the image's resolution to fit the pygame  
    
    def print_caption(self):
        if self.winner != None:
            pygame.display.set_caption(f'Press the Space to Play Again!') 
        else:
            pygame.display.set_caption(f'Player "{"OX"[self.player]}" Turn!') #set_caption method displays text at top of screen and the f-string allows self.player to evaluate if it will dispaly an X or an O

    def run(self): 
        self.print_caption()
        self.draw() 
        self.run_game_process() 

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE)) #creates a variable that controles the size of the display screen
        self.clock = pygame.time.Clock() #creates a variable that will be used to help control the game's speed and framerate
        self.tic_tac_toe = TicTacToe(self) 

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)

    def check_events(self):
        for event in pygame.event.get(): #loops over all the events in the event queue (events being clicks/mouse movements)
            if event.type == pygame.QUIT: #This if statement will end the game once a quit event is reached in the queue
                pygame.quit() #shuts down pygame when done game is finished
                sys.exit() #exits the program when game is finished 
            if event.type == pygame.KEYDOWN: #checks if a key was pressed
                if event.key == pygame.K_SPACE: #checks if the key pressed was the space bar 
                    self.new_game() 

    def run(self):
        while True:
            self.tic_tac_toe.run() 
            self.check_events()
            pygame.display.update() #updates the screen after the game events are processed
            self.clock.tick(60) #sets the game to run at 60 frames per second 


if __name__ == '__main__':
    game = Game()
    game.run()
