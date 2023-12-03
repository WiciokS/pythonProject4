from abc import abstractmethod
from enum import Enum


class AreaName(Enum):
    MAP = 0
    MENU = 1


class MoveDirection(Enum):
    FROM_TOP = 0
    FROM_BOTTOM = 1
    FROM_LEFT = 2
    FROM_RIGHT = 3


class AreaInput:
    def __init__(self, state_context, area_name, top_left_x=0, top_left_y=0, width=0, height=0):
        self.AreaName = area_name
        self.state_context = state_context
        if top_left_x > width:
            raise Exception("top_left_x must be less than width")
        if top_left_y > height:
            raise Exception("top_left_y must be less than height")
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = width
        self.bottom_right_y = height
        pass

    def move_by(self, move_direction, amount):
        if move_direction == MoveDirection.FROM_TOP:
            self.top_left_y += amount
        elif move_direction == MoveDirection.FROM_BOTTOM:
            self.bottom_right_y -= amount
        elif move_direction == MoveDirection.FROM_LEFT:
            self.top_left_x += amount
        elif move_direction == MoveDirection.FROM_RIGHT:
            self.bottom_right_x -= amount

    def inside(self, mouse_coordinate):
        if self.top_left_x <= mouse_coordinate[0] <= self.bottom_right_x:
            if self.top_left_y <= mouse_coordinate[1] <= self.bottom_right_y:
                return True
        return False

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def process_mouse_input_event(self, event):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def tick_anim(self):
        pass
