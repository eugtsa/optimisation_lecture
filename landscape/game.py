from time import sleep
from yaml import parse
import logging
from domain.base_algo import BaseAlgo
from helpers.exceptions import (
    RetryLevelException,
    NextLevelException,
    QuitGameException,
)
from helpers.level_loader import LevelLoader
from domain.rules import Rules
from domain.world import World
from helpers.world_renderer_simple import WorldRenderSimple
from helpers.key_press import press_any_key
import importlib
import argparse
import pygame

global AGENT_NAME

def raise_if_special_keys_pressed():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise QuitGameException()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                raise NextLevelException()
            if event.key == pygame.K_r:
                raise RetryLevelException()
            if event.key == pygame.K_q:
                raise QuitGameException()


def play_level(current_world: World, algo_class: BaseAlgo, args):
    if not args.daemon:
        wrs = WorldRenderSimple(
            current_world.level,
            agent_name=ALGO_NAME,
            scale=args.scale)

    algo = algo_class()

    if not args.daemon:
        wrs.render_world(current_world)

    # draw initital world
    best_x,best_f = None,None
    while not current_world.is_finished():

        next_iter = algo.get_next_iteration(
            current_world,
            current_world.level.target_function,
            current_world.level.target_function.deriv,
            current_world.level.target_function.dderiv
        )
        
        # track best x best f
        if best_x is None:
            best_x = next_iter
            best_f = current_world.level.target_function(next_iter)
            print(best_f,best_x)
        else:
            new_f = current_world.level.target_function(next_iter)
            if new_f<best_f:
                best_f,best_x = new_f, next_iter
                print(best_f,best_x)

        current_world.update_cur_pos(next_iter)
        current_world.tick_num +=1
        current_world.score = best_f
        current_world.best_x = best_x
        current_world.best_f = best_f

        if not args.daemon:
            wrs.render_world(current_world)
            sleep(0.1)
            raise_if_special_keys_pressed()
        # draw world + score
    if not args.daemon:
        wrs.render_world(current_world)
        press_any_key()
    return current_world.score


def to_classname(module_name: str):
    return "".join(w.capitalize() for w in module_name.split("_"))


def load_algo_class(algo_name: str):
    algo_module_name = algo_name
    algo_module = importlib.import_module("algos." + algo_module_name)
    return getattr(algo_module, to_classname(algo_module_name))


def main(args):
    algo_class = load_algo_class(args.algo)
    ll = LevelLoader()
    total_score = 0

    for level_name in ll.list_levels():
        level_finished = False

        while not level_finished:
            try:
                level = ll.load_level(level_name)
                level.display_settings.pixels_in_one_x_scale = int(level.display_settings.pixels_in_one_x_scale*args.scale)
                
                current_world = World(level, level.start_pos, total_score)
                
                score = play_level(current_world, algo_class, args)
                total_score = score
                level_finished = True
            except NextLevelException as e:
                level_finished = True
                break
            except RetryLevelException as e:
                pass
            except Exception as e:
                if type(e) == RetryLevelException:
                    pass
                else:
                    print("Algorithm broke! Please debug!")
                    logging.exception(e)
                    level_finished = True
                    press_any_key()
                    break
    print("Total game score: {}".format(total_score))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algo", type=str, default="monte_carlo")
    parser.add_argument('-d',"--daemon", action='store_true')
    parser.add_argument("-s", "--scale", type=float, default=1.0)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ALGO_NAME = args.algo
    main(args)
