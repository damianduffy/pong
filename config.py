# Main configuration file for game
# global game settings configured from here

# Set game values
SCREENSIZE      = [640, 360]            # Game resolution
FULLSCREEN      = False                 # Window or fullscreen
SOUND           = False                 # All sound on or off
SCROLL_MAP      = True
TILESIZE        = 16
TITLE           = "Pong"
FPS             = 30                    # how fast the game runs
INTERFACE_WIDTH = TILESIZE * 10
SPEED           = 4                     # Default speed for puck
PUCK_SIZE       = [20, 20]              # Default puck size
CENTRE_PUCK     = [(SCREENSIZE[0] // 2) - (PUCK_SIZE[0] // 2), (SCREENSIZE[1] // 2) - (PUCK_SIZE[1] // 2)]
PADDLE_SPEED    = 10                    # How fast can the paddles slide
PADDLE_SIZE     = [20, 80]              # default paddle size

# Colours
BLACK           = (0,0,0)
WHITE           = (255,255,255)
RED             = (255,0,0)
LIME            = (0,255,0)
BLUE            = (0,0,255)
YELLOW          = (255,255,0)
AQUA            = (0,255,255)
MAGENTA         = (255,0,255)
SILVER          = (192,192,192)
GRAY            = (128,128,128)
MAROON          = (128,0,0)
OLIVE           = (128,128,0)
GREEN           = (0,128,0)
PURPLE          = (128,0,128)
TEAL            = (0,128,128)
NAVY            = (0,0,128)
