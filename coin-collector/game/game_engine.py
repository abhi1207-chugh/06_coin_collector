import random
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6

COIN_TYPES = [
    ("bronze", 1, (205, 127, 50)),
    ("silver", 3, (192, 192, 192)),
    ("gold", 5, (255, 215, 0)),
]


class GameEngine:
    def __init__(self):
        self.player = Player(
            x=WIDTH / 2,
            y=HEIGHT / 2
        )

        self.coins = [
            self._random_coin(index)
            for index in range(NUM_COINS)
        ]

        self.score = 0

    def _random_coin(self, index):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)

        coin_type, value, color = COIN_TYPES[
            index % len(COIN_TYPES)
        ]

        return Coin(
            x=x,
            y=y,
            radius=12,
            value=value,
            color=color,
            coin_type=coin_type
        )

    def handle_input(self, keys_pressed):
        dx = dy = 0

        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed

        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed

        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed

        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed

        self.player.move(
            dx,
            dy,
            WIDTH,
            HEIGHT
        )

    def update(self):
        collected = check_collection(
            self.player,
            self.coins
        )

        for coin in collected:
            self.score += coin.value

        self.coins = [
            coin for coin in self.coins
            if coin not in collected
        ]

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.player,
            self.coins
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )
