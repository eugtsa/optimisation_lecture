from domain.world import World
from domain.level import Level
from helpers.exceptions import TargetFunctionCalledOnPointOutOfDomainError
import pygame

pygame.init()

SCALE = 50
SPRITES = {
    "pac": "./images/pac.png",
    "wall": "./images/wall.png",
    "fin_pos": "./images/fin_pos.png",
}
GAME_FONT = pygame.freetype.Font("./fonts/kongtext.ttf", SCALE / 2)


class WorldRenderSimple:
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    GREEN = (0, 70, 0)
    LGREEN = (0, 200, 0)
    RED = (100, 0, 0)
    YELLOW = (255, 174, 66)

    def __init__(self, level:Level, agent_name, scale:float) -> None:
        global SCREEN, CLOCK, GAME_FONT
        self.scale = scale
        GAME_FONT = pygame.freetype.Font("./fonts/kongtext.ttf", SCALE / 2 *scale)

        self.xsize = level.display_settings.sizex*level.display_settings.pixels_in_one_x_scale
        self.ysize = level.display_settings.sizey*level.display_settings.pixels_in_one_x_scale
        SCREEN = pygame.display.set_mode(
            (self.xsize, 
             self.ysize)
        )
        pygame.display.set_caption(agent_name)
        CLOCK = pygame.time.Clock()
        SCREEN.fill(self.BLACK)
        
        self.tf_landscape = self._create_and_draw_tf_pixel_array(SCREEN, level)
        #self._load_all_sprites()

    def _create_and_draw_tf_pixel_array(self, screen, level:Level):
        prev_p = None
        for pix_x in range(0,level.display_settings.sizex*level.display_settings.pixels_in_one_x_scale):

            x = level.display_settings.origin.x+float(pix_x)/level.display_settings.pixels_in_one_x_scale

            try:
                tf_value = level.target_function(x)
                y = int((tf_value-level.display_settings.origin.y)*level.display_settings.pixels_in_one_x_scale)
                color = self.GREEN
            except TargetFunctionCalledOnPointOutOfDomainError:
                color = self.RED
                y = 1

            if prev_p is None:
                pygame.draw.circle(
                    screen,
                    color,
                    (pix_x, self.ysize-y),
                    3,
                )
            else:
                pygame.draw.line(
                    screen,
                    color,
                    prev_p,
                    (pix_x, self.ysize-y),
                    3,
                )


            prev_p = (pix_x, self.ysize-y)
        
       
        return screen.copy() 
            

    def _load_all_sprites(self):
        for k, v in SPRITES.items():
            self.__dict__["_" + k] = self._load_sprite(v)

    def _load_sprite(self, sprite_file):
        sprite = pygame.image.load(sprite_file)
        return pygame.transform.scale(sprite, (SCALE, SCALE))

    def render_world(self, world: World):
        SCREEN.blit(self.tf_landscape, (0,0))

        self._draw_f_and_x(world.best_f,world.best_x, world.tick_num)

        cur_pos_x, cur_pos_y = world.cur_pos, world.level.target_function(world.cur_pos)

        self._draw_cur_pos(world,cur_pos_x, cur_pos_y)
        # self._draw_pac_man(world.cur_pos)
        if world.is_finished():
             self._draw_finish(world)
        pygame.display.update()

    def _draw_finish_pos(self, fin_pos):
        self._draw_sprite(fin_pos, self._fin_pos)

    def _draw_found_minimum(self, world: World,cur_pos_x,cur_pos_y,color=LGREEN):
        cur_pos = world.to_pixel_coords(cur_pos_x, cur_pos_y)
        
        pygame.draw.line(
            SCREEN,
            color,
            cur_pos,
            (cur_pos[0],cur_pos[1]+40),
            2,
        )
        pygame.draw.line(
            SCREEN,
            color,
            cur_pos,
            (cur_pos[0]+10,cur_pos[1]+40),
            2,
        )
        pygame.draw.line(
            SCREEN,
            color,
            cur_pos,
            (cur_pos[0]-10,cur_pos[1]+40),
            2,
        )

    def _draw_cur_pos(self, world: World,cur_pos_x,cur_pos_y,color=LGREEN):
        if cur_pos_x<world.level.display_settings.origin.x:
            # draw to left
            pygame.draw.circle(
                SCREEN,
                color,
                (0,0),
                4,
            )
        elif cur_pos_x>(world.level.display_settings.origin.x+world.level.display_settings.sizex):
            pygame.draw.circle(
                SCREEN,
                color,
                (self.xsize,0),
                4,
            )
        else:
            cur_pos = world.to_pixel_coords(cur_pos_x, cur_pos_y)
            print("cur_pos: {} {} ".format(cur_pos[0],cur_pos[1]))
            pygame.draw.circle(
                SCREEN,
                color,
                cur_pos,
                4,
            )

    def _draw_sprite(self, point, sprite):
        rect = sprite.get_rect()
        rect = rect.move((point.x * SCALE, point.y * SCALE))
        SCREEN.blit(sprite, rect)

    def _draw_finish(self,world):
        #self._draw_cur_pos(world,world.best_x, world.best_f)
        self._draw_found_minimum(world,world.best_x, world.best_f)

        GAME_FONT.render_to(
            SCREEN,
            (self.xsize/2-40, self.ysize/2),
            "FIN!",
            self.WHITE,
        )

    def _draw_f_and_x(self, f,x, tick_num: int):
        
        GAME_FONT.render_to(
            SCREEN, 
            (0, self.ysize-20), 
            "BEST F={}".format(f), self.WHITE
        )
        GAME_FONT.render_to(
            SCREEN, 
            (0, self.ysize-42), 
            "BEST X={}".format(x), self.WHITE
        )
        GAME_FONT.render_to(
            SCREEN,
            (0, 0),
            "TICK:{}".format(tick_num),
            self.WHITE,
        )

    def _draw_dot(self, dot_pos):
        pygame.draw.circle(
            SCREEN,
            self.YELLOW,
            (SCALE * dot_pos.x + SCALE / 2, SCALE * dot_pos.y + SCALE / 2),
            SCALE / 4,
        )
