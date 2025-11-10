
import math
# 맵 바뀌면 날아가는 것들 (몬스터, 배경, 이펙트 등)
world_temporary = [[] for _ in range(4)]

# 유지되어야 하는 객체 (플레이어, UI 등)
world_persistent = [[] for _ in range(3)]

world_npc = [[] for _ in range(2)]

#충돌처리 완료해서 지워질거 저장
remove_queue = []

def add_object(o, depth=0, persistent=False):
    if persistent:
        world_persistent[depth].append(o)
    else:
        world_temporary[depth].append(o)

def add_objects(ol, depth=0, persistent=False):
    if persistent:
        world_persistent[depth] += ol
    else:
        world_temporary[depth] += ol

def add_npc(o, depth=0):
    world_npc[depth].append(o)

def update():
    # 영속 + 임시 둘 다 업데이트
    for layer in world_persistent + world_temporary:
        for o in layer:
            o.update()


def _really_remove_object(o):
    for layer in world_temporary:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
    for layer in world_persistent:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

def render():
    # 순서: 영속 객체는 UI 등에만 사용되므로 나중에 그리면 됨
    for layer in world_temporary:
        for o in layer:
            o.draw()
    for layer in world_persistent:
        for o in layer:
            o.draw()

def render_npc():
    for layer in world_npc:
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

    # 임시 객체 먼저 제거 시도
    for layer in world_temporary:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

    # 영속 객체에서도 제거 가능
    for layer in world_persistent:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
    #npc는 리스트에서만 제거
    for layer in world_npc:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

    raise ValueError('Cannot delete non existing object')


def clear_temporary():
    """맵 바뀔 때 호출 → 임시 객체만 제거"""
    global world_temporary
    for layer in world_temporary:
        layer.clear()
    collision_pairs.clear()


def clear_all():
    """게임 완전 종료 시 호출 → 모든 객체 제거"""
    clear_temporary()
    for layer in world_persistent:
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

def special_directional_collide(a, b):
    # 방향형 스킬이 어느 쪽에 있는지 판별
    skill, target = None, None
    if hasattr(a, 'degree') and hasattr(a, 'player'):
        skill, target = a, b
    elif hasattr(b, 'degree') and hasattr(b, 'player'):
        skill, target = b, a
    else:
        return False

    px, py = skill.player.x, skill.player.y
    tx, ty = target.x, target.y

    dx = tx - px
    dy = ty - py

    dist = math.sqrt(dx * dx + dy * dy)
    max_range = getattr(skill, 'distance', 200)

    # 거리가 너무 멀면 충돌 X
    if dist > max_range + 50:
        return False

    # 각도 차이 계산
    angle_to_target = math.degrees(math.atan2(dy, dx))
    diff = abs((angle_to_target - skill.degree + 180) % 360 - 180)

    # 각도 허용 범위 (스킬에 따라 다르게 설정 가능)
    angle_tolerance = getattr(skill, 'angle_tolerance', 25)

    return diff < angle_tolerance

def special_area_collide(a, b):
    """
    원형(범위형) 스킬 충돌 판정.
    스킬의 중심(a.x, a.y)과 대상(b)의 중심 거리 계산 후,
    스킬 범위(a.distance) 내에 있으면 True 반환.
    """
    # 스킬과 대상 구분 (a,b 순서 상관없이 처리)
    skill, target = None, None
    if hasattr(a, 'distance') and hasattr(a, 'player'):
        skill, target = a, b
    elif hasattr(b, 'distance') and hasattr(b, 'player'):
        skill, target = b, a
    else:
        return False

    # 스킬 중심
    sx, sy = skill.x, skill.y
    # 대상 중심
    if hasattr(target, 'x') and hasattr(target, 'y'):
        tx, ty = target.x, target.y
    else:
        return False

    # 두 점 거리 계산
    dx = tx - sx
    dy = ty - sy
    dist = math.sqrt(dx * dx + dy * dy)

    # 충돌 거리 기준 (스킬 범위 + 적 크기 보정)
    radius = getattr(skill, 'distance', 100)/4
    hitbox = 50  # 적 반지름 대략치 (필요시 enemy.get_bb로 동적계산 가능)

    return dist <= radius + hitbox

def handle_collisions():

    # 충돌dict의 모든 그룹에 대해서 충돌검사를 수행
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:  # 첫번째 리스트의 모든 객체에 대해서
            for b in pairs[1]:  # 두번째 리스트의 모든 객체에 대해서
                #  예외 처리: 물대포 같은거 전용 판정

                if group =='cannon:enemy':
                    if special_directional_collide(a, b):
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)
                    #continue  # AABB 검사 스킵
                elif group =='EQ:enemy':
                    if special_area_collide(a, b):
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)

                    #continue  # AABB 검사 스킵

                # 기본 충돌
                elif collide(a, b):
                    a.handle_collision(group, b)  # 충돌했으면 처리는 각각의 객체가 알잘딱 처리해야함
                    b.handle_collision(group, a)  # 충돌했으면 처리는 각각의 객체가 알잘딱 처리해야함
                    # 하지만 collision_pairs에서 해당 객체가 제거가 안되었으므로 remove_collision_object함수
                    # 만들었음 remove_object에서 호출해서 제거함