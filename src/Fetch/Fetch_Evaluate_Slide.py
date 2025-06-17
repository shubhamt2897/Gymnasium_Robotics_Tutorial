# File: evaluate_slide.py

import gymnasium as gym
import gymnasium_robotics
from stable_baselines3 import DDPG

# --- Configuration ---
# These must EXACTLY match the parameters from your successful training run
ENV_ID = "FetchSlide-v3"
MODEL_FILENAME = "fetch_slide_model.zip"

# --- Evaluation ---
print(f"--- Evaluating model for {ENV_ID} ---")
print(f"Loading model from: {MODEL_FILENAME}")

# Create the evaluation environment with rendering
eval_env = gym.make(ENV_ID, render_mode="human")

# Load the trained model, providing the 'env' argument because it was trained with HER
model = DDPG.load(MODEL_FILENAME, env=eval_env)

# Run the evaluation loop for 10 episodes
for episode in range(10):
    obs, info = eval_env.reset()
    print(f"\n--- Starting Evaluation Episode {episode + 1} ---")
    done = False
    while not done:
        # Use the trained policy to predict the best action
        action, _states = model.predict(obs, deterministic=True)
        # Take the action in the environment
        obs, reward, terminated, truncated, info = eval_env.step(action)
        # Check if the episode has ended
        done = terminated or truncated

        # Check for success, which is the most reliable way for these envs
        if done and info.get('is_success'):
            print("Goal achieved!")

print("\nEvaluation finished.")
eval_env.close()