from pico2d import load_image


class BombEffect:
    def __init__(self, x, y, camera, effect_type="red"):
        if effect_type == "green":
            self.image = load_image('./Art/Items/bomb_effect_green.png')  # Green effect
        else:
            self.image = load_image('./Art/Items/bomb_effect.png')  # Default Red effect
        self.x, self.y = x, y
        self.camera = camera
        self.frame = 0
        self.finished = False
        self.frame_time = 0.0

    def update(self):
        self.frame_time += 0.016
        if self.frame_time >= 0.1:
            self.frame += 1
            self.frame_time = 0.0
            if self.frame >= 7:
                self.finished = True

    def draw(self):
        if not self.finished:
            sprite_width = self.image.w // 7
            sprite_height = self.image.h
            draw_width = sprite_width * 1
            draw_height = sprite_height * 1
            self.image.clip_draw(
                self.frame * sprite_width - 20, 0, sprite_width, sprite_height,
                self.x - self.camera.x, self.y - self.camera.y,
                draw_width, draw_height
            )
