from modules.config import *
from modules.ui_logic import *
from modules.haptic_port import serial_ports

def display_initial_screen(xc, yc, screen, port, x_image, y_image, haplyBoard, device):
    '''Display initial screen asking the user to move the haptic handle towards the starting position'''

    start_text = Text(xc, yc, "Please press e to start the game!", bg_color=(252, 81, 133))
    next_text = Text(xc, 550, "Please move the haptic handle onto the blue circle", bg_color=(252, 81, 133))

    # wait until the start button is pressed
    run = True
    while run:
        F = np.zeros(2)
        for event in pygame.event.get(): 
            if event.type == pygame.KEYUP:
                if event.key == ord('e'): 
                    run = False


        screen.fill(color=(54, 79, 107))
        start_text.draw(screen)
        pygame.display.flip()

    start_circle_center = [207, 385]
    run = True
    time_on_start = 0.0
    while run:
        for event in pygame.event.get(): 
            if event.type == pygame.KEYUP:
                if event.key == ord('e'): 
                    run = False

        if port and haplyBoard.data_available():
            device.device_read_data()
            motorAngle = device.get_device_angles()
            
            device_position = device.get_device_position(motorAngle)
            xh = np.array(device_position)*1e3*3
            xh[0] = np.round(-xh[0]+xc)
            xh[1] = np.round(xh[1]+100)
            pm = np.array(xh)
        else:
            pm = np.array(pygame.mouse.get_pos())

        if np.linalg.norm(pm - start_circle_center) < 20:
            start_area_color = (54, 79, 107)
            time_on_start += dt
        else: 
            start_area_color = (63, 193, 201)

        if port:
            F[1] = 0     # Flips the force on the Y=axis 
            F[0] = 0    # Flips the force on the X=axis 
            
            # Update the forces of the device
            device.set_device_torques(F)
            device.device_write_torques()

            time.sleep(0.001)

        screen.fill(color=background_color)
        screen.blit(jaw_image, (x_image, y_image))
        screen.blit(tartar_image, (x_image, y_image))

        create_transparent_rect(0, 0, screen_width, screen_height, (54, 79, 107), 200, screen)

        pygame.draw.circle(screen, start_area_color, start_circle_center, 20)

        pygame.draw.circle(screen, (0, 0, 255), pm, 5)

        if time_on_start > 1:
            next_text.text = "Game starting in " + str(int(end_start_time-time.time()))
            next_text.y = yc
            next_text.update()
            next_text.draw(screen)
            pygame.display.flip()  
            if end_start_time - time.time() < 0: 
                run = False
        else:
            end_start_time = 5 + time.time()
            next_text.draw(screen)
            pygame.display.flip()