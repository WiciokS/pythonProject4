import pygame

from UI.Button import Button


class AnimatedButton(Button):
    def __init__(self, default_sprite_path, pressed_sprite_path, text, text_size, button_size_x = 0, button_size_y = 0, text_color=(255, 255, 255)):
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

        # Attribute to control the animation
        self.is_pressed = False
        self.animation_time = 100  # Time in milliseconds to display the pressed image
        self.last_press_time = None  # Time of the last button press

    def press(self):
        # Call this method to simulate a button press
        self.image = self.pressed_sprite
        self.is_pressed = True
        self.last_press_time = pygame.time.get_ticks()

    def update(self):
        # Call this method in the game loop to manage the animation state
        current_time = pygame.time.get_ticks()
        if self.is_pressed and (current_time - self.last_press_time >= self.animation_time):
            # After the animation time has passed, revert to the default image
            self.image = self.default_sprite
            self.is_pressed = False

    def is_pressed(self):
        return self.is_pressed

    def action(self):
        # Implement the abstract method. This can be a placeholder if no action is needed.
        pass
