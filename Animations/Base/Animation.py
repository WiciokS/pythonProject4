class Animation:
    def __init__(self, frames, delay_tick, loop=True):
        self.frames = frames
        self.delay_tick = delay_tick
        self.loop = loop
        self.current_frame = 0
        self.current_delay_tick = 0
        self.playing = False

    def play(self):
        self.playing = True

    def tick(self):
        if self.playing:
            if self.current_delay_tick >= self.delay_tick:
                self.current_delay_tick = 0
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    if self.loop:
                        self.current_frame = 0
                    else:
                        self.playing = False
            self.current_delay_tick += 1

    def stop(self):
        self.playing = False
        self.current_frame = 0
        self.current_delay_tick = 0

    def get_current_frame(self):
        return self.frames[self.current_frame]
