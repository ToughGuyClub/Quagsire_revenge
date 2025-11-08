world = [[] for _ in range(4)]


def add_object(o, depth=0):
    world[depth].append(o)


def add_objects(ol, depth=0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


# collision_pairs에 있는 모든 O(객체)를 제거하는 함수임
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
            # collision_pairs(dict자료형으로 된그거)에서도 제거해야함
            remove_collision_object(o)
            return

    raise ValueError('Cannot delete non existing object')


def clear():
    global world

    for layer in world:
        layer.clear()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


collision_pairs = {}


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        # 처음 추가되는 그룹이라면 그룹을 생성함
        collision_pairs[group] = [[], []]
    if a: collision_pairs[group][0].append(a)
    if b: collision_pairs[group][1].append(b)


def handle_collisions():
    # 충돌dict의 모든 그룹에 대해서 충돌검사를 수행
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:  # 첫번째 리스트의 모든 객체에 대해서
            for b in pairs[1]:  # 두번째 리스트의 모든 객체에 대해서
                if collide(a, b):
                    a.handle_collision(group, b)  # 충돌했으면 처리는 각각의 객체가 알잘딱 처리해야함
                    b.handle_collision(group, a)  # 충돌했으면 처리는 각각의 객체가 알잘딱 처리해야함
                    # 하지만 collision_pairs에서 해당 객체가 제거가 안되었으므로 remove_collision_object함수
                    # 만들었음 remove_object에서 호출해서 제거함