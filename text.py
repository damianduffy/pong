import pygame

pygame.init()

font = pygame.font.SysFont("monospace", 15)
msg_colour = (255,255,0)
bold = 0                                        # 0=normal, 1=bold

def centre_text(message, SCREENSIZE):
    # IMPROVE - make ASCII type message box for information to be presented in
    return (SCREENSIZE[0] // 2 - message.get_rect().width // 2, SCREENSIZE[1] // 2 - message.get_rect().height)

msg_exit = font.render("Are you sure you want to quit? [y/n] Or would you rather start a new game? [space]", bold, msg_colour, (255,0,0))
msg_pause = font.render("Game paused.  Press [p] to resume.", bold, msg_colour, (255,0,0))
msg_score = font.render("Someone SCORED!!!!", bold, msg_colour, (255,0,0))
msg_newgame = font.render("Would you like to play a game? [y/n]", bold, msg_colour, (255,0,0))

# function for rendering dialogue boxes.  Text is passed and a formated dialogue box is returned
def dialogue(message):
    msg_len = message.get_rect().width
