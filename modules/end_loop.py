from modules.config import *
from modules.ui_logic import *

def display_end(xc, yc, screen, tartar_fraction, gum_score, total_score):
    '''Displays the end screen displaying the score of the user for the current trial'''
    total_score = tartar_fraction + gum_score

    end_text = Text(xc, yc-50, "Your score: ", 50)
    score_text = Text(xc, yc, str(total_score), 50)
    tartar_score = Text(xc, yc+50, "Tartar removed: " + str(tartar_fraction), 30)
    gum_damage = Text(xc, yc+100, "Gum damage: " + str(gum_score), 30)

    run = True
    while run:
        for event in pygame.event.get(): 
            if event.type == pygame.KEYUP:
                if event.key == ord('q'): 
                    run = False


        screen.fill(color=(54, 79, 107))
        create_transparent_rect(0, 0, screen_width, screen_height, (54, 79, 107), 200, screen)
        end_text.draw(screen)
        score_text.draw(screen)
        tartar_score.draw(screen)
        gum_damage.draw(screen)

        pygame.display.flip()

    