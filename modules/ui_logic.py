import pygame

def create_transparent_rect(x, y, width, height, color, alpha, screen):
    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    transparent_surface.fill((color[0], color[1], color[2], alpha))
    screen.blit(transparent_surface, (x, y))

class Text:
    def __init__(self, x, y, text, font_size=36, font_color=(0,0,0), bg_color=None, corner_radius=10):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.font_color = font_color
        self.bg_color = bg_color
        self.corner_radius = corner_radius
        self.update()

    def update(self):
        self.rendered_text = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.rendered_text.get_rect(center=(self.x, self.y))
        self.bg_rect = pygame.Rect(self.text_rect.left - 10, self.text_rect.top - 5, self.text_rect.width + 20, self.text_rect.height + 10)
        if self.bg_color:
            self.background = pygame.Surface((self.bg_rect.width, self.bg_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(self.background, self.bg_color, self.background.get_rect(), border_radius=self.corner_radius)
            self.background.blit(self.rendered_text, self.text_rect)

    def draw(self, screen):
        if self.bg_color:
            screen.blit(self.background, self.bg_rect.topleft)
        screen.blit(self.rendered_text, self.text_rect)