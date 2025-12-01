"""
Snake Game - Classic snake game implementation using Pygame.
Author: Your Name
Date: 2025
"""

import pygame
import random
import sys
from enum import IntEnum
from typing import Tuple, List


class Difficulty(IntEnum):
    """Game difficulty levels with corresponding frame rates."""
    SLOW = 7
    MEDIUM = 15
    FAST = 25


class Color:
    """Color palette for the game."""
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GREEN = (0, 200, 0)


class GameConfig:
    """Game configuration constants."""
    WIDTH = 600
    HEIGHT = 400
    BLOCK_SIZE = 20
    TITLE = "Snake Game"
    FONT_SIZE = 24
    FONT_LARGE = 32
    BEEP_FREQUENCY = 1000
    BEEP_DURATION = 300
    MAX_NAME_LENGTH = 20


class SnakeGame:
    """Main Snake game class."""

    def __init__(self, player_name: str = "Player", difficulty: Difficulty = Difficulty.MEDIUM):
        """Initialize the game with player name and difficulty."""
        pygame.init()
        self.player_name = player_name
        self.difficulty = difficulty
        self.screen = pygame.display.set_mode((GameConfig.WIDTH, GameConfig.HEIGHT))
        pygame.display.set_caption(GameConfig.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", GameConfig.FONT_SIZE)
        self.font_large = pygame.font.SysFont("Arial", GameConfig.FONT_LARGE, bold=True)
        self.reset_game()

    def reset_game(self) -> None:
        """Reset game state for a new game."""
        self.snake: List[Tuple[int, int]] = [(GameConfig.WIDTH // 2, GameConfig.HEIGHT // 2)]
        self.direction: Tuple[int, int] = (GameConfig.BLOCK_SIZE, 0)
        self.food_pos = self._spawn_food()
        self.score = 0
        self.game_over = False

    def _spawn_food(self) -> Tuple[int, int]:
        """Spawn food at a random location on the grid."""
        return (
            random.randrange(0, GameConfig.WIDTH, GameConfig.BLOCK_SIZE),
            random.randrange(0, GameConfig.HEIGHT, GameConfig.BLOCK_SIZE),
        )

    @staticmethod
    def _play_sound() -> None:
        """Play a beep sound on game over."""
        try:
            import winsound
            winsound.Beep(GameConfig.BEEP_FREQUENCY, GameConfig.BEEP_DURATION)
        except (ImportError, RuntimeError):
            print('\a')  # Fallback to system beep

    def _handle_input(self) -> bool:
        """Handle user input. Returns False if user quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                new_direction = self._key_to_direction(event.key)
                if new_direction and self._is_valid_direction(new_direction):
                    self.direction = new_direction
        return True

    @staticmethod
    def _key_to_direction(key: int) -> Tuple[int, int] | None:
        """Convert key press to direction vector."""
        key_map = {
            pygame.K_UP: (0, -GameConfig.BLOCK_SIZE),
            pygame.K_DOWN: (0, GameConfig.BLOCK_SIZE),
            pygame.K_LEFT: (-GameConfig.BLOCK_SIZE, 0),
            pygame.K_RIGHT: (GameConfig.BLOCK_SIZE, 0),
        }
        return key_map.get(key)

    def _is_valid_direction(self, direction: Tuple[int, int]) -> bool:
        """Check if direction is valid (not opposite to current direction)."""
        opposite = (-self.direction[0], -self.direction[1])
        return direction != opposite

    def _update_game_state(self) -> None:
        """Update snake position and check for collisions."""
        new_head = (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1],
        )

        # Check collisions
        if self._check_collision(new_head):
            self.game_over = True
            self._play_sound()
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food_pos:
            self.score += 1
            self.food_pos = self._spawn_food()
        else:
            self.snake.pop()

    def _check_collision(self, head: Tuple[int, int]) -> bool:
        """Check if the snake collided with walls or itself."""
        x, y = head
        # Wall collision
        if x < 0 or x >= GameConfig.WIDTH or y < 0 or y >= GameConfig.HEIGHT:
            return True
        # Self collision
        if head in self.snake:
            return True
        return False

    def _draw_game(self) -> None:
        """Draw all game elements."""
        self.screen.fill(Color.BLACK)
        self._draw_snake()
        self._draw_food()
        self._draw_score()
        pygame.display.flip()

    def _draw_snake(self) -> None:
        """Draw the snake on the screen."""
        for block in self.snake:
            pygame.draw.rect(
                self.screen,
                Color.GREEN,
                (block[0], block[1], GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE),
            )

    def _draw_food(self) -> None:
        """Draw food on the screen."""
        pygame.draw.rect(
            self.screen,
            Color.RED,
            (
                self.food_pos[0],
                self.food_pos[1],
                GameConfig.BLOCK_SIZE,
                GameConfig.BLOCK_SIZE,
            ),
    def _draw_score(self) -> None:
        """Draw the player name and score on the screen."""
        name_text = self.font.render(f"Player: {self.player_name}", True, Color.DARK_GREEN)
        score_text = self.font.render(f"Score: {self.score}", True, Color.WHITE)
        self.screen.blit(name_text, (10, 10))
        self.screen.blit(score_text, (10, 35))
        score_text = self.font.render(f"Score: {self.score}", True, Color.WHITE)
    def _draw_game_over_screen(self) -> None:
        """Draw the game over screen and wait for user input."""
        self.screen.fill(Color.BLACK)
        game_over_text = self.font_large.render("GAME OVER!", True, Color.RED)
        player_text = self.font.render(f"Player: {self.player_name}", True, Color.DARK_GREEN)
        score_text = self.font.render(f"Final Score: {self.score}", True, Color.WHITE)
        exit_text = self.font.render("Press any key to exit...", True, Color.WHITE)

        self.screen.blit(
            game_over_text,
            (
                GameConfig.WIDTH // 2 - game_over_text.get_width() // 2,
                GameConfig.HEIGHT // 2 - 80,
            ),
        )
        self.screen.blit(
            player_text,
            (
                GameConfig.WIDTH // 2 - player_text.get_width() // 2,
                GameConfig.HEIGHT // 2 - 20,
            ),
        )
        self.screen.blit(
            score_text,
            (
                GameConfig.WIDTH // 2 - score_text.get_width() // 2,
                GameConfig.HEIGHT // 2 + 20,
            ),
        )
        self.screen.blit(
            exit_text,
            (
                GameConfig.WIDTH // 2 - exit_text.get_width() // 2,
                GameConfig.HEIGHT // 2 + 80,
            ),
        )
        pygame.display.flip()

        # Wait for user input to exit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    waiting = Falsent.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    waiting = False

def get_player_name() -> str:
    """Get player name from user input."""
    print("\n" + "=" * 50)
    print("  🐍 WELCOME TO SNAKE GAME 🐍".center(50))
    print("=" * 50)
    
    while True:
        name = input(f"\nEnter your name (max {GameConfig.MAX_NAME_LENGTH} characters): ").strip()
        
        if not name:
            print("❌ Name cannot be empty. Please try again.")
            continue
        
        if len(name) > GameConfig.MAX_NAME_LENGTH:
            print(f"❌ Name is too long. Maximum {GameConfig.MAX_NAME_LENGTH} characters allowed.")
            continue
        
        print(f"✅ Welcome, {name}!")
        return name


def main() -> None:
    """Entry point for the game."""
    try:
        player_name = get_player_name()
        difficulty = select_difficulty()
        game = SnakeGame(player_name, difficulty)
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing! Goodbye!")
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        pygame.quit()
        sys.exit(1)
    while True:
        choice = input("\nEnter 1, 2, or 3: ").strip()
        difficulty_map = {"1": Difficulty.SLOW, "2": Difficulty.MEDIUM, "3": Difficulty.FAST}

        if choice in difficulty_map:
            selected = difficulty_map[choice]
            level_names = {Difficulty.SLOW: "Slow", Difficulty.MEDIUM: "Medium", Difficulty.FAST: "Fast"}
            print(f"✅ Difficulty set to: {level_names[selected]}\n")
            return selected
        print("❌ Invalid choice. Please enter 1, 2, or 3.")

def select_difficulty() -> Difficulty:
    """Display difficulty menu and get user selection."""
    print("\n" + "=" * 40)
    print("  SNAKE GAME - DIFFICULTY SELECTION")
    print("=" * 40)
    print("1 - Slow   (7 FPS)")
    print("2 - Medium (15 FPS) - Recommended")
    print("3 - Fast   (25 FPS)")
    print("=" * 40)

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        difficulty_map = {"1": Difficulty.SLOW, "2": Difficulty.MEDIUM, "3": Difficulty.FAST}

        if choice in difficulty_map:
            return difficulty_map[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


def main() -> None:
    """Entry point for the game."""
    try:
        difficulty = select_difficulty()
        game = SnakeGame(difficulty)
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()