from modules import MineGenerator, pygame

TILE_SIZE = 50
RADIUS = 9
GEN_RADIUS = 20

class MineDisplay():
    def __init__(self):
        self.mine_gen = MineGenerator()
        self.surface = pygame.Surface((850, 850))
        self.is_mining = False
        self.is_moving = False
        self.tile_target = None
        self.screen_shift = (0, 0)
        self.break_time = None
        self.current_break_time = None
        self.move_vec = None
        self.move_time = None
        self.current_move_time = None
        
        self.ore_dict = self.mine_gen.ore_dict
        
        self.ore_colours = {
            "diamond": (49, 208, 232),
            "iron": (240, 240, 240),
            "copper": (143, 75, 10),
            "coal": (20, 20, 19),
            "emerald": (52, 158, 80),
            "gold": (194, 159, 43),
            "stone": (100, 100, 100)
        }
        
        # TODO create modular player art class (change colour of various bits)
        self.player_img = pygame.image.load("Assets/mining.png").convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (100, 100))
        self._image_rect = self.player_img.get_rect()
        self._image_rect.center = (425, 425)
        
        # TODO create player class
        self.player_loc = (0, 1)
        self.player_movespeed = 150
        self.player_mining_speed = 5
        self.player_fuel = 100
        self.player_drain_drill = 10
        self.player_drain_move = 5
        # upgradable value later? making deep mining faster
        self.player_mining_attenuation = 0.5
        self.player_mining_tier = 10
        self.player_depth = 1
        
        self.gen_new_mine((10, 23))
        
  
    def gen_new_mine(self, start=(0, 1)):
        self.player_loc = start
        self.player_depth = self.player_loc[1]
        self.mine_gen.gen_new(start)
        
    def gen_col(self, direction):
        for i in range((-GEN_RADIUS), GEN_RADIUS+1):
            self.mine_gen.gen_tile((self.player_loc[0] + (GEN_RADIUS * direction), self.player_loc[1] + i))
    
    def gen_row(self, direction):
        for i in range((-GEN_RADIUS), GEN_RADIUS+1):
            self.mine_gen.gen_tile((self.player_loc[0] + i, self.player_loc[1] + (GEN_RADIUS * direction)))
        
    def calc_breaking_time(self, hardness):
        depth_mod = self.player_depth ** self.player_mining_attenuation
        hardness_mod = depth_mod * hardness
        final_time = hardness_mod / self.player_mining_speed
        return final_time
           
    def drill_tile(self, dt):
        # break the block based on mining speed stat, fails and stops you there if you cannot afford to
        if self.current_break_time == 0:
            self.screen_shift = (0, 0)
            self.current_move_time = 0
            self.is_moving = True
        self.current_break_time += dt
        self.move_time = self.break_time * 0.5
        
        if self.current_break_time >= self.break_time:
            print(f"Mining completed. Broken: {self.mine_gen.mine_map.get(self.tile_target, "stone")}, Duration: {self.break_time}s") 
            self.mine_gen.mine_map[self.tile_target] = "air"
            self.move_time = 25 / self.player_movespeed
            self.current_move_time = self.move_time * 0.5
            self.is_moving = True
            self.is_mining = False
        elif self.current_break_time >= (self.break_time * 0.5) and self.is_moving:
            self.is_moving = False
    
    def move(self, dt):
        if self.is_mining:
            self.current_move_time += (dt * 0.5)
        else:
            self.current_move_time += dt
        progress = self.current_move_time/self.move_time
        self.screen_shift = (self.move_vec[0] * progress * TILE_SIZE, self.move_vec[1] * progress * TILE_SIZE)
        if self.current_move_time >= self.move_time:
            if self.move_vec[0] != 0:
                self.gen_col(self.move_vec[0])
            else:
                self.gen_row(self.move_vec[1])
            self.screen_shift = (0, 0)
            self.player_loc = self.tile_target
            self.is_moving = False
            self.player_depth = abs(self.player_loc[1])
            print(f"Finished Movement. Location: {self.player_loc}, Depth: {self.player_depth}")

    def check_move(self, dx, dy):
        if self.is_mining or self.is_moving:
            return
        if (self.player_depth == 1) and (dy == -1):
            print("Cant go higher")
            return
        
        self.tile_target = (self.player_loc[0] + dx, self.player_loc[1] + dy)
        self.move_vec = (dx, dy)
        
        if self.mine_gen.mine_map.get(self.tile_target, "stone") not in self.mine_gen.walkable_tile:
            tile = self.mine_gen.mine_map.get(self.tile_target, "stone")
            tile_info = self.ore_dict[tile]
            if self.player_mining_tier >= tile_info["tier"]:
                self.is_mining = True
                self.current_break_time = 0
                self.break_time = self.calc_breaking_time(hardness=tile_info["hardness"])
                print(f"Mining started. Target: {self.tile_target}")
        else:
            self.is_moving = True
            self.current_move_time = 0
            self.move_time = 25 / self.player_movespeed
            print(f"Movement Started. Target: {self.tile_target}")
            
    def draw_map(self):
        # TODO add & preload tinted art for ores/stone/bg
        mining_block = None
        mining_colour = None
        for dx in range(-RADIUS, RADIUS+1):
            for dy in range(-RADIUS, RADIUS+1):
                world_loc = (self.player_loc[0] + dx, self.player_loc[1] + dy)
                
                tile_type = self.mine_gen.mine_map.get(world_loc, "stone")
                
                screen_loc_x = ((dx + RADIUS - 1) * TILE_SIZE) - int(self.screen_shift[0])
                screen_loc_y = ((dy + RADIUS - 1) * TILE_SIZE) - int(self.screen_shift[1])
                
                
                if world_loc[1] >= 1:    
                    if tile_type in self.mine_gen.walkable_tile:
                        colour = self.mine_gen.walkable_tile[tile_type]
                        
                    else:
                        colour = self.ore_colours[tile_type]
                
                    pygame.draw.rect(self.surface, colour, (screen_loc_x, screen_loc_y, TILE_SIZE, TILE_SIZE))
                    
                    if self.is_mining:
                        mining_block = pygame.Rect(screen_loc_x, screen_loc_y, TILE_SIZE, TILE_SIZE)
                        mining_colour = colour
        return mining_block, mining_colour
                
                
    
    def update_time(self, dt):
        if self.is_mining:
            self.drill_tile(dt)
        if self.is_moving:
            self.move(dt)
                
    def mine_events(self, events):
        held_keys = pygame.key.get_pressed()
        if held_keys[pygame.K_UP]:
            self.check_move(0, -1)
        if held_keys[pygame.K_DOWN]:
            self.check_move(0, 1)
        if held_keys[pygame.K_LEFT]:
            self.check_move(-1, 0)
        if held_keys[pygame.K_RIGHT]:
            self.check_move(1, 0)
                    
                    
    def draw_mines(self, surface):
        self.surface.fill((0, 0, 0))

        extra_draw, colour = self.draw_map()
        
        self.surface.blit(self.player_img, self._image_rect)
        if extra_draw is not None:
            pygame.draw.rect(self.surface, colour, extra_draw)
        
        
        
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, 850, 850), 5)
        surface.blit(self.surface, (175, 75))