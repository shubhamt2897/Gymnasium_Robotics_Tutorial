# MuJoCo Environment Guide

This document provides information on the available MuJoCo environments in Gymnasium and how to use them.

## Available Environments

Gymnasium provides several MuJoCo-based environments:

### Basic Environments

- **Ant-v4**: A 3D quadruped with the goal of moving forward as fast as possible.
- **HalfCheetah-v4**: A 2D cheetah-like robot that needs to move forward as fast as possible.
- **Hopper-v4**: A 2D one-legged robot that needs to hop forward as fast as possible.
- **Humanoid-v4**: A 3D humanoid robot that needs to move forward as fast as possible without falling over.
- **HumanoidStandup-v4**: A 3D humanoid robot that starts lying on the ground and needs to stand up.
- **Pusher-v4**: A robot arm that needs to push an object to a target location.
- **Reacher-v4**: A 2D robot arm that needs to reach a target location.
- **Swimmer-v4**: A 2D snake-like robot that needs to swim forward as fast as possible.
- **Walker2d-v4**: A 2D bipedal robot that needs to walk forward as fast as possible.

### Advanced Environments (via gymnasium-robotics)

- **Fetch** series: Robot arm manipulation tasks
- **Shadow Hand** series: Dexterous manipulation with a realistic hand model
- **Adroit** series: Advanced dexterous manipulation tasks

## Using Environments

### Basic Usage

```python
import gymnasium as gym

# Create an environment
env = gym.make("Humanoid-v4", render_mode="human")

# Reset the environment
observation, info = env.reset()

# Run simulation
for _ in range(1000):
    # Sample a random action
    action = env.action_space.sample()
    
    # Execute the action
    observation, reward, terminated, truncated, info = env.step(action)
    
    # Render the environment
    env.render()
    
    # Check if episode is done
    if terminated or truncated:
        observation, info = env.reset()

# Close the environment
env.close()
```

### Observation and Action Spaces

Each environment has specific observation and action spaces:

```python
import gymnasium as gym

env = gym.make("Humanoid-v4")

print(f"Observation space: {env.observation_space}")
print(f"Shape: {env.observation_space.shape}")
print(f"Action space: {env.action_space}")
print(f"Shape: {env.action_space.shape}")
```

### Rendering Options

MuJoCo environments support multiple rendering modes:

```python
# Human rendering (displays a window)
env = gym.make("Humanoid-v4", render_mode="human")

# RGB array rendering (returns a numpy array of pixels)
env = gym.make("Humanoid-v4", render_mode="rgb_array")

# Depth array rendering (returns a depth map)
env = gym.make("Humanoid-v4", render_mode="depth_array")
```

## Customizing Environments

You can customize environments by extending the base classes:

```python
from gymnasium.envs.mujoco.humanoid_v4 import HumanoidEnv

class MyCustomHumanoid(HumanoidEnv):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def step(self, action):
        observation, reward, terminated, truncated, info = super().step(action)
        
        # Add custom reward logic
        custom_reward = ...
        
        return observation, custom_reward, terminated, truncated, info
```

See the examples in the `examples/` directory for more detailed customization examples.
