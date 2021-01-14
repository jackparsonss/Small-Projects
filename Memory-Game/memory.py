# A game which has 16 tiles with 8 unique tiles, user clicks the tiles to flip over and tries to match the two identical ones
import pygame,random

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((520, 425))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

  def __init__(self, surface):
    # Initialize a Game.
    # - self is the Game to initialize
    # - surface is the display window surface object

    # === objects that are part of every game that we will discuss
    self.surface = surface
    self.bg_color = pygame.Color('black')
    self.game_Clock = pygame.time.Clock()
    self.FPS = 60
    self.close_clicked = False
    self.continue_game = True
      
    # === game specific objects
    self.score = 0
    self.amt_of_tiles = 16
    self.tiles_names = self.create_tile_names()
    self.tile_positions = [(5,5), (110,5), (215,5), (320,5), (5,110), (110,110), (215,110), (320,110), (5,215), (110,215), (215,215), (320,215), (5,320), (110,320), (215,320), (320,320)]
    self.shuffle(self.tile_positions)
    self.tiles = self.create_tiles(self.tiles_names)
    self.correct = []

  def shuffle(self, alist):
    # Randomly shuffles items
    # - self is the Game in which the tiles get randomly placed
    # - alist are the items being shuffled
    random.shuffle(alist)

  def create_tile_names(self):
    # Creates a list of all the different photo names strings
    # - self is the Game in which the names will be used
    names = []
    for i in range(1, 9):
      names.append("image"+str(i)+".bmp")
    return names * 2

  def create_tiles(self, tile_names):
    # Creates all 16 game tiles
    # - self is the Game where the tiles are being created
    # - tile_names are the different photo image strings
    tiles = []
    for i in range(self.amt_of_tiles):
      tiles.append(Tile(self.tiles_names[i], "image0.bmp", self.surface, self.tile_positions[i]))
    return tiles

  def play(self):
    # Play the game until the player presses the close box.
    # - self is the Game that should be continued or not.
    while not self.close_clicked:  # until player clicks close box
      # play frame
      self.handle_events()
      self.draw()            
      if self.continue_game:
        self.update()
        self.decide_continue()
      self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

  def handle_events(self):
    # Handle each user event by changing the game state appropriately.
    # - self is the Game whose events will be handled
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        self.close_clicked = True
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        for tile in self.tiles:
          if tile.rect.collidepoint(mouse_pos):
            tile.flip()

  def draw(self):
    # Draw all game objects.
    # - self is the Game to draw
    self.surface.fill(self.bg_color) # clear the display surface first
    self.draw_score()
    for i in range(self.amt_of_tiles):
      self.tiles[i].draw(self.tile_positions[i])

    pygame.display.update() # make the updated surface appear on the display

  def draw_score(self):
      # draw game score
      # - self is the score to draw

      # move text as score increases
      location = (415,0)
      if self.score < 10:
        location = (470,0)
      elif self.score < 100:
        location = (440,0)

      font_size = 68
      fg_color = pygame.Color('white')
      string = str(self.score)
      font = pygame.font.SysFont('Times New Roman', font_size)
      text_box = font.render(string, True, fg_color)
      self.surface.blit(text_box, location)

  def correct_tiles(self, two_tiles):
    # Checks two tiles and sees if they are the same
    # - self is the Game where the tiles exist
    # - two_tiles are the two tiles being compared
    if two_tiles[0].check_image() == two_tiles[1].check_image():
      for i in range(2):
        self.correct.append(two_tiles[i])
      two_tiles = []

  def incorrect_tiles(self, check_tiles):
    # Takes in tiles and flips them back over if they are not the same
    # - self is Game where the tiles exist
    # - check_tiles are the tiles being flipped back over
    for tile in check_tiles:
      if tile not in self.correct:
        pygame.time.wait(500)
        tile.unlfip()

  def two_flipped(self):
    # Checks if the two cards flipped are the same
    # if not then flip both back over
    # - self is the Game to check if tiles are flipped
    flipped = []
    for tile in self.tiles:
      # if tile is flipped and not already correct then add tile to temp variables
      if tile.is_exposed() and tile not in self.correct:
        flipped.append(tile)
    # once two tiles are flipped check if the same or else flip back over
    if len(flipped) == 2:   
      # add both tiles to correct
      self.correct_tiles(flipped)
      # unflip tiles
      self.incorrect_tiles(flipped)

  def update(self):
    # Update the game objects for the next frame.
    # - self is the Game to update
    self.two_flipped()
    self.score = pygame.time.get_ticks() // 1000

  def decide_continue(self):
    # Check and remember if the game should continue
    # - self is the Game to check
    amt_exposed = 0
    for tile in self.tiles:
      if tile.is_exposed() == True:
        amt_exposed+=1
      if amt_exposed == self.amt_of_tiles:
        self.continue_game = False
    

class Tile:
  # An object in this class represents a single tile

  def __init__(self, tile_image, flipped_image, surface, position):
    # Initialize a Tile.
    # - self is the Tile to be initialized
    # - tile_image is the string name of the image tile
    # - flipped_image is default image seen
    # - surface is the screen in which tiles get drawn onto
    # - position is a tuple of the top left corner of each tile
    self.tile_image = tile_image
    self.flipped_image = pygame.image.load(flipped_image)
    self.surface = surface
    self.position = position
    self.exposed = False
    self.image = pygame.image.load(tile_image)
    self.current = [self.flipped_image, self.image]
    self.clicked = 0 # 0 is default image, 1 is tile_image
    self.rect = pygame.Rect(position[0], position[1], 100, 100)

  def flip(self):
    # Flips the tile from default image to tile_image
    # - self is the Tile to be flipped
    self.clicked = 1
    self.exposed = True

  def unlfip(self):
    # Flips the tile from tile_image to default
    # - self is the Tile to be unflipped
    self.clicked = 0
    self.exposed = False

  def is_exposed(self):
    # Returns a bool checking which side of the tile is exposed
    # - self is the Tile being checked
    return self.exposed

  def check_image(self):
    # Returns a string of the name of the tile_image
    # - self is the Tiles name being checked
    return self.tile_image

  def draw(self, pos):
    # Draws the tile onto the screen
    # - self is the tile being drawn
    # - pos is the position where the tile is being draw
    self.surface.blit(self.current[self.clicked], pos)

main()