import sys, pygame, math, time, random, csv
from actor import Actor
from bullet import Bullet

debug = False

def main():
    print("Hello from turtle-exvs!")
    pygame.init()

    size = width, height = 640, 480
    black = 0, 0, 0
    flicker = False

    screen = pygame.display.set_mode(size, pygame.SHOWN)
    clock = pygame.time.Clock()
    internal_surface = pygame.Surface((1920,1080))

    ship = [
            [img("turtle1w.png"),img("turtle1s.png"),img("turtle1a.png"),img("turtle1d.png")],
            [img("turtle2w.png"),img("turtle2s.png"),img("turtle2a.png"),img("turtle2d.png")]
    ]

    lock_imgs = [
        [ img("lock_red.png"), img("lock_green.png") ],
        [ img("lock2_red.png"), img("lock2_green.png") ],
        [ img("lock3_red.png"), img("lock3_green.png") ],
        [ img("lock4_red.png"), img("lock4_green.png") ],
    ]

    a_on = img("on.png")
    bullet = img("bullet.png")
    beam = img("beam.png")
    sky = img("sky_seamless_texture_5921.jpg")

    arena_arr = []

    with open("arena.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            arena_arr.append([int(cell) for cell in row])  # Convert strings to integers

    arena_tile_size = 32

    actors = []
    actors.append(Actor(64, 64, 64, 0, None))
    actors.append(Actor(64, 900 - 64, 64, 1, actors[0]))
    actors.append(Actor(1920 - 64, 64, 64, 1, actors[0]))
    actors.append(Actor(1920 - 64, 900 - 64, 64, 0, actors[1]))
    actors[0].target = actors[1]
    actors[1].target = actors[3]
    actors[2].target = actors[3]
    scroll = 0

    while True:
        for a in actors:
            a.update()
            update_bullets(a.bullets, arena_arr)
            update_bullets(a.beams, arena_arr)

        flicker = (not flicker)
        pf = [False,False,False,False]

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            sys.exit()


        m = [keys[pygame.K_w],keys[pygame.K_s],keys[pygame.K_a],keys[pygame.K_d]]
        actors[0].move(arena_arr, m)
        actors[1].move(arena_arr, bot_action(arena_arr,actors[1].target,actors[1], 200,360))
        actors[2].move(arena_arr, bot_action(arena_arr,actors[2].target,actors[2], 200,360))
        actors[3].move(arena_arr, bot_action(arena_arr,actors[3].target,actors[3], 200,360))
        
        actors[0].lock_on(actors, 1)
        actors[1].lock_on(actors, 3)
        actors[2].lock_on(actors, 3)
        actors[3].lock_on(actors, 1)

        if keys[pygame.K_e]:
            actors[0].shoot_a(add_bullet)

        if keys[pygame.K_r]:
            actors[0].shoot_b(add_bullet)

        if keys[pygame.K_t]:
            if actors[0].target == actors[1]:
                actors[0].target = actors[2]
            elif actors[0].target == actors[2]:
                actors[0].target = actors[1]


        screen.fill(black)

        scroll_size = 1000
        scroll_x = scroll % scroll_size
        scroll_y = scroll % scroll_size

        for sx in range(-scroll_size, 1920, scroll_size):
            for sy in range(-scroll_size, 1080, scroll_size):
                internal_surface.blit(sky, (sx + scroll_x, sy + scroll_y))

        scroll += 1

        for i in range(0,32):
            for j in range(0,60):
                if arena_arr[i][j] == 1:
                    internal_surface.blit(a_on, (j * arena_tile_size, i * arena_tile_size))

        actor_index = 0
        for sa in actors:
            internal_surface.blit(bullet, (sa.x, sa.y))

            for p in sa.bullets:
                internal_surface.blit(bullet,(p.x,p.y))

            for p in sa.beams:
                internal_surface.blit(beam,(p.x,p.y))

            blit_centered(internal_surface, ship[sa.team][sa.direction], (sa.x,sa.y), sa.size)

            for st in actors:
                if sa.target == st:
                    blit_centered(internal_surface, lock_imgs[actor_index][sa.lock_type], (st.x,st.y), 80)
            actor_index += 1

        scaled_surface = pygame.transform.scale(internal_surface, size)
        screen.blit(scaled_surface, (0, 0))




        pygame.display.flip()
        clock.tick(30)  # limits FPS to 30

def img(s): #pygame.image.load(s) wrapper to simplify loading images and declutter top part of code.
    return pygame.image.load("img/" + s)

# Example usage
#add_bullet(100, 100, 45, 5, 3)  # Add a point moving at 45 degrees at speed 5, lasting 3 seconds
def add_bullet(bullet_array, spawn_point, angle, speed, lifetime):
    x, y  = spawn_point
    bullet_array.append(Bullet(x, y, angle, speed, lifetime))

def update_bullets(bullet_array, arena_arr):
    for bullet in bullet_array[:]:  # Iterate over a copy to allow safe removal
        bullet.move(arena_arr)
        if bullet.is_expired():
            bullet_array.remove(bullet)

def angle_to_point(point, target_point):
    x,y = point
    target_x, target_y = target_point
    dist_x = target_x - x
    dist_y = target_y - y

    angle = math.atan2(dist_x, dist_y)
    angle_degrees = math.degrees(angle)

    return angle_degrees + 180

def rot_center(image, angle, center):
    x,y = center

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

def blit_centered(s,i,c,z):
    zx,zy = c
    zx -= z * 0.5
    zy -= z * 0.5
    nc = (zx, zy)
    s.blit(i,nc)

def bot_action(a, p, b, min, max):
    dist = math.sqrt((b.x - p.x) ** 2 + (b.y - p.y) ** 2)
    bravery = 100

    if dist > min and dist < max:
        if b.bot_shot_choice == 1: 
            b.shoot_a(add_bullet)
        if b.bot_shot_choice == 2: 
            b.shoot_b(add_bullet)

    if b.weapon_ammo_a <= 0:
        bravery -= 50

    if b.weapon_ammo_b <= 0:
        bravery -= 50

    if time.time() - b.bot_last_update_time > b.bot_timer:
        b.bot_shot_choice =  random.randrange(0,3)
    return bot_movement(a, p, b, min, max, bravery)
    


def bot_movement(a, p, b, min, max, bravery):
    if time.time() - b.bot_last_update_time > b.bot_timer:
        b.bot_last_update_time = time.time()
        bs = 1
        test = []
        mod = [[-bs,-bs],[0,-bs],[bs,-bs],
            [-bs, 0], [0,0],  [bs, 0], 
            [-bs, bs],[0,bs],[bs,bs]]
        mov = [[True,False,True,False], [True, False, False, False],[True,False,False,True],
            [False,False,True,False],[False,False,False,False], [False,False,False,True],
            [False, True,True,False],[False,True,False,False],[False,True,False,True]] #wsad
        
        for i in range(9):
            test.append(math.sqrt(((b.x + mod[i][0]) - p.x) ** 2 + ((b.y + mod[i][1]) - p.y) ** 2))

        wid = 4
        found_move = False


        whem = random.randrange(0,100)
        if whem < 20:
            wid = random.randrange(0,8)
            found_move = True

        for j in range(32):
            if not found_move:
                bs = j
                for i in range(9):
                    fa = test[wid] * b.map_collision_check(a, mov[wid], bs)
                    fb = test[i] * b.map_collision_check(a, mov[i], bs)

                    if test[4] > max:
                        if fb < fa:
                            found_move = True
                            wid = i

                    if test[4] < min:
                        if fb > fa:
                            found_move = True
                            wid = i
                            
                    if not found_move:
                        btest = False
                        cur_brave = random.randrange(0,100)
                        
                        if cur_brave < bravery:
                            if fa > fb:
                                btest = True
                        else:
                            if fa < fb:
                                btest = True

                        if btest:
                            if b.map_collision_check(a, mov[i], bs) < 9: #wall blocking map
                                if test[i] > min and test[i] < max:
                                    found_move = True
                                    wid = i
        if debug:
            print(f"Current dist: {test[4]}")
        b.bot_last_movement = mov[wid]
        return mov[wid]
    else:
        return b.bot_last_movement

if __name__ == "__main__":
    main()
