# File: evaluate_pretrained.py

import gymnasium as gym
import gymnasium_robotics
from stable_baselines3 import TD3
from huggingface_sb3 import load_from_hub

# --- Model Information ---
repo_id = "Edgar404/td3-FetchPickAndPlaceDense-v3"
filename = "td3-FetchPickAndPlaceDense-v3.zip"

# --- Download the Model ---
print(f"Downloading model from Hugging Face Hub: {repo_id}")
model_path = load_from_hub(repo_id, filename) # This will now use your logged-in credentials
print(f"Model downloaded successfully to: {model_path}")

# --- Evaluation ---
eval_env = gym.make("FetchPickAndPlace-v3", render_mode="human")
model = TD3.load(model_path, env=eval_env)

# ... (the rest of the evaluation loop is the same) ...
for episode in range(10):
    obs, info = eval_env.reset()
    print(f"\n--- Starting Evaluation Episode {episode + 1} ---")
    done = False
    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = eval_env.step(action)
        done = terminated or truncated

        if done and info.get('is_success'):
            print("Goal achieved!")

print("\nEvaluation finished.")
eval_env.close()