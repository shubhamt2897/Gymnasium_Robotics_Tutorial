# File: evaluate.py (Upgraded Version)

import gymnasium as gym
import gymnasium_robotics
from stable_baselines3 import DDPG
import numpy as np

print("\n--- Evaluating Trained Agent ---")

model_path = "fetch_pick_and_place_ddpg_her.zip" # <-- MAKE SURE THIS IS CORRECT

eval_env = gym.make("FetchPickAndPlace-v3", render_mode="human")
model = DDPG.load(model_path, env=eval_env)

# --- Variables for metrics ---
num_episodes = 50  # Run more episodes for a more reliable success rate
successful_episodes = 0
total_rewards = []

print(f"--- Running {num_episodes} Evaluation Episodes ---")

for episode in range(num_episodes):
    obs, info = eval_env.reset()
    done = False
    episode_reward = 0
    
    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = eval_env.step(action)
        
        episode_reward += reward
        done = terminated or truncated

        # Check for success at the end of the episode
        # The 'is_success' key in the info dict is the most reliable way
        if done and info.get('is_success'):
            successful_episodes += 1

    total_rewards.append(episode_reward)
    print(f"Episode {episode + 1}: Reward = {episode_reward:.2f} | Success = {info.get('is_success', False)}")


# --- Calculate and Print Final Metrics ---
success_rate = (successful_episodes / num_episodes) * 100
average_reward = np.mean(total_rewards)

print("\n\n--- Evaluation Complete ---")
print(f"Success Rate: {success_rate:.2f}% ({successful_episodes}/{num_episodes})")
print(f"Average Reward per Episode: {average_reward:.2f}")

eval_env.close()