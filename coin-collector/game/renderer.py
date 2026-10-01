import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_OBSTACLE = (200, 70, 70)


def draw_scene(surface, player, coins, obstacles=None):
    surface.fill(COLOR_BG)

    if obstacles:
        for obstacle in obstacles:
            pygame.draw.rect(
                surface,
                COLOR_OBSTACLE,
                obstacle,
                border_radius=4
            )

    for coin in coins:
        pygame.draw.circle(
            surface,
            coin.color,
            (int(coin.x), int(coin.y)),
            coin.radius
        )

    pygame.draw.rect(
        surface,
        COLOR_PLAYER,
        player.get_rect(),
        border_radius=4
    )


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(
        font.render(text, True, color),
        pos
    )


def draw_game_over(surface, font, score):
    overlay = pygame.Surface(
        (
            surface.get_width(),
            surface.get_height()
        ),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    game_over_text = font.render(
        "GAME OVER",
        True,
        (255, 255, 255)
    )

    score_text = font.render(
        f"Final Score: {score}",
        True,
        (255, 255, 255)
    )

    restart_text = font.render(
        "Press R to start a new round",
        True,
        (255, 255, 255)
    )

    center_x = surface.get_width() // 2
    center_y = surface.get_height() // 2

    surface.blit(
        game_over_text,
        game_over_text.get_rect(
            center=(center_x, center_y - 40)
        )
    )

    surface.blit(
        score_text,
        score_text.get_rect(
            center=(center_x, center_y)
        )
    )

    surface.blit(
        restart_text,
        restart_text.get_rect(
            center=(center_x, center_y + 40)
        )
    )
