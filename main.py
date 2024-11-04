# Imports:
# --------
# from padm_env import create_env
from Q_learning import train_q_learning, visualize_q_table
from env_sul3104 import create_env

# User definitions:
# -----------------
train = True
visualize_results = True

learning_rate = 0.01  # Learning rate
gamma = 0.99  # Discount factor
epsilon = 1.0  # Exploration rate
epsilon_min = 0.1  # Minimum exploration rate
epsilon_decay = 0.995  # Decay rate for exploration
no_episodes = 4000  # Number of episodes

goal_coordinates = (6, 6)
# Define all hell state coordinates as a tuple within a list
hell_state_coordinates = [(1, 3), (3, 5), (6, 2)]
block_states = [(0, 6), (2, 1), (3, 3), (5, 4), (5, 0)]
hell_state_coordinates += block_states

# test_hell_state_coordinates = [(1, 1), (2, 2), (4, 4)]
# test_block_states = [(3, 3), (5, 5)]
#
# hell_state_coordinates = test_hell_state_coordinates
# block_states = test_block_states
# hell_state_coordinates += block_states

# Execute:
# --------
if train:
    # Create an instance of the environment:
    # --------------------------------------
    env = create_env()

    # Train a Q-learning agent:
    # -------------------------
    train_q_learning(env=env,
                     no_episodes=no_episodes,
                     epsilon=epsilon,
                     epsilon_min=epsilon_min,
                     epsilon_decay=epsilon_decay,
                     alpha=learning_rate,
                     gamma=gamma)

if visualize_results:
    # Visualize the Q-table:
    # ----------------------
    visualize_q_table(hell_state_coordinates=hell_state_coordinates,
                      goal_coordinates=goal_coordinates,
                      q_values_path="q_table.npy")
