import gym
import time
import pygame
import numpy as np
from copy import deepcopy
from gym import spaces


def draw_animation(image_path, screen, x, y, size):
    # Load and scale the image
    animation_image = pygame.image.load(image_path)
    animation_image = pygame.transform.scale(animation_image, (size, size))
    screen.blit(animation_image, (int(x), int(y)))


class GameEnvironment(gym.Env):
    def __init__(self):
        super(GameEnvironment, self).__init__()
        # Define the maze as a 2D numpy array
        self.maze = np.array([
            ['S', '.', '.', '.', '.', '.', '#'],
            ['.', '#', '.', '$', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '#', '.', '$', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '#', '.', '.'],
            ['#', '.', '$', '.', '.', '.', 'G'],
        ])
        self.grid_size = 7
        self.cell_size = 100
        self.state = None
        self.reward = 0
        self.info = {}
        self.goal = np.array((6, 6))
        self.done = False
        # test_hell_state_coordinates = [(1, 1), (2, 2), (4, 4)]
        # test_block_states = [(3, 3), (5, 5)]
        #
        # self.hell_states = test_hell_state_coordinates
        # self.block_states = test_block_states
        self.hell_states = [(1, 3), (3, 5), (6, 2), (0, 6), (2, 1), (3, 3), (5, 4), (5, 0)]
        self.block_states = [(0, 6), (2, 1), (3, 3), (5, 4), (5, 0)]

        # Action-space:
        self.action_space = gym.spaces.Discrete(4)

        # Observation space:
        self.observation_space = gym.spaces.Box(
            low=0, high=self.grid_size - 1, shape=(2,), dtype=np.int32)

        # # Setup pygame
        # pygame.init()
        # pygame.font.init()
        # self.font = pygame.font.SysFont('Arial', 75)
        # self.screen = pygame.display.set_mode(
        #     (self.cell_size * self.grid_size, self.cell_size * self.grid_size))

    def reset(self):
        self.state = np.array([0, 0])
        self.done = False
        self.reward = 0

        self.info["Distance to goal"] = np.sqrt(
            (self.state[0] - self.goal[0]) ** 2 +
            (self.state[1] - self.goal[1]) ** 2
        )

        return self.state, self.info

    def close(self):
        pass
        # pygame.quit()

    def step(self, action):
        previous_state = deepcopy(self.state)
        # Actions:
        # --------
        # Up:
        if action == 0 and self.state[0] > 0:
            self.state[0] -= 1
        # Down:
        if action == 1 and self.state[0] < self.grid_size - 1:
            self.state[0] += 1
        # Right:
        if action == 2 and self.state[1] < self.grid_size - 1:
            self.state[1] += 1
        # Left:
        if action == 3 and self.state[1] > 0:
            self.state[1] -= 1

        # Reward:
        # -------
        if np.array_equal(self.state, self.goal):  # Check goal condition
            self.reward += 20
            self.done = True
        # Check hell-states
        elif True in [np.array_equal(self.state, each_hell) for each_hell in self.hell_states]:
            if True in [np.array_equal(self.state, each_block) for each_block in self.block_states]:
                self.reward -= 2
                self.done = False
                # self.state = previous_state
            else:
                self.reward -= 6
                self.done = True
        else:  # Every other state
            self.reward += 0
            self.done = False

        # Info:
        # -----
        self.info["Distance to goal"] = np.sqrt(
            (self.state[0] - self.goal[0]) ** 2 +
            (self.state[1] - self.goal[1]) ** 2
        )

        return self.state, self.reward, self.done, self.info

    def is_valid_position(self, pos):
        row, col = pos
        if row < 0 or col < 0 or row >= self.num_rows or col >= self.num_cols:
            return False
        if self.maze[row, col] == '#':
            return False
        return True

    def display_message(self, message):
        pass
        # self.render()
        # message_surface = self.font.render(message, True, (255, 0, 0))
        # self.screen.blit(
        #     message_surface,
        #     (self.screen.get_width() // 2 - message_surface.get_width() // 2,
        #      self.screen.get_height() // 2 - message_surface.get_height() // 2)
        # )
        # pygame.display.update()
        # time.sleep(3)

    def render(self):
        pass
        # self.screen.fill((0, 0, 0))
        #
        # # Load background image
        # background_image = pygame.image.load('background.png')
        # background_image = pygame.transform.scale(background_image, (self.screen.get_width(), self.screen.get_height()))
        # self.screen.blit(background_image, (0, 0))
        #
        # # Draw grid lines
        # for x in range(0, self.screen.get_width(), self.cell_size):
        #     pygame.draw.line(self.screen, (100, 100, 100), (x, 0), (x, self.screen.get_height()))
        # for y in range(0, self.screen.get_height(), self.cell_size):
        #     pygame.draw.line(self.screen, (100, 100, 100), (0, y), (self.screen.get_width(), y))
        #
        # # Draw the maze elements
        # for row in range(self.grid_size):
        #     for col in range(self.grid_size):
        #         cell_left = col * self.cell_size
        #         cell_top = row * self.cell_size
        #         if self.maze[row, col] == '#':
        #             draw_animation("door.png", self.screen, cell_left, cell_top, self.cell_size)
        #         elif self.maze[row, col] == 'G':
        #             draw_animation("jewels.png", self.screen, cell_left, cell_top, self.cell_size)
        #         elif self.maze[row, col] == '$':
        #             draw_animation("wolf.png", self.screen, cell_left, cell_top, self.cell_size)
        #
        # # Draw the agent
        # draw_animation("queen.png", self.screen, self.state[1] * self.cell_size, self.state[0] * self.cell_size, self.cell_size)

        # pygame.display.update()
        # time.sleep(0.5)


def create_env():
    return GameEnvironment()
