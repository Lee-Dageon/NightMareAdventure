import game_world


class MonsterRemovalTimer:
    def __init__(self, monster, delay):
        self.monster = monster
        self.delay = delay
        self.elapsed_time = 0.0  # 경과 시간

    def update(self, elapsed_time):
        self.elapsed_time += elapsed_time
        if self.elapsed_time >= self.delay:
            if self.monster in game_world.world[1]:
                print(f"Removing monster at ({self.monster.x}, {self.monster.y}) after delay.")
                game_world.remove_object(self.monster)
            return True  # 타이머 제거 신호 반환
        return False
