import gymnasium as gym
from gymnasium.wrappers import flatten_observation
from collections import defaultdict
import numpy as np

class BlackjackAgent:
    def __init__(self, env:gym.Env, 
                 learning_rate:float,
                initial_epsilon: float,
                epsilon_decay: float,
                final_epsilon: float,
                discount_factor: float = 0.95,
                ):
        """Initialize a Reinforcement Learning agent with an empty dictionary
        of state-action values (q_values), a learning rate and an epsilon.

        Args:
            env: The training environment
            learning_rate: The learning rate
            initial_epsilon: The initial epsilon value
            epsilon_decay: The decay for epsilon
            final_epsilon: The final epsilon value
            discount_factor: The discount factor for computing the Q-value
        """
        self.env = env
        self.q_values = defaultdict(lambda: np.zeros(self.env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        # For plotting metrics
        self.training_error = []
        self.epsilon_history = []

    def get_action(self, obs: tuple[int, int, bool]) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        # with probability (1 - epsilon) act greedily (exploit)
        else:
            return int(np.argmax(self.q_values[obs]))
            # print(np.argmax(self.q_values[obs]))
        
    def update(
        self,
        obs: tuple[int, int, bool],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: tuple[int, int, bool],
    ):
        """Updates the Q-value of an action."""
        temporal_difference = reward + self.discount_factor * np.max(
            self.q_values[next_obs]
        )
        self.q_values[obs][action] = (1-self.lr) * self.q_values[obs][action] + self.lr * temporal_difference
        # future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        # temporal_difference = (
        #     reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        # )

        # self.q_values[obs][action] = (
        #     self.q_values[obs][action] + self.lr * temporal_difference
        # )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
        
        self.epsilon_history.append(self.epsilon)

env = gym.make("LunarLander-v2", render_mode="human")

for _ in range(1):
    observation, info = env.reset()

    episode_over = False
    while not episode_over:
        action = env.action_space.sample()  # agent policy that uses the observation and info
        observation, reward, terminated, truncated, info = env.step(action)

        episode_over = terminated or truncated  # 结束条件或超时

# env.close()