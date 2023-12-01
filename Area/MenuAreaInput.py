from Area.AreaInput import AreaInput, AreaName


class MenuAreaInput(AreaInput):

    def tick(self):
        pass

    def __init__(self, state_context, top_left_x=0, top_left_y=0, width=0, height=0):
        super().__init__(state_context, AreaName.MENU, top_left_x, top_left_y, width, height)

    def process_mouse_input_event(self, event):
        pass

    def draw(self, screen):
        pass
