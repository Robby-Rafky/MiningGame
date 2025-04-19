from modules import pygame

class EnhancedRect(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.label = " "
        self.image = None
        self.base_image = None
        self.clickable = False
        self.bg_color = None
        self.border_color = None
        self.show_label = False
        self.img_is_coloured = False
        self.alignment = None
        self.text_colour = None

        self._label_surfaces = None
        self.label_font_size = None
        self._label_min_font_size = None
        self._line_spacing = None
        self._font_name = "Assets/ModernDOS9x16.ttf"
        self._label_padding = None
        self._image_rect = None
        
# -------------------------------------- LABEL STUFF ----------------------------------------------

    def add_label(self, font_size=36, min_font_size=None, line_spacing=5, text_colour=(0, 0, 0), alignment="center"):
        self.label_font_size = font_size
        self.text_colour = text_colour
        self.alignment = alignment
        self._label_min_font_size = min_font_size or font_size
        self._line_spacing = line_spacing
        return self
    
    def set_alignment(self, alignment):
        self.alignment = alignment
        return self
    
    def set_text_colour(self, text_colour=(0, 0, 0)):
        self.text_colour = text_colour
        return self
        
    def update_label(self, text=None):
        self.show_label = True
        self.label = text or self.label
        self._prepare_label_text(self.label_font_size, self._label_min_font_size, self._line_spacing)
        return self
    
    def label_visible(self, show_label=True):
        self.show_label = show_label
        return self

    def _prepare_label_text(self, font_size, min_font_size, line_spacing):
        padding = 10
        text_area_width = self.width - 2 * padding
        text_area_height = self.height - 2 * padding

        while font_size >= min_font_size:
            font = pygame.font.Font(self._font_name, font_size)
            words = self.label.split(" ")
            lines = []
            line = ""

            for word in words:
                test_line = line + word + " "
                if font.size(test_line)[0] <= text_area_width:
                    line = test_line
                else:
                    lines.append(line.strip())
                    line = word + " "
            lines.append(line.strip())

            total_height = len(lines) * font.get_height() + (len(lines) - 1) * line_spacing
            if total_height <= text_area_height:
                self._label_surfaces = [(font.render(l, True, self.text_colour), font) for l in lines]
                self._label_padding = padding
                return
            font_size -= 1

        smallest_font = pygame.font.Font(self._font_name, min_font_size)
        self._label_surfaces = [(smallest_font.render(self.label, True, self.text_colour), smallest_font)]
        self._label_padding = padding

# -------------------------------------- IMAGE STUFF ----------------------------------------------

    def add_img(self, image_path):
        self.base_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.base_image
        self.scale_img()
        return self
    
    def scale_img(self, scale=(100, 100)):
        self.image = pygame.transform.scale(self.image, scale)
        self._image_rect = self.image.get_rect(center=self.center)
        return self
        
    def colour_img(self, colour=(0, 0, 0)):
        img_final = self.base_image.copy()
        img_coloured = pygame.Surface(self.base_image.get_size())
        img_coloured.fill(colour)
        img_final.blit(img_coloured, (0, 0), special_flags=pygame.BLEND_MULT)
        img_scale = self.image.get_size()
        self.image = img_final
        self.scale_img(img_scale)
        return self

# -------------------------------------- BUTTON STUFF ---------------------------------------------

    def add_button(self):
        self.is_clickable()
        return self

    def is_clickable(self, flag=True):
        self.clickable = flag
        return self

    def button_event(self, mouse_pos):
        return self.clickable and self.hover_event(mouse_pos)
        
# -------------------------------------- TOOLTIP STUFF --------------------------------------------

# TODO - ADD THIS LATER
    def add_tooltip(self):
        return self

    

# -------------------------------------- GENERAL STUFF --------------------------------------------

    def hover_event(self, mouse_pos):
        return self.collidepoint(mouse_pos)

    def set_colours(self, bg_colour=(180, 180, 180), border_colour=(0, 0, 0)):
        self.bg_color = bg_colour
        self.border_color = border_colour
        return self

    def draw(self, surface):
        if self.bg_color:
            pygame.draw.rect(surface, self.bg_color, self)
        if self.border_color:
            pygame.draw.rect(surface, self.border_color, self, 2)
        if self.image:
            surface.blit(self.image, self._image_rect.topleft)
        if self.show_label:
            total_height = sum(surf.get_height() for surf, _ in self._label_surfaces) + self._line_spacing * (len(self._label_surfaces) - 1)
            y_offset = self.top + self._label_padding + (self.height - 2 * self._label_padding - total_height) // 2

            for surf, font in self._label_surfaces:
                if self.alignment == 'left':
                    x = self.left + self._label_padding
                elif self.alignment == 'right':
                    x = self.right - self._label_padding - surf.get_width()
                else:
                    x = self.centerx - surf.get_width() // 2
                surface.blit(surf, (x, y_offset))
                y_offset += surf.get_height() + self._line_spacing
