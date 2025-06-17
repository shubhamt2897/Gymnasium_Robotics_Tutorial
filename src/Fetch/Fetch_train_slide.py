
import gymnasium as gym
import gymnasium_robotics
# FIX 2A: Import DDPG AND HerReplayBuffer
from stable_baselines3 import DDPG, HerReplayBuffer
from stable_baselines3.common.noise import NormalActionNoise
import numpy as np

# --- Configuration ---
# FIX 1: Use the v3 version of the environment
ENV_ID = "FetchSlide-v3"
MODEL_FILENAME = "fetch_slide_model.zip"
LOG_DIR = "./her_fetch_slide_tensorboard/"
TRAINING_STEPS = 1_000_000

# --- Environment and Model Setup ---
train_env = gym.make(ENV_ID)

# FIX 2B: Use the HerReplayBuffer class directly, not the string "her"
replay_buffer_class = HerReplayBuffer
replay_buffer_kwargs = dict(
    n_sampled_goal=4,
    goal_selection_strategy="future",
    #max_episode_length=50 # This should match the environment's time limit
)
n_actions = train_env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

model = DDPG(
    "MultiInputPolicy",
    train_env,
    replay_buffer_class=replay_buffer_class,
    replay_buffer_kwargs=replay_buffer_kwargs,
    action_noise=action_noise,
    verbose=1,
    tensorboard_log=LOG_DIR,
)

# --- Training ---
print(f"--- Starting training for {ENV_ID} ---")
model.learn(total_timesteps=TRAINING_STEPS)
model.save(MODEL_FILENAME)
print(f"--- Training Complete. Model saved to {MODEL_FILENAME} ---")
train_env.close()