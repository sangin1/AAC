import pygame

for i in range(0, pygame.joystick.get_count()):
     gamepads.append(pygame.joystick.Joystick(i))
     gamepads[-1].init()
     gamepadInfo = basicfont.render("Detected joystics: " + gamepads[-1].get_name(), True, (0,0,0))
     gamepadInfo2 = basicfont.render("Button: " + str(gamepads[-1].get_numbuttons()), True, (0,0,0))
     gamepadInfo3 = basicfont.render("Stick: " + str(gamepads[-1].get_numaxes()), True, (0,0,0))

while(True):
    for i in range(0, pygame.joystick.get_count()):
        if gamepads[-1].get_button() == True:
            print(i+'번 누름')
