import pygame

from UI.Button import Button


class AnimatedButton(Button):
    def __init__(self, default_sprite_path, pressed_sprite_path, text, text_size, button_size_x=0, button_size_y=0,
                 text_color=(255, 255, 255)):
        # Load the images
        default_sprite = pygame.image.load(default_sprite_path).convert_alpha()
        pressed_sprite = pygame.image.load(pressed_sprite_path).convert_alpha()

        # Set the button size to the default sprite size if no size is provided
        if button_size_x == 0:
            button_size_x = default_sprite.get_width()
        if button_size_y == 0:
            button_size_y = default_sprite.get_height()

        # Change the size of the sprites
        default_sprite = pygame.transform.scale(default_sprite, (button_size_x, button_size_y))
        pressed_sprite = pygame.transform.scale(pressed_sprite, (button_size_x, button_size_y))

        # Render the text
        font = pygame.font.Font(None, text_size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=default_sprite.get_rect().center)

        # Blit the text onto the sprites
        default_sprite.blit(text_surface, text_rect)
        pressed_sprite.blit(text_surface, text_rect)

        # Initialize the Button class with the loaded images
        super().__init__(default_sprite, pressed_sprite)

    def toggle_pressed(self):
        # Call this method to toggle the button's state
        if self.image is self.pressed_sprite:
            self.image = self.default_sprite
        else:
            self.image = self.pressed_sprite

    def turn_pressed(self):
        # Call this method to set the button's state to pressed
        self.image = self.pressed_sprite

    def turn_default(self):
        # Call this method to set the button's state to default
        self.image = self.default_sprite

    def is_pressed(self):
        return self.image is self.pressed_sprite

    def action(self):
        # Implement the abstract method. This can be a placeholder if no action is needed.
        pass
