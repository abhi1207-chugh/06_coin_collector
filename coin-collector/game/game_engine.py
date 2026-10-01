import random
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
STARTING_LIVES = 3
ROUND_DURATION = 30

COIN_TYPES = [
    ("bronze", 1, (205, 127, 50)),
    ("silver", 3, (192, 192, 192)),
    ("gold", 5, (255, 215, 0)),
]


class GameEngine:
    def __init__(self):
        self.start_x = WIDTH / 2
        self.start_y = HEIGHT / 2
        self.round_duration = ROUND_DURATION

        self.reset_round()

    def reset_round(self):
        self.player = Player(
            x=self.start_x,
            y=self.start_y
        )

        self.score = 0
        self.lives = STARTING_LIVES

        self.obstacles = self._create_obstacles()

        self.coins = [
            self._random_coin(index)
            for index in range(NUM_COINS)
        ]

        self.start_time = pygame.time.get_ticks()
        self.remaining_time = self.round_duration
        self.game_over = False

    def _create_obstacles(self):
        return [
            pygame.Rect(150, 120, 120, 25),
            pygame.Rect(430, 100, 120, 25),
            pygame.Rect(250, 280, 200, 25),
            pygame.Rect(100, 390, 140, 25),
        ]

    def _random_coin(self, index):
        coin_type, value, color = COIN_TYPES[
            index % len(COIN_TYPES)
        ]

        for _ in range(100):
            x = random.randint(30, WIDTH - 30)
            y = random.randint(30, HEIGHT - 30)

            coin_rect = pygame.Rect(
                int(x - 12),
                int(y - 12),
                24,
                24
            )

            if any(
                coin_rect.colliderect(obstacle)
                for obstacle in self.obstacles
            ):
                continue

            if coin_rect.colliderect(
                self.player.get_rect()
            ):
                continue

            return Coin(
                x=x,
                y=y,
                radius=12,
                value=value,
                color=color,
                coin_type=coin_type
            )

        return Coin(
            x=50,
            y=50,
            radius=12,
            value=value,
            color=color,
            coin_type=coin_type
        )

    def handle_input(self, keys_pressed):
        if self.game_over:
            if keys_pressed[pygame.K_r]:
                self.reset_round()
            return

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
        if self.game_over:
            return

        elapsed_seconds = (
            pygame.time.get_ticks() - self.start_time
        ) / 1000

        self.remaining_time = max(
            0,
            self.round_duration - elapsed_seconds
        )

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

        player_rect = self.player.get_rect()

        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle):
                self.lives -= 1

                self.player.x = self.start_x
                self.player.y = self.start_y

                break

        if (
            self.remaining_time <= 0
            or self.lives <= 0
        ):
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.player,
            self.coins,
            self.obstacles
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 40)
        )

        renderer.draw_text(
            surface,
            font,
            f"Time: {int(self.remaining_time)}",
            (10, 70)
        )

        if self.game_over:
            renderer.draw_game_over(
                surface,
                font,
                self.score
            )
