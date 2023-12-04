import pygame
from Area.AreaInput import AreaInput, AreaName
from States.State import StateFactory, StateName
from UI.AnimatedButton import AnimatedButton


class MenuAreaInput(AreaInput):
    font = 18  # Font size for the gold cost text

    def tick_anim(self):
        # Update the coin animation
        self.coin_frame_counter += 1
        if self.coin_frame_counter >= self.coin_animation_rate:
            self.coin_frame_counter = 0
            self.current_coin_frame = (self.current_coin_frame + 1) % len(self.coin_sprites)

    def tick(self):
        for event in self.state_context.app_var.events:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.process_mouse_input_event(event)

    def __init__(self, state_context, top_left_x=0, top_left_y=0, width=0, height=0):
        super().__init__(state_context, AreaName.MENU, top_left_x, top_left_y, width, height)
        self.tower_icons = []
        self.tower_backgrounds = []  # List to hold the background sprites
        self.gold_cost_texts = []
        self.icon_collision_rects = []

        y_offset = 64  # Starting y position for the first icon

        # Create an instance of the AnimatedButton
        self.enter_button = AnimatedButton(
            'Sprites/Buttons/EnterButton/Enter Button1.png',
            'Sprites/Buttons/EnterButton/Enter Button2.png',
            "Start Wave",
            26
        )

        # Create enter button collision rect
        self.enter_button_collision_rect = pygame.Rect(self.bottom_right_x - self.enter_button.image.get_width() - 8,
                                                       self.bottom_right_y - self.enter_button.image.get_height() - 8,
                                                       self.enter_button.image.get_width(),
                                                       self.enter_button.image.get_height())
        # Position the button in the bottom corner
        self.enter_button.rect.bottomright = (self.bottom_right_x - 8, self.bottom_right_y - 8)

        # Load the coin sprites for the animation
        self.coin_sprites = [
            pygame.image.load(f'Sprites/Coin/Coin{i}.png') for i in range(1, 6)
        ]
        self.current_coin_frame = 0
        self.coin_animation_rate = 5  # Adjust as needed for animation speed
        self.coin_frame_counter = 0

        # Load the background sprite - replace 'path/to/background_sprite.png' with your actual file path
        self.background_sprite = pygame.image.load('Sprites/Background/Background.png')

        for index, tower_class in enumerate(state_context.game_var.level.available_towers):
            # Dynamically load the icon based on the tower's class attribute
            icon_path = tower_class.icon_path
            icon_sprite = pygame.image.load(icon_path)
            self.tower_icons.append(icon_sprite)

            # Create a rectangle for collision detection
            rect = pygame.Rect(self.top_left_x + 48, self.top_left_y + y_offset, icon_sprite.get_width(),
                               icon_sprite.get_height())
            self.icon_collision_rects.append((rect, index))  # Append a tuple with the rect and index

            # Put text of gold cost below the icon
            gold_cost_text = pygame.font.SysFont("Arial", self.font).render(
                str(tower_class.cost), True, (0, 0, 0))
            self.gold_cost_texts.append(gold_cost_text)

            # Increment y_offset for the next icon
            y_offset += icon_sprite.get_height() + 64

    def switch_to_game_state(self):
        # The action that will be executed when the button is clicked
        if self.state_context.game_var.level.current_wave_index < len(self.state_context.game_var.level.waves):
            self.state_context.current_state_root.switch_substate(
                StateFactory.create_state(StateName.ACTIVE_GAME, self.state_context)
            )

    def process_mouse_input_event(self, event):
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Press the button
            if self.enter_button_collision_rect.collidepoint(mouse_pos):
                if not self.enter_button.is_pressed():
                    self.enter_button.turn_pressed()
        elif event.type == pygame.MOUSEBUTTONUP:
            # Release the button
            if self.enter_button.is_pressed():
                self.enter_button.turn_default()
            if self.enter_button_collision_rect.collidepoint(mouse_pos):
                # Switch to the game state
                self.switch_to_game_state()

            # Check each icon for a collision with the mouse click
        for rect, tower_index in self.icon_collision_rects:  # Corrected iteration
            if rect.collidepoint(mouse_pos):
                # Create the selected tower based on the clicked icon
                if (self.state_context.game_var.level.gold >=
                        self.state_context.game_var.level.available_towers[tower_index].cost):
                    self.state_context.game_var.selected_tower = self.state_context.game_var.level.available_towers[
                        tower_index](self.state_context)
                break  # Exit the loop once a collision is found

    def draw(self, screen):
        # Draw background for the menu area
        screen.fill((128, 128, 128), (self.top_left_x, self.top_left_y, self.bottom_right_x, self.bottom_right_y))

        # Draw the current gold amount
        gold_amount_text = pygame.font.SysFont("Arial", self.font).render(
            str(self.state_context.game_var.level.gold), True, (0, 0, 0)
        )
        screen.blit(gold_amount_text, (self.top_left_x + 32, self.top_left_y + 14))

        # Draw the animated coin sprite near the total gold amount
        coin_sprite = self.coin_sprites[self.current_coin_frame]
        # Position the coin sprite to the left of the gold amount text
        coin_x = self.top_left_x + 8
        coin_y = self.top_left_y + 16
        screen.blit(coin_sprite, (coin_x, coin_y))

        # Draw the enter button
        screen.blit(self.enter_button.image, self.enter_button.rect)

        # Draw tower backgrounds, icons, and gold cost texts
        for icon_sprite, (rect, index) in zip(self.tower_icons, self.icon_collision_rects):
            # Calculate the top left position of the background sprite to be centered and 4 pixels above the icon
            background_x = rect.centerx - self.background_sprite.get_width() // 2
            background_y = rect.top - 4

            # Draw the background sprite
            screen.blit(self.background_sprite, (background_x, background_y))

            # Now draw the icon sprite
            screen.blit(icon_sprite, rect.topleft)

            # Calculate the x position for the gold cost text to be centered below the icon
            text_image = self.gold_cost_texts[index]
            text_x = rect.centerx - text_image.get_width() // 2
            text_y = rect.bottom + 8  # 8 pixels below the icon

            # Draw the gold cost text
            screen.blit(text_image, (text_x, text_y))
