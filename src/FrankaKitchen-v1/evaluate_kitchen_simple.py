import gymnasium as gym
import gymnasium_robotics
from stable_baselines3 import SAC
from gymnasium.wrappers import FlattenObservation  # Add this import
import numpy as np
import time
import os

# --- Configuration ---
ENV_ID = "FrankaKitchen-v1"
MODEL_PATH = "./models/kitchen_microwave_model.zip"  # or best_model.zip
NUM_EPISODES = 10
RENDER_MODE = "human"  # Set to None for no rendering

def evaluate_model(model_path, num_episodes=10, render=True):
    """
    Evaluate a trained SAC model on FrankaKitchen environment
    """
    # Load the trained model
    if not os.path.exists(model_path):
        print(f"Model file not found: {model_path}")
        return
    
    model = SAC.load(model_path)
    print(f"Loaded model from: {model_path}")
    
    # Create environment (SAME AS TRAINING)
    env = gym.make(
        ENV_ID,
        tasks_to_complete=['microwave'],
        render_mode=RENDER_MODE if render else None
    )
    # Apply the same wrapper as training
    env = FlattenObservation(env)
    
    # Evaluation metrics
    episode_rewards = []
    episode_lengths = []
    success_count = 0
    
    print(f"--- Evaluating for {num_episodes} episodes ---")
    
    for episode in range(num_episodes):
        obs, info = env.reset()
        episode_reward = 0
        episode_length = 0
        done = False
        
        print(f"Episode {episode + 1}/{num_episodes}")
        
        while not done:
            # Get action from trained model
            action, _states = model.predict(obs, deterministic=True)
            
            # Take step in environment
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
            episode_reward += reward
            episode_length += 1
            
            if render:
                time.sleep(0.01)  # Small delay for better visualization
        
        # Check if task was completed successfully
        if info.get('is_success', False):
            success_count += 1
            print(f"  ✓ Success! Reward: {episode_reward:.2f}, Length: {episode_length}")
        else:
            print(f"  ✗ Failed. Reward: {episode_reward:.2f}, Length: {episode_length}")
        
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
    
    # Calculate statistics
    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)
    mean_length = np.mean(episode_lengths)
    success_rate = success_count / num_episodes
    
    print("\n--- Evaluation Results ---")
    print(f"Success Rate: {success_rate:.2%} ({success_count}/{num_episodes})")
    print(f"Mean Reward: {mean_reward:.2f} ± {std_reward:.2f}")
    print(f"Mean Episode Length: {mean_length:.1f}")
    print(f"Min Reward: {min(episode_rewards):.2f}")
    print(f"Max Reward: {max(episode_rewards):.2f}")
    
    env.close()
    return {
        'success_rate': success_rate,
        'mean_reward': mean_reward,
        'std_reward': std_reward,
        'mean_length': mean_length,
        'episode_rewards': episode_rewards
    }

def test_random_policy(num_episodes=5):
    """
    Test random policy for comparison
    """
    print("\n--- Testing Random Policy ---")
    
    env = gym.make(
        ENV_ID,
        tasks_to_complete=['microwave'],
        render_mode=None
    )
    # Apply same wrapper for fair comparison
    env = FlattenObservation(env)
    
    episode_rewards = []
    success_count = 0
    
    for episode in range(num_episodes):
        obs, info = env.reset()
        episode_reward = 0
        done = False
        
        while not done:
            action = env.action_space.sample()  # Random action
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            episode_reward += reward
        
        if info.get('is_success', False):
            success_count += 1
        
        episode_rewards.append(episode_reward)
    
    success_rate = success_count / num_episodes
    mean_reward = np.mean(episode_rewards)
    
    print(f"Random Policy - Success Rate: {success_rate:.2%}, Mean Reward: {mean_reward:.2f}")
    env.close()

if __name__ == "__main__":
    # Test random policy first for baseline
    test_random_policy()
    
    # Evaluate trained model
    if os.path.exists(MODEL_PATH):
        results = evaluate_model(MODEL_PATH, NUM_EPISODES, render=True)
    else:
        print(f"Model not found at {MODEL_PATH}")
        print("Please train a model first using train_kitchen_worker.py")