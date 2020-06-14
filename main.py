import pygame
from GameClass import Game
import time
from threading import Thread

pygame.init()
GAME_START: int = False
game = Game(False, 10, 60)
game.start()
game.bg_screen_draw()
game.on_start()
pygame.display.update()
clock_thread = Thread(target=game.clock_thread)
clock_thread.start()


def main():
    try:
        while not GAME_START:
            time.sleep(0.01)
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    print("Stop")
                    game.stop_event_listener = True
                    game.stop_thread = True
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    keys_p = pygame.key.get_pressed()
                    if keys_p[pygame.K_ESCAPE]:
                        print("Escape to Stop")
                        game.stop_event_listener = True
                        game.stop_thread = True
                        pygame.quit()
                        quit()
                    if keys_p[pygame.K_RETURN]:
                        print("Start")
                        if game.FINISH_GAME:
                            game.on_start()
                        game.stop_thread = False
                        thread1 = Thread(target=game.timer_thread)
                        thread1.start()
                        # run_play_thread = Thread(target=game.run_play)
                        # run_play_thread.start()
                        # run_play_thread.join()
                        game.run_play()
                        game.stop_thread = True
                        game.finish_stat()
    finally:
        game.stop_thread = True
        game.stop_event_listener = True
        pygame.quit()
        quit()


if __name__ == "__main__":
    main()
