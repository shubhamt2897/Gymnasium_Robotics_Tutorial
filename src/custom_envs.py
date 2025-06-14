"""
Custom MuJoCo environments for reinforcement learning research.
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.mujoco.humanoid_v4 import HumanoidEnv
from gymnasium.envs.mujoco.ant_v4 import AntEnv

class TimeLimitWrapper(gym.Wrapper):
    """
    A wrapper that limits the duration of episodes.
    """
    def __init__(self, env, max_steps=1000):
        super().__init__(env)
        self.max_steps = max_steps
        self.steps = 0
        
    def reset(self, **kwargs):
        self.steps = 0
        return super().reset(**kwargs)
        
    def step(self, action):
        observation, reward, terminated, truncated, info = super().step(action)
        self.steps += 1
        
        if self.steps >= self.max_steps:
            truncated = True
            
        return observation, reward, terminated, truncated, info

class RewardScalingWrapper(gym.Wrapper):
    """
    A wrapper that scales the reward by a constant factor.
    """
    def __init__(self, env, scale=1.0):
        super().__init__(env)
        self.scale = scale
        
    def step(self, action):
        observation, reward, terminated, truncated, info = super().step(action)
        scaled_reward = reward * self.scale
        return observation, scaled_reward, terminated, truncated, info

class EnhancedHumanoidEnv(HumanoidEnv):
    """
    Enhanced Humanoid environment with additional rewards for specific behaviors.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def step(self, action):
        observation, reward, terminated, truncated, info = super().step(action)
        
        # Extract relevant state information
        qpos = self.data.qpos.flat.copy()
        qvel = self.data.qvel.flat.copy()
        
        # Additional reward components
        height = qpos[2]  # z-position (height)
        upright_reward = 0.1 * height  # Reward for being upright
        
        # Penalize excessive movement for stability
        action_penalty = 0.01 * np.square(action).sum()
        
        # Combine rewards
        modified_reward = reward + upright_reward - action_penalty
        
        # Add reward components to info
        info['reward_upright'] = upright_reward
        info['reward_action_penalty'] = -action_penalty
        info['reward_original'] = reward
        
        return observation, modified_reward, terminated, truncated, info

class EnhancedAntEnv(AntEnv):
    """
    Enhanced Ant environment with additional rewards for energy efficiency.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def step(self, action):
        observation, reward, terminated, truncated, info = super().step(action)
        
        # Extract relevant state information
        xpos = self.get_body_com("torso")[0]  # x-position
        
        # Additional reward for forward progress
        forward_reward = 0.1 * xpos
        
        # Energy efficiency reward - penalize large actions
        energy_penalty = 0.01 * np.square(action).sum()
        
        # Combine rewards
        modified_reward = reward + forward_reward - energy_penalty
        
        # Add reward components to info
        info['reward_forward'] = forward_reward
        info['reward_energy'] = -energy_penalty
        info['reward_original'] = reward
        
        return observation, modified_reward, terminated, truncated, info
