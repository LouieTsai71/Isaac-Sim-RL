# train.py
import isaacsim
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from rl_environment import RobotEnv
import omni.ui as ui
from omni.isaac.ui.element_wrappers import FloatField

def make_env():
    def _init():
        return RobotEnv()
    return _init

def main():
    num_envs = 4
    envs = SubprocVecEnv([make_env() for _ in range(num_envs)])

    model = PPO("MlpPolicy", envs, verbose=1)

    for i in range(10):
        model.learn(total_timesteps=1000)
        reward = model.episode_reward
        episode = i
        update_ui(reward, episode)

    model.save("robot_ppo")

    env = RobotEnv()
    obs = env.reset()
    for _ in range(1000):
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        if done:
            obs = env.reset()

def update_ui(reward, episode):
    window = ui.Window("Training Info", width=300, height=200)
    with window.frame:
        with ui.VStack():
            ui.Label(f"Reward: {reward}")
            ui.Label(f"Episode: {episode}")

if __name__ == "__main__":
    main()
