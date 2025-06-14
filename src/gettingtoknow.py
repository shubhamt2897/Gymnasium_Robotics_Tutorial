import gymnasium as gym
import gymnasium_robotics

# The registration happens automatically when gymnasium_robotics is imported
# so gym.register_envs() is often not needed.

env = gym.make("FetchReach-v3")

# In recent Gymnasium versions, reset() returns two values: observation and info
observation, info = env.reset()

# Take a random step
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())

# --- FIX is here: Use env.unwrapped to access the base environment's methods ---

# The following always has to hold:
assert reward == env.unwrapped.compute_reward(obs["achieved_goal"], obs["desired_goal"], info)
assert truncated == env.unwrapped.compute_truncated(obs["achieved_goal"], obs["desired_goal"], info)
assert terminated == env.unwrapped.compute_terminated(obs["achieved_goal"], obs["desired_goal"], info)

# However goals can also be substituted:
substitute_goal = obs["achieved_goal"].copy()
substitute_reward = env.unwrapped.compute_reward(obs["achieved_goal"], substitute_goal, info)
substitute_terminated = env.unwrapped.compute_terminated(obs["achieved_goal"], substitute_goal, info)
substitute_truncated = env.unwrapped.compute_truncated(obs["achieved_goal"], substitute_goal, info)

print("Script finished successfully, all assertions passed!")