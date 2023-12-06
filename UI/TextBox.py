import pygame
import re

class TextBox:
    def __init__(self, x, y, width, height, text_size=32, regex_pattern=".*", max_length=12):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White color
        self.text_color = (0, 0, 0)  # Black text
        self.text_size = text_size
        self.font = pygame.font.Font(None, self.text_size)
        self.text = ""
        self.active = False
        self.regex_pattern = regex_pattern
        self.max_length = max_length

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.save_input("UI/output.txt")
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < self.max_length:
                    self.text += event.unicode
                    if not re.match(self.regex_pattern, self.text):
                        self.text = self.text[:-1]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.text_color, self.rect, 2)  # Border

    def save_input(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.text)
