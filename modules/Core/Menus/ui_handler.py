from modules import EnhancedRect, MineDisplay


class UIHandler:
    def __init__(self):
        # buttons and stuff go here, all menus are created/destroyed here.
        # menu stack to handle stacking menus, also just has permanent ui elements here
        # buttons create menu and put ontop of stack, each menu has a button for nuking itself off the stack.
        self.mine_disp = MineDisplay()
        self.disp_stack = []
        
        pass
    
    def handler_time_updates(self, dt):
        # time delta for anything time related thats irrespective of frames
        self.mine_disp.update_time(dt)

    
    def handler_events(self, events, mouse_pos):
        # handle UI events based on whats ontop of the stack. Handles itself if nothing is ontop.
        self.mine_disp.mine_events(events)
    
    def handler_draws(self, surface):
        # Draws everything in order of the stack with itself and other UI elements always at the bottom
        self.mine_disp.draw_mines(surface)
        

