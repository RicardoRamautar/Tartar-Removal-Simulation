from modules.config import *
from modules.ui_logic import Text

def display_settings(xc, yc, screen):
    '''Display the first screen asking for the name of the participant and the assistance level'''

    settings            = Text(xc, 50, "Settings")
    participant         = Text(150, yc-90+20, "Participant name:")
    haptic_assistance   = Text(200, yc+20, "Assistance (0.2 - 0.17.5 - 0.15 - 0): ")
    continue_text       = Text(screen_width - 140, screen_height-75, "Continue")

    font = pygame.freetype.SysFont(None, 24)

    input_rect1 = pygame.Rect(450, yc-90, 200, 50)
    input_active1 = False
    text1 = ""

    input_rect2 = pygame.Rect(450, yc, 200, 50)
    input_active2 = False
    text2 = ""

    input_rect3     = pygame.Rect(screen_width-200, screen_height-100, 120, 50)

    # Main loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect1.collidepoint(event.pos):
                    input_active1 = True
                    text1 = ""
                else:
                    input_active1 = False
                
                if input_rect2.collidepoint(event.pos):
                    input_active2 = True
                    text2 = ""
                else:
                    input_active2 = False

                if input_rect3.collidepoint(event.pos):
                    run = False

            elif event.type == pygame.KEYDOWN:
                if input_active1:
                    if event.key == pygame.K_RETURN:
                        input_active1 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                elif input_active2:
                    if event.key == pygame.K_RETURN:
                        input_active2 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        screen.fill((54, 79, 107))

        text_surf1, text_rect1 = font.render(text1, (255, 0, 0))
        text_rect1.center = input_rect1.center

        text_surf2, text_rect2 = font.render(text2, (255, 0, 0))
        text_rect2.center = input_rect2.center

        pygame.draw.rect(screen, (0, 0, 0), input_rect1, 2)
        pygame.draw.rect(screen, (0, 0, 0), input_rect2, 2)
        pygame.draw.rect(screen, (0, 0, 0), input_rect3, 2)

        settings.draw(screen)
        participant.draw(screen)
        haptic_assistance.draw(screen)
        continue_text.draw(screen)

        screen.blit(text_surf1, text_rect1)
        screen.blit(text_surf2, text_rect2)

        pygame.display.flip()

    return text1, float(text2)