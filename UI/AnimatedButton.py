import pygame

from UI.Button import Button


class AnimatedButton(Button):
    def __init__(self, default_sprite_path, pressed_sprite_path):
        # Load the images
        default_sprite = pygame.image.load(default_sprite_path)
        pressed_sprite = pygame.image.load(pressed_sprite_path)
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

    def action(self):
        # Implement the abstract method. This can be a placeholder if no action is needed.
        pass
