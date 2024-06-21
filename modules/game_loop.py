from modules.config import *
from modules.ui_logic import *
from modules.haptic_port import serial_ports

def game(xc, yc, current_trial, port, pos_image, x_gradient, y_gradient, 
         assistance_level, x_image, y_image, screen, clock, dpm, device, haplyBoard):
    '''Displays the actual game of removing tartar'''
    pm       = np.zeros(2)       # Position of mouse at time t
    pm_prev  = np.zeros(2)       # Position of mouse at time t-1
    xh       = np.zeros(2)       # Position of haptic device at time t
    tartar_pos_prev = np.zeros(2) # Last position of haptic handle on tartar

    tartar_score = 0             # Stores how much tartar is removed
    tartar_fraction = 0          # Stores fraction of total tartar removed
    gum_score    = 0             # Stores how often the gum is touched

    tartar_score_text   = Text(110, 565, "Tartar removed: 0%", 30)
    gum_score_text      = Text(300, 565, "Gum hits: 0", 30)
    time_text           = Text(500, 565, "0", 30)
    trial_text          = Text(xc, 25, "Trial " + str(current_trial))

    game_start = time.time()
    game_end = game_start + 30

    running = True
    while game_end > time.time() and running:
        F = np.zeros(2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == ord('q'):
                    running = False 

        if port and haplyBoard.data_available():
            device.device_read_data()
            motorAngle = device.get_device_angles()
            
            device_position = device.get_device_position(motorAngle)
            xh = np.array(device_position)*1e3*3
            xh[0] = np.round(-xh[0]+xc)
            xh[1] = np.round(xh[1]+100)
            pm = xh
        else:
            pm = pygame.mouse.get_pos()

        dxm = (pm - pm_prev) / dpm          # Displacement of mouse between t-1 and t
        vm  = dxm / dt                      # Velocity of mouse between t-1 and t

        # Damping force on arm
        F += -1 * vm

        # Virtual shape
        grad_x, grad_y = x_gradient[int(pm[1]),int(pm[0])], y_gradient[int(pm[1]),int(pm[0])]
        F += assistance_level*np.array([grad_x, grad_y])

        if port:
            F[1] = F[1]     # Flips the force on the Y=axis 
            F[0] = -F[0]    # Flips the force on the X=axis 
            
            # Update the forces of the device
            device.set_device_torques(F)
            device.device_write_torques()

            time.sleep(0.001)
        
        # Simulation of tartar removal
        adj_pm = (pm[0] - int(x_image), pm[1] - int(y_image))
        for x in range(int(adj_pm[0] - tool_radius), int(adj_pm[0] + tool_radius)):
            for y in range(int(adj_pm[1] - tool_radius), int(adj_pm[1] + tool_radius)):
                if 0 <= x < tartar_image.get_width() and 0 <= y < tartar_image.get_height():
                    if (x - adj_pm[0])**2 + (y - adj_pm[1])**2 <= tool_radius**2:
                        tartar_image.set_at((x, y), (0, 0, 0, 0))
                        cor_color = get_pixels(np.array([x+x_image,y+y_image]), tartar, pos_image)
                        if cor_color == tartar_color:
                            tartar_score += 1   
                            tartar_fraction = int(tartar_score / nr_tartar_pixels * 100)
                            tartar_score_text.text = "Tartar removed: " + str(tartar_fraction) + "%"
                            tartar_score_text.update()
                            tartar[y,x, :] = [0,0,0]

                        elif get_pixels(np.array([x+x_image,y+y_image]), sprite, pos_image) == inside and cor_color != [0,0,0] and np.linalg.norm(pm - tartar_pos_prev) >= 10:
                            gum_score -= 1
                            gum_score_text.text = "Gum hits: " + str(gum_score)
                            gum_score_text.update()

                            tartar_pos_prev = np.array(pm)


        # Draw on screen
        screen.fill(color=background_color)
        screen.blit(jaw_image, (x_image, y_image))
        screen.blit(tartar_image, (x_image, y_image))
        # screen.blit(tartar_image_2, (x_image, y_image))

        create_transparent_rect(0, screen_height-70, screen_width, screen_height, (54, 79, 107), 200, screen)

        tartar_score_text.draw(screen)
        gum_score_text.draw(screen)

        time_text.text = "Time remaining: " + str(int(game_end - time.time()))
        time_text.update()
        time_text.draw(screen)
        trial_text.draw(screen)
                        
        # Draw mouse
        pygame.draw.circle(screen, (0, 0, 255), pm, 5)

        pygame.display.flip()

        # Limit FPS
        clock.tick(FPS)  

        # Update variables
        pm_prev     = np.array(pm).copy()

    return tartar_score, gum_score, tartar_fraction