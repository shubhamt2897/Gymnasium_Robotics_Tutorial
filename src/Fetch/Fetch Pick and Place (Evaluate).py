# File: evaluate.py

import gymnasium as gym
import gymnasium_robotics
from stable_baselines3 import DDPG

print("\n--- Evaluating Trained Agent ---")

# File path where the trained model is saved
model_path = "fetch_pick_and_place_ddpg_her.zip"

# 1. Create the evaluation environment FIRST.
# We need this to pass to the .load() function.
eval_env = gym.make("FetchPickAndPlace-v3", render_mode="human")

# 2. Load the trained model.
# CRITICAL: You must pass the 'env' argument when loading a model
# that was trained using HerReplayBuffer.
model = DDPG.load(model_path, env=eval_env)

# 3. Run the evaluation loop for 10 episodes
for episode in range(10):
    # Reset the environment to get the initial observation
    obs, info = eval_env.reset()
    print(f"\n--- Starting Evaluation Episode {episode + 1} ---")
    
    done = False
    while not done:
        # Use the trained model to predict the best action
        # 'deterministic=True' means we don't use action noise during evaluation
        action, _states = model.predict(obs, deterministic=True)

        # Take the action in the environment
        obs, reward, terminated, truncated, info = eval_env.step(action)
        
        # An episode is done if it's terminated (goal reached) or truncated (time limit)
        done = terminated or truncated

        # Check if the goal was achieved in this step
        # For Fetch envs, a reward of 0 means success
        if reward == 0:
            print("Goal achieved!")

print("\nEvaluation finished.")
eval_env.close()