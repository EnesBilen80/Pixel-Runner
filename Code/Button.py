import pygame


class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color, rect_size, rect_color):
        self.rect_color = rect_color
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = pygame.Rect((self.x_pos - rect_size[0] // 2, self.y_pos - rect_size[1] // 2), rect_size)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update(self, screen):
        pygame.draw.rect(screen, self.rect_color, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
