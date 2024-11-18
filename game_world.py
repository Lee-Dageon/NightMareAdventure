world = [[] for _ in range(4)]
collision_pairs = {}

#group : 'boy:ball', 'boy:zombie'
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()



def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o   #메모리에서도 삭제(free와 유사)
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()



# fill here
def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                # a 또는 b가 삭제된 상태라면 충돌 건너뛰기
                if hasattr(a, 'is_deleted') and a.is_deleted:
                    continue
                if hasattr(b, 'is_deleted') and b.is_deleted:
                    continue

                # 충돌이 발생한 경우 처리
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
