# File: train.py

import gymnasium as gym
import gymnasium_robotics
from stable_baselines3 import DDPG, HerReplayBuffer
from stable_baselines3.common.noise import NormalActionNoise
import numpy as np

# 1. Define Model and Training Parameters
model_class = DDPG
goal_selection_strategy = "future"
N_SAMPLED_GOAL = 4
model_path = "fetch_pick_and_place_ddpg_her.zip"

# 2. Create the Gym environment
env = gym.make("FetchPickAndPlace-v3")

# 3. Setup the HER Replay Buffer
replay_buffer_kwargs = {
    "n_sampled_goal": N_SAMPLED_GOAL,
    "goal_selection_strategy": goal_selection_strategy,
}
n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

# 4. Instantiate the DDPG model with HER
model = model_class(
    "MultiInputPolicy",
    env,
    replay_buffer_class=HerReplayBuffer,
    replay_buffer_kwargs=replay_buffer_kwargs,
    action_noise=action_noise,
    verbose=1,
    tensorboard_log="./her_fetch_tensorboard/",
)

# 5. Train the model
print("Starting model training...")
model.learn(total_timesteps=100000)

# 6. Save the trained model
print("Training finished. Saving model...")
model.save(model_path)
print(f"Model saved to {model_path}")

env.close()