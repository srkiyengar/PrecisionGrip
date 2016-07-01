__author__ = 'srkiyengar'

import pygame
import logging
import logging.handlers
from datetime import datetime
import reflex
import screen_print as sp
import joystick as js


POS_ERROR = 20

#logger
LOG_LEVEL = logging.DEBUG
LOG_FILENAME = 'PrecisionGrabber' + datetime.now().strftime('%Y-%m-%d---%H:%M:%S')

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

SCAN_RATE = 20           #1(one) second divided by scan rate is the loop checking if the main program should die


if __name__ == '__main__':

    # Set up a logger with output level set to debug; Add the handler to the logger
    my_logger = logging.getLogger("My_Logger")
    my_logger.setLevel(LOG_LEVEL)
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=2000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    # end of logfile preparation Log levels are debug, info, warn, error, critical

    #Create Palm object
    palm = reflex.reflex_sf() # Reflex object ready
    my_logger.info('Reflex_SF object created')

    for i in range(1,5,1):
        lowest_position = palm.finger[i]["lower_limit"]
        highest_position = palm.finger[i]["upper_limit"]
        init_position = palm.finger[i]["initial_position"]


        my_logger.info('--- Finger {}:'.format(i))
        my_logger.info('       Lower Limit Position --- {}'.format(lowest_position))
        my_logger.info('       Upper Limit Position --- {}'.format(highest_position))
        my_logger.info('       Initial Position {}'.format(init_position))

        calibrate = 0

        if (i == 1 or i == 3):
            a = lowest_position - POS_ERROR
            b= highest_position + POS_ERROR
            if a >= init_position or init_position >= b:
                my_logger.info('Servo {} Initial Position {} not between Lower Limit {} and Upper Limit {}'\
                               .format(i,init_position,lowest_position,highest_position))
                print('Servo {} Initial Position {} not between Lower Limit {} and Upper Limit {}'.format(\
                    i,init_position,lowest_position,highest_position))
                calibrate = 1
        elif (i == 2):
            a = lowest_position + POS_ERROR
            b = highest_position - POS_ERROR
            if a <= init_position or init_position <= b:
                my_logger.info('Servo {} Initial Position {} not between Lower Limit {} and Upper Limit {}'\
                               .format(i,init_position,lowest_position,highest_position))
                print('Servo {} Initial Position {} not between Lower Limit {} and Upper Limit {}'.format(\
                    i,init_position,lowest_position,highest_position))
                calibrate = 1

    pygame.init()

    # Set the width and height of the screen [width,height]
    size = [500, 700]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Reflex_SF JoyStick Movements")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # for print in Pygame screen object
    textPrint = sp.TextPrint()
    my_joy = js.ExtremeProJoystick()
    my_controller = reflex.joy_reflex_controller(my_joy,palm)

    # Joystick Values


    #Loop until the user clicks the close button.
    done = False

    while done==False:
        screen.fill(WHITE)
        textPrint.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.JOYBUTTONDOWN:
                button = my_joy.get_button_pressed(event)
                my_logger.info("Button {} pressed".format(button))
                my_controller.set_button_press(button)
            elif event.type == pygame.JOYBUTTONUP:
                button = my_joy.get_button_released(event)
                my_logger.info("Button {} Released".format(button))
                my_controller.set_button_release(button)
            elif event.type == pygame.JOYHATMOTION:
                my_logger.info("Hat movement - {}".format(my_joy.get_hat_movement(event)))
                pass
            elif event.type == pygame.JOYAXISMOTION:
                pass
            else:
                pass # ignoring other non-logitech joystick event types



        # The code below is to test the measurement of Axes displacement in the Joystick and should be removed
        Num_Axes = my_joy.axes
        #for k in range(0,Num_Axes,1):
            #d = my_joy.get_axis_displacement_and_grip(k)
            #my_logger.info("Axis No.: {} Move: {} Displacement: {} Grip: {}".format(k,d[0],d[1],d[2]))
            #if d[0] == 1:
                #palm.grip_fingers(d[1],d[2])
            #elif d[0] == 2:
                #palm.space_finger1_and_finger2(d[1],d[2])
        # end of test code for the measurement of Axes displacement in the Joystick

        textPrint.Screenprint(screen, "When ready to Quit, close the screen")
        textPrint.Yspace()

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second OR 50 ms scan rate - 1000/20 = 50 ms Both display and checking of Joystick;
        clock.tick(SCAN_RATE)