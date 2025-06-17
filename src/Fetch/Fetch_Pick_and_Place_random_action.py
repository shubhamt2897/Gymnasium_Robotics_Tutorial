import gymnasium as gym
import gymnasium_robotics

# The registration happens automatically when gymnasium_robotics is imported
# so gym.register_envs() is often not needed.

env = gym.make("FetchPickAndPlace-v3", render_mode="human" )   
# This returns the initial observation and optional info.
print("Resetting environment...")
observation, info = env.reset()
print("Initial Observation:", observation)

# 3. Run the simulation loop
print("\nStarting simulation with random actions...")
for step in range(500):
    # 4. Get a random action
    # The action space provides a sample() method for this.
    action = env.action_space.sample()

    # 5. Step the environment
    # This executes the action and returns feedback from the environment.
    observation, reward, terminated, truncated, info = env.step(action)
# Check if the episode is over
    if terminated or truncated:
        print("Terminated:", terminated, "Truncated:", truncated )
        print("Episode finished. Resetting environment.")
        observation, info = env.reset()

# 6. Close the environment
# This is important for cleanup.
print("\nSimulation finished. Closing environment.")
env.close()
