import gymnasium as gym
import gymnasium_robotics
from stable_baselines3 import SAC
from stable_baselines3.her.her_replay_buffer import HerReplayBuffer
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from gymnasium.wrappers import FlattenObservation
import numpy as np
import os

# --- Configuration ---
ENV_ID = "FrankaKitchen-v1"
MODEL_FILENAME = "kitchen_microwave_model"
TRAINING_STEPS = 1_000_000
LOG_DIR = "./logs/"
MODEL_DIR = "./models/"

# Create directories
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# --- Environment Setup ---
def make_env():
    env = gym.make(
        ENV_ID,
        tasks_to_complete=['microwave'],
        render_mode=None
    )
    # Flatten the observation space to handle nested Dict spaces
    env = FlattenObservation(env)
    return env

env = make_env()
env = Monitor(env, LOG_DIR)

# Create evaluation environment
def make_eval_env():
    eval_env = gym.make(
        ENV_ID,
        tasks_to_complete=['microwave'],
        render_mode=None
    )
    eval_env = FlattenObservation(eval_env)
    return eval_env

eval_env = make_eval_env()
eval_env = Monitor(eval_env, LOG_DIR + "eval/")

# --- Model Setup ---
# For flattened environments, we can't use HER directly
# Use standard SAC without HER for now
model = SAC(
    "MlpPolicy",  # Changed from MultiInputPolicy to MlpPolicy for flattened obs
    env,
    learning_rate=1e-3,
    buffer_size=1_000_000,
    learning_starts=1000,
    batch_size=256,
    tau=0.05,
    gamma=0.95,
    train_freq=1,
    gradient_steps=1,
    verbose=1,
    device="cuda",
    tensorboard_log=LOG_DIR
)

# --- Callbacks ---
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path=MODEL_DIR,
    log_path=LOG_DIR,
    eval_freq=10000,
    deterministic=True,
    render=False
)

checkpoint_callback = CheckpointCallback(
    save_freq=50000,
    save_path=MODEL_DIR,
    name_prefix=MODEL_FILENAME
)

# --- Training ---
print(f"--- Training agent for task: 'microwave' ---")
print(f"Total timesteps: {TRAINING_STEPS}")

model.learn(
    total_timesteps=TRAINING_STEPS,
    callback=[eval_callback, checkpoint_callback],
    log_interval=1000
)

# Save final model
model.save(os.path.join(MODEL_DIR, MODEL_FILENAME))
print(f"--- Training complete. Model saved to {MODEL_DIR}{MODEL_FILENAME} ---")

env.close()
eval_env.close()