import pygame
from tkinter import *

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   screen = pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Pong')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface, screen)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface, screen):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object
      self.root = self.initialize_window("Menu", "300x325")
      self.game_mode = None
      self.surface = surface
      self.screen = screen
      self.bg_color = pygame.Color('black')
      self.game_Clock = pygame.time.Clock()
      self.FPS = 60
      self.close_clicked = False
      self.continue_game = True
 
      self.paddles = {'left': Paddle(self.surface, 'white', 100, 200, 10, 50, [0,5], True), 'right': Paddle(self.surface, 'white', 400, 200, 10, 50, [0,5], True), 'bot':Paddle(self.surface, 'white', 400, 200, 10, 50, [0,5], False)}
      self.ball = Ball('white', 7, [250, 200], [5, 5], self.surface, self.paddles['right'])
      self.game_score = {'left': 0, 'right': 0}
      self.paddle_input = {'left':(pygame.K_q, pygame.K_a), 'right':(pygame.K_p, pygame.K_l)}
      self.text_font = pygame.font.SysFont('Comic Sans', 72)
      self.text_color = (255,255,255)


   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.
      self.menu() # the player choses single or multiplayer
      self.set_paddles()

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def initialize_window(self, title, size):
      # initializes tkinter window
      # - self is the window
      # - title is the windows title 
      # - size is the length x width of the window
      root = Tk()
      root.title(title)
      root.geometry(size)
      root.resizable(0, 0)
      root.config(bg='#23272A')
      return root

   def set_mode(self, mode):
      # Sets the gamemode and destroys the menu
      # - self is the game
      # - mode is the chosen gamemode
      self.game_mode = mode
      self.root.destroy()

   def set_paddles(self):
      # Sets the paddles based on the game mode
      # - self is the game where the paddles are located
      self.left_paddle = self.paddles['left']
      if self.game_mode == 'multiplayer':
         self.right_paddle = self.paddles['right']
      elif self.game_mode == 'singleplayer':
         # in singleplayer right paddle becomes a bot
         self.right_paddle = self.paddles['bot']
      
   def menu(self):
      # Creates the widgets on the menu
      # - self is the menu window
      Label(self.root, text="Left Paddle: Q and A to move", pady=5, bg='#99AAB5').grid(row=0, pady=5)
      Label(self.root, text="Right Paddle: P and L to move", pady=5, bg='#99AAB5').grid(row=1, pady=5)
      Label(self.root, text="First to 11 Wins!", pady=5, bg='#99AAB5').grid(row=2, pady=5)
      single_player_button = Button(self.root, text='Singleplayer', font='Arial', padx=35, pady=25, bg='#99AAB5', activebackground='#2C2F33', command=lambda: self.set_mode('singleplayer'))
      multiplayer_player_button = Button(self.root, text='Local Multiplayer', font='Arial', padx=20, pady=25, bg='#99AAB5', activebackground='#2C2F33', command=lambda: self.set_mode('multiplayer'))

      single_player_button.grid(row=3, padx=70, pady=15)
      multiplayer_player_button.grid(row=4)

      self.root.mainloop()
   
   def score_text(self, text_string, text_font, text_color, text_pos):
      # Creates a text to be displayed on the screen 
      # - self is the Game that the text is being displayed
      # - text_string is the string being displayed
      # - text_font is the font and the size of the text
      # - text_color is the color of the text
      # - text_pos is the position of the text

      text_image = text_font.render(text_string, True , text_color)
      self.screen.blit(text_image, text_pos)

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True

   def player_points(self):
      # Calculates and displays both players points 
      # - self is the Game to display points
      
      # if ball hits right side then add point to left player and vice versa
      if (self.ball.center[0] == 500):
         self.game_score['left'] += 1

      if (self.ball.center[0] == 0):
         self.game_score['right'] += 1
      
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      self.surface.fill(self.bg_color) # clear the display surface first

      # display left players points
      self.score_text(str(self.game_score['left']), self.text_font, self.text_color, (30,10))
      # display right players points
      self.score_text(str(self.game_score['right']), self.text_font, self.text_color, (445,10))

      # draw game objects
      self.ball.draw()
      self.left_paddle.draw()
      self.right_paddle.draw()

      # draw players points
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      # check if ball hits the paddle
      self.ball.bounce(self.left_paddle, self.right_paddle)

      # move the ball and keeps it in bounds
      self.ball.move()
      self.player_points()

      # moves paddles from user input
      self.left_paddle.move(self.paddle_input['left'])
      self.right_paddle.move(self.paddle_input['right'], self.ball.get_center()[1])


   def decide_continue(self):
      # Check and remember if the game should continue
      # End game is score is above 10
      # - self is the Game to check

      if self.game_score['left'] > 10 or self.game_score['left'] > 10:
         self.continue_game = False


class Ball:
   # An object in this class represents the ball in the game 
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface, paddle):
      # Initialize a Ball.
      # - self is the Ball to initialize
      # - color is the pygame.Color of the ball
      # - radius is the int pixel radius of the ball
      # - center is a list containing the x and y int
      #   coords of the center of the ball
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object
      # - paddle is the paddle the the ball bounces off of

      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
      self.paddle = Paddle
      self.screen_size = self.surface.get_size()
      
   def move(self):
      # Change the location of the Ball by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # if ball hits borders then change direction
      # - self is the Ball to move
      for i in range(0,2):
         # move ball 
         self.center[i] += self.velocity[i]
         # if ball hits border change x or y velocity
         if (self.center[i] == 0 or self.center[i] == self.screen_size[i]):
            self.velocity[i] = -self.velocity[i]

   def draw(self):
      # Draw the ball on the surface
      # - self is the Ball to draw
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)

   def bounce(self, paddle1, paddle2):
      # check if ball collides with paddle and if so then multiply the x value of the balls velocity by -1
      # - self is the Ball to bounce
      # - paddle1 is the left paddle
      # - paddle2 is the right paddle

      if (paddle1.check_collision(self.center) and self.velocity[0] == -abs(self.velocity[0])):
         self.velocity[0] = -self.velocity[0]

      if (paddle2.check_collision(self.center) and self.velocity[0] == abs(self.velocity[0])):
         self.velocity[0] = -self.velocity[0]

   def get_center(self):
      return self.center


class Paddle:
   # An object in this class represents the players paddles
   
   def __init__(self, paddle_surface, paddle_color, x, y, width, height, paddle_velocity, user):
      # Initialize a Paddle.
      # - self is the Paddle to be initialized
      # - paddle_surface is the window's pygame.Surface object
      # - paddle_color is the pygame.Color of the paddle
      # - x,y,width,height is the pygame rect parameters
      # - paddle_velocity is the speed at which the paddle moves
      # - user is a bool determining if their is a user or a bot

      self.surface = paddle_surface
      self.color = pygame.Color(paddle_color)
      self.rect = pygame.Rect(x,y,width,height)
      self.velocity = paddle_velocity
      self.user = user

   def draw(self):
      # Draw the paddle to the screen
      # - self is the Paddle to be drawn
      pygame.draw.rect(self.surface, self.color, self.rect)

   def move(self, paddle_input, ball_y=1):
      # Takes in user input and moves the paddle up or down the y-axis
      # - self is the Paddle to be moved
      # - paddle_input is the up and down keyboard input for the paddle stored in a list
      # - ball_y is the y position of the game ball, this is used for singleplayer gamemode where there is an AI

      if self.user:
         # move up
         if (pygame.key.get_pressed()[paddle_input[0]]):
            self.rect = self.rect.move(self.velocity[0], -self.velocity[1])

         # move down
         if (pygame.key.get_pressed()[paddle_input[1]]):
            self.rect = self.rect.move(self.velocity[0], self.velocity[1])
      else:
         # Move bot based on position of ball, this creates an unbeatable AI
         self.rect.y = ball_y

      # check if top is in bounds
      if (self.rect.top <= 0):
         self.rect.top = 0

      # check if bottom is in bounds
      if (self.rect.bottom >= 400):
         self.rect.bottom = 400

   def check_collision(self, point):
      # Checks if a point is inside the paddle
      # - self is the paddle to be checked
      # - point is the x,y coordinate being checked 
      collision = self.rect.collidepoint(point)
      return collision

main()