import json, random

class MineGenerator:
    def __init__(self):
        self.base_seed = None
        with open("modules\Core\Mines\ores.json", "r", encoding='utf-8') as f:
            self.ore_dict = json.load(f)
        
        self.mine_map = {}
        self.start = None
            
        self.walkable_tile = {
            "air": (0, 0, 0),
        }
        
        
    def gen_new(self, start=(0, 1)):
        self.base_seed = random.randint(1000000, 9999999)
        
        self.start = start
        
        self.mine_map[start] = "air"
        
        print(f"New mine created seed: {self.base_seed}, Starting location: {self.start}")

        for x in range(-20, 21):
            for y in range(-20, 21):
                self.gen_tile((x, y))

    def gen_tile(self, coords):
        x, y = coords
        if (x, y) in self.mine_map:
            return

        for ore, data in self.ore_dict.items():
            if y > data["depth"]:
                rng = random.Random(f"{x}_{y}_{ore}_{self.base_seed}")
                if rng.random() < (data["rarity"] / 1000):
                    self.gen_vein(x, y, ore, data["size"])
                    return 

    def gen_vein(self, x, y, ore, max_size):
        vein_rng = random.Random(f"vein_{x}_{y}_{ore}_{self.base_seed}")
        placed = 0

        ore_tiles = set()
        ore_tiles.add((x, y))
        self.mine_map[(x, y)] = ore
        placed += 1

        attempts = 0
        max_attempts = max_size * 5 

        while placed < max_size and attempts < max_attempts:
            base_x, base_y = vein_rng.choice(list(ore_tiles))


            dx = vein_rng.randint(-2, 2)
            dy = vein_rng.randint(-2, 2)
            if abs(dx) + abs(dy) > 2 or (dx == 0 and dy == 0):
                attempts += 1
                continue  
               
            nx, ny = base_x + dx, base_y + dy

            if (nx, ny) in self.mine_map:
                if self.mine_map[(nx, ny)] in self.walkable_tile:
                    attempts += 1
                    continue  
                if self.mine_map[(nx, ny)] == ore:
                    attempts += 1
                    continue 
            if (nx, ny) in ore_tiles:
                attempts += 1
                continue 
            
            self.mine_map[(nx, ny)] = ore
            ore_tiles.add((nx, ny))
            placed += 1
            attempts += 1

