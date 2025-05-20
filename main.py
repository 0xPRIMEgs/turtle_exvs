import sys, pygame, math, time, random
pygame.init()

size = width, height = 640, 480
black = 0, 0, 0

screen = pygame.display.set_mode(size, pygame.SHOWN)
clock = pygame.time.Clock()



internal_surface = pygame.Surface((1920,1080))



ship = [
        [pygame.image.load("turtle1w.png"),pygame.image.load("turtle1s.png"),pygame.image.load("turtle1a.png"),pygame.image.load("turtle1d.png")],
        [pygame.image.load("turtle2w.png"),pygame.image.load("turtle2s.png"),pygame.image.load("turtle2a.png"),pygame.image.load("turtle2d.png")]
]
ball = pygame.image.load("ship_bottom.png")
flames = [pygame.image.load("flame_w.png"),pygame.image.load("flame_s.png"),pygame.image.load("flame_a.png"),pygame.image.load("flame_d.png")]
arena = pygame.image.load("meta-arena.png")

a_on = pygame.image.load("on.png")
a_off = pygame.image.load("off.png")

lock_imgs = [
    [ pygame.image.load("lock_red.png"), pygame.image.load("lock_green.png") ],
    [ pygame.image.load("lock2_red.png"), pygame.image.load("lock2_green.png") ],
    [ pygame.image.load("lock3_red.png"), pygame.image.load("lock3_green.png") ],
    [ pygame.image.load("lock4_red.png"), pygame.image.load("lock4_green.png") ],
]

bullet = pygame.image.load("bullet.png")
beam = pygame.image.load("beam.png")

sky = pygame.image.load("sky_seamless_texture_5921.jpg")

flicker = False
new_size = (64, 64)
#ship = pygame.transform.smoothscale(ship, new_size)

arena_arr = [
    [0] * 60 for _ in range(32)
]


arena_arr[0][0:60] = [1] * 60
arena_arr[31][0:60] = [1] * 60

for row in arena_arr:
    row[0] = 1  # Left wall
    row[59] = 1  # Right wall

# Original pattern placement adjusted for new size
# Top-right corner (original placement)
arena_arr[5][5:9] = [1, 1, 1, 1]
arena_arr[5][19:21] = [1, 1]
arena_arr[6][5] = 1
arena_arr[6][19:21] = [1, 1]
arena_arr[7][5] = 1
arena_arr[9][12:14] = [1, 1]
arena_arr[10][12:14] = [1, 1]
arena_arr[12][20] = 1
arena_arr[13][5:7] = [1, 1]
arena_arr[13][20] = 1
arena_arr[14][5:7] = [1, 1]
arena_arr[14][17:21] = [1, 1, 1, 1]

# **Bottom-right corner**
shift_down = 15
arena_arr[5 + shift_down][5:9] = [1, 1, 1, 1]
arena_arr[5 + shift_down][19:21] = [1, 1]
arena_arr[6 + shift_down][5] = 1
arena_arr[6 + shift_down][19:21] = [1, 1]
arena_arr[7 + shift_down][5] = 1
arena_arr[9 + shift_down][12:14] = [1, 1]
arena_arr[10 + shift_down][12:14] = [1, 1]
arena_arr[12 + shift_down][20] = 1
arena_arr[13 + shift_down][5:7] = [1, 1]
arena_arr[13 + shift_down][20] = 1
arena_arr[14 + shift_down][5:7] = [1, 1]
arena_arr[14 + shift_down][17:21] = [1, 1, 1, 1]

# **Top-left corner**
shift_right = 33
arena_arr[5][5 + shift_right:9 + shift_right] = [1, 1, 1, 1]
arena_arr[5][19 + shift_right:21 + shift_right] = [1, 1]
arena_arr[6][5 + shift_right] = 1
arena_arr[6][19 + shift_right:21 + shift_right] = [1, 1]
arena_arr[7][5 + shift_right] = 1
arena_arr[9][12 + shift_right:14 + shift_right] = [1, 1]
arena_arr[10][12 + shift_right:14 + shift_right] = [1, 1]
arena_arr[12][20 + shift_right] = 1
arena_arr[13][5 + shift_right:7 + shift_right] = [1, 1]
arena_arr[13][20 + shift_right] = 1
arena_arr[14][5 + shift_right:7 + shift_right] = [1, 1]
arena_arr[14][17 + shift_right:21 + shift_right] = [1, 1, 1, 1]

# **Bottom-left corner**
arena_arr[5 + shift_down][5 + shift_right:9 + shift_right] = [1, 1, 1, 1]
arena_arr[5 + shift_down][19 + shift_right:21 + shift_right] = [1, 1]
arena_arr[6 + shift_down][5 + shift_right] = 1
arena_arr[6 + shift_down][19 + shift_right:21 + shift_right] = [1, 1]
arena_arr[7 + shift_down][5 + shift_right] = 1
arena_arr[9 + shift_down][12 + shift_right:14 + shift_right] = [1, 1]
arena_arr[10 + shift_down][12 + shift_right:14 + shift_right] = [1, 1]
arena_arr[12 + shift_down][20 + shift_right] = 1
arena_arr[13 + shift_down][5 + shift_right:7 + shift_right] = [1, 1]
arena_arr[13 + shift_down][20 + shift_right] = 1
arena_arr[14 + shift_down][5 + shift_right:7 + shift_right] = [1, 1]
arena_arr[14 + shift_down][17 + shift_right:21 + shift_right] = [1, 1, 1, 1]

arena_tile_size = 32

class Bullet:
    def __init__(self, x, y, angle, speed, lifetime):
        self.x = x
        self.y = y
        self.angle = math.radians(angle - 90)  # Convert to radians for movement
        self.speed = speed
        self.creation_time = time.time()
        self.lifetime = lifetime

    def move(self, arena_arr):
        self.x -= math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        one_over_tile_size = 1/32
        bullet_size = 4
        
        bullet_tile_x, bullet_tile_y = math.floor((self.x) * one_over_tile_size),math.floor((self.y) * one_over_tile_size)
        if arena_arr[bullet_tile_y][bullet_tile_x] != 0:
            self.lifetime = 0

        bullet_tile_x, bullet_tile_y = math.floor((self.x + bullet_size) * one_over_tile_size),math.floor((self.y + bullet_size) * one_over_tile_size)
        if arena_arr[bullet_tile_y][bullet_tile_x] != 0:
            self.lifetime = 0


    def is_expired(self):
        return time.time() - self.creation_time > self.lifetime

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


class Actor:
    def __init__(self, x, y, size, team, target):
        self.x = x
        self.y = y
        self.angle = 0
        self.direction = 0
        self.size = size
        self.bullets = []
        self.beams = []
        self.flames = []
        self.team = team
        self.speed = 8

        self.target = target
        self.lock_type = 0

        self.weapon_ammo_a = 25
        self.weapon_ammo_max_a = 25
        self.reload_timer_a = 1
        self.last_reload_a = 0 

        self.weapon_ammo_b = 5
        self.weapon_ammo_max_b = 5
        self.cool_down_b = 0.5
        self.last_shot_b = 0
        self.reload_timer_b = 1
        self.last_reload_b = 0 

        self.bot_timer = 0.5
        self.bot_last_movement = [False,False,False,False]
        self.bot_last_update_time = 0
        self.bot_shot_choice = 0

    def pos(self):
        return (self.x, self.y)

    def tpos(self, a):
        mtn = 1/32
        ptx, pty = math.floor((self.x) * mtn),math.floor((self.y) * mtn)

        if pty < len(a):
            if ptx < len(a[pty]):
                return (ptx, pty)

        return (-1,-1)
    
    def shoot_a(self):
         if self.weapon_ammo_a > 0:
            spread = 1
            na = self.angle + (random.randrange(-10, 10) * spread)
            add_bullet(self.bullets, self.pos(), na, 5, 3)  # Add a point moving at 45 degrees at speed 5, lasting 3 seconds
            self.weapon_ammo_a -= 1
            if self.weapon_ammo_a == 0:
                self.last_reload_a = time.time()

    def shoot_b(self):
         if time.time() - self.last_shot_b > self.cool_down_b:
            if self.weapon_ammo_b > 0:
                for i in range(10):
                    add_bullet(self.beams, self.pos(), self.angle, 5 - (i * 0.1), 3)  # Add a point moving at 45 degrees at speed 5, lasting 3 seconds
                self.weapon_ammo_b -= 1
                self.last_shot_b = time.time()
                if self.weapon_ammo_b == 0:
                    self.last_reload_b = time.time()

    def m_check(self, arena_arr, m, s):
        result = 1
        ppx, ppy = self.x, self.y

        if m[2]:
            self.x -= s
        elif m[3]:
            self.x += s

        if m[0]:
            self.y -= s
        elif m[1]:
            self.y += s

        mtn = 1/32
        ptx, pty = self.tpos(arena_arr)

        if ptx >= 0 and pty >= 0:
            if arena_arr[pty][ptx] != 0:
                result = 9

        print(f"Checking movement: {m}, arena value: {arena_arr[pty][ptx] if ptx >= 0 and pty >= 0 else 'out of bounds'}")

        self.x = ppx
        self.y = ppy

        return result


    def move(self, arena_arr, m):
        ppx, ppy = self.x, self.y
        if m[2]:
            self.direction = 2
            self.x -= self.speed
        elif m[3]:
            self.direction = 3
            self.x += self.speed

        mtn = 1/32
        ptx, pty = self.tpos(arena_arr)

        if ptx >= 0 and pty >= 0:
            if arena_arr[pty][ptx] != 0:
                self.x = ppx

        if m[0]:
            self.direction = 0
            self.y -= self.speed
        elif m[1]:
            self.direction = 1
            self.y += self.speed

        ptx, pty = self.tpos(arena_arr)

        if ptx >= 0 and pty >= 0:
            if arena_arr[pty][ptx] != 0:
                self.y = ppy

    def update(self):
        if self.weapon_ammo_a == 0:
            if time.time() - self.last_reload_a > self.reload_timer_a:
                self.weapon_ammo_a = self.weapon_ammo_max_a

        if self.weapon_ammo_b == 0:
            if time.time() - self.last_reload_b > self.reload_timer_b:
                self.weapon_ammo_b = self.weapon_ammo_max_b

        dist = math.sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
        if dist < 360:
            self.lock_type = 1
        else:
            self.lock_type = 0

    def center(self):
        return (self.x + (self.size * 0.5), self.y + (self.size * 0.5))

    def lock_on(self, a, id):
        self.angle = angle_to_point(self.center(),a[id].center())

    def is_expired(self):
        return time.time() - self.creation_time > self.lifetime

actors = []
actors.append(Actor(64, 64, 64, 0, None))
actors.append(Actor(64, 900 - 64, 64, 1, actors[0]))
actors.append(Actor(1920 - 64, 64, 64, 1, actors[0]))
actors.append(Actor(1920 - 64, 900 - 64, 64, 0, actors[1]))
actors[0].target = actors[1]
actors[1].target = actors[3]
actors[2].target = actors[3]
scroll = 0


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
            b.shoot_a()
        if b.bot_shot_choice == 2: 
            b.shoot_b()

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
                    fa = test[wid] * b.m_check(a, mov[wid], bs)
                    fb = test[i] * b.m_check(a, mov[i], bs)

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
                            if b.m_check(a, mov[i], bs) < 9: #wall blocking map
                                if test[i] > min and test[i] < max:
                                    found_move = True
                                    wid = i
        print(f"Current dist: {test[4]}")
        b.bot_last_movement = mov[wid]
        return mov[wid]
    else:
        return b.bot_last_movement

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
       actors[0].shoot_a()

    if keys[pygame.K_r]:
       actors[0].shoot_b()

    if keys[pygame.K_t]:
        if actors[0].target == actors[1]:
           actors[0].target = actors[2]
        elif actors[0].target == actors[2]:
           actors[0].target = actors[1]


    screen.fill(black)
    screen.blit(arena, (0,0))


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
