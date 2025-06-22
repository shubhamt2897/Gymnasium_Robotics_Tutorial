# Fetch Slide Environment Hyperparameter Tuning with SAC using Optuna
import gymnasium as gym
import gymnasium_robotics
from stable_baselines3 import SAC, HerReplayBuffer
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
import optuna
import torch as th
import numpy as np

# --- Configuration ---
ENV_ID = "FetchSlide-v3"
# Number of Optuna trials to run
N_TRIALS = 30
# Training timesteps for EACH trial
N_TIMESTEPS = 25000
# Number of episodes to evaluate EACH trained model
N_EVAL_EPISODES = 20

# --- The Objective Function for Optuna ---
def objective(trial: optuna.Trial) -> float:
    """
    This function is called by Optuna for each trial.
    It trains and evaluates an SAC model with a given set of hyperparameters.
    """
    print(f"\n--- Starting Trial #{trial.number} ---")

    # 1. Suggest Hyperparameters for this trial
    learning_rate = trial.suggest_float("learning_rate", 1e-5, 1e-3, log=True)
    
    # Suggest a network architecture
    net_arch_str = trial.suggest_categorical("net_arch", ["small", "medium", "big"])
    net_arch = {
        "small": [64, 64],
        "medium": [128, 128],
        "big": [256, 256],
    }[net_arch_str]

    policy_kwargs = dict(net_arch=net_arch)

    # 2. Create and Train the SAC model
    # We create a new environment for each trial
    train_env = gym.make(ENV_ID)
    
    # Use the same HER Buffer configuration as before
    replay_buffer_class = HerReplayBuffer
    replay_buffer_kwargs = dict(
        n_sampled_goal=4,
        goal_selection_strategy="future",
    )

    model = SAC(
        "MultiInputPolicy",
        train_env,
        learning_rate=learning_rate,
        policy_kwargs=policy_kwargs,
        replay_buffer_class=replay_buffer_class,
        replay_buffer_kwargs=replay_buffer_kwargs,
        verbose=0,  # Set to 0 to keep the output clean
        device="cuda" # Ensure GPU is used
    )

    # Train the model
    model.learn(total_timesteps=N_TIMESTEPS)

    # 3. Evaluate the Trained Model
    eval_env = gym.make(ENV_ID)
    successful_episodes = 0
    for _ in range(N_EVAL_EPISODES):
        obs, info = eval_env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = eval_env.step(action)
            done = terminated or truncated
            if done and info.get('is_success'):
                successful_episodes += 1
    
    eval_env.close()

    success_rate = successful_episodes / N_EVAL_EPISODES
    print(f"Trial #{trial.number} Finished. Success Rate: {success_rate:.2f}")

    # 4. Return the performance score
    return success_rate

# --- Main Execution Block ---
if __name__ == "__main__":
    # Create an Optuna study. 'direction="maximize"' means we want to find the highest success rate.
    study = optuna.create_study(direction="maximize")
    
    # Start the optimization process
    study.optimize(objective, n_trials=N_TRIALS, timeout=3600) # Run for N_TRIALS or 1 hour

    # Print the results
    print("\n--- Hyperparameter Tuning Complete ---")
    print(f"Number of finished trials: {len(study.trials)}")
    print("Best trial:")
    best_trial = study.best_trial
    print(f"  Value (Success Rate): {best_trial.value:.4f}")
    print("  Params: ")
    for key, value in best_trial.params.items():
        print(f"    {key}: {value}")