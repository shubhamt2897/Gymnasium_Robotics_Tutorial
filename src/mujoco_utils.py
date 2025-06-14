"""
MuJoCo utilities and helper functions for common tasks.
"""

import gymnasium as gym
import numpy as np
import os
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any, Optional

def create_mujoco_env(env_id: str, render_mode: str = "human") -> gym.Env:
    """
    Create a MuJoCo environment with specified render mode.
    
    Args:
        env_id: The Gymnasium environment ID
        render_mode: The rendering mode (human, rgb_array, depth_array)
        
    Returns:
        The initialized Gymnasium environment
    """
    try:
        env = gym.make(env_id, render_mode=render_mode)
        print(f"Successfully created environment: {env_id}")
        return env
    except Exception as e:
        print(f"Error creating environment {env_id}: {e}")
        raise

def set_mujoco_rendering_backend(backend: str) -> None:
    """
    Set the MuJoCo rendering backend.
    
    Args:
        backend: One of 'glfw', 'egl', or 'osmesa'
    """
    valid_backends = ['glfw', 'egl', 'osmesa']
    if backend not in valid_backends:
        raise ValueError(f"Backend must be one of {valid_backends}")
    
    os.environ['MUJOCO_GL'] = backend
    print(f"Set MuJoCo rendering backend to: {backend}")

def run_random_episode(env: gym.Env, max_steps: int = 1000, render: bool = True) -> Tuple[float, int]:
    """
    Run a random episode in the environment.
    
    Args:
        env: The Gymnasium environment
        max_steps: Maximum number of steps to run
        render: Whether to render the environment
        
    Returns:
        Tuple of (total_reward, steps_taken)
    """
    observation, info = env.reset()
    total_reward = 0
    steps = 0
    
    for step in range(max_steps):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        
        total_reward += reward
        steps += 1
        
        if render:
            env.render()
        
        if terminated or truncated:
            break
    
    return total_reward, steps

def evaluate_policy(env: gym.Env, policy_fn, num_episodes: int = 10) -> Dict[str, Any]:
    """
    Evaluate a policy over multiple episodes.
    
    Args:
        env: The Gymnasium environment
        policy_fn: Function that takes an observation and returns an action
        num_episodes: Number of episodes to run
        
    Returns:
        Dictionary with evaluation metrics
    """
    rewards = []
    episode_lengths = []
    
    for episode in range(num_episodes):
        observation, info = env.reset()
        done = False
        episode_reward = 0
        steps = 0
        
        while not done:
            action = policy_fn(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward
            steps += 1
            done = terminated or truncated
        
        rewards.append(episode_reward)
        episode_lengths.append(steps)
        print(f"Episode {episode+1}: Reward = {episode_reward:.2f}, Steps = {steps}")
    
    return {
        "mean_reward": np.mean(rewards),
        "std_reward": np.std(rewards),
        "min_reward": np.min(rewards),
        "max_reward": np.max(rewards),
        "mean_episode_length": np.mean(episode_lengths),
        "rewards": rewards,
        "episode_lengths": episode_lengths
    }

def visualize_rewards(rewards: List[float], title: str = "Episode Rewards", save_path: Optional[str] = None) -> None:
    """
    Visualize rewards over episodes.
    
    Args:
        rewards: List of episode rewards
        title: Plot title
        save_path: Path to save the figure (if None, will display instead)
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(rewards) + 1), rewards, marker='o')
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title(title)
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path)
        print(f"Figure saved to {save_path}")
    else:
        plt.show()
