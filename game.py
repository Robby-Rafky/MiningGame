from modules import EnhancedRect, UIHandler, pygame

class Game:
    def __init__(self):
        pygame.init()
        
        self.running = True
        
        self.window = pygame.display.set_mode((1200, 1000))
        self.game_screen = pygame.Surface((1200, 1000))
        
        self.game_clock = pygame.time.Clock()
        
        self.ui_handler = UIHandler()

    
    def updates(self, dt):
        self.ui_handler.handler_time_updates(dt)
    
    def event_checking(self):
        # all event checks (feed mouse pos here)
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            
        self.ui_handler.handler_events(events, mouse_pos)
        
    def screen_layering(self):
        # all draw calls EVERYTHING WITH CLICKABLES BLITS TO 0, 0
        self.game_screen.fill((0, 0, 0))
        self.ui_handler.handler_draws(self.game_screen)
        pass
        
    def game_loop(self):
        self.event_checking()
        self.screen_layering()
        
        self.window.blit(self.game_screen, (0, 0))
        dt = self.game_clock.tick(60) / 1000
        self.updates(dt)
        pygame.display.flip()

pygame.quit()
