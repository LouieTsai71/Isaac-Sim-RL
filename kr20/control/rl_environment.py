# rl_environment.py
import isaacsim
import gym
from gym import spaces
import numpy as np
from pxr import UsdPhysics
import omni.usd
from .common import set_drive_parameters

class RobotEnv(gym.Env):
    def __init__(self):
        super(RobotEnv, self).__init__()
        
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(6,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32)

        self.stage = omni.usd.get_context().get_stage()

    def step(self, action):
        self._apply_action(action)
        self._timeline.play()
        state = self._get_state()
        reward = self._compute_reward(state)
        done = self._check_done(state)
        info = {}
        return state, reward, done, info

    def reset(self):
        state = self._reset_simulation()
        return state

    def render(self, mode='human'):
        pass

    def _apply_action(self, action):
        for i, act in enumerate(action):
            joint_name = f"/Root/KR20/Robot/A{i+1}/node_/mesh_/R{i+1}"
            joint = UsdPhysics.DriveAPI.Get(self.stage.GetPrimAtPath(joint_name), "angular")
            set_drive_parameters(joint, "position", act)

    def _get_state(self):
        state = []
        for i in range(6):
            joint_name = f"/Root/KR20/Robot/A{i+1}/node_/mesh_/R{i+1}"
            joint = UsdPhysics.DriveAPI.Get(self.stage.GetPrimAtPath(joint_name), "angular")
            position = joint.GetTargetPositionAttr().Get()
            velocity = joint.GetTargetVelocityAttr().Get()
            state.extend([position, velocity])
        return np.array(state, dtype=np.float32)

    def _compute_reward(self, state):
        reward = -np.sum(np.square(state[:6]))
        return reward

    def _check_done(self, state):
        return False

    def _reset_simulation(self):
        for i in range(6):
            joint_name = f"/Root/KR20/Robot/A{i+1}/node_/mesh_/R{i+1}"
            joint = UsdPhysics.DriveAPI.Get(self.stage.GetPrimAtPath(joint_name), "angular")
            set_drive_parameters(joint, "position", 0.0)
        return self._get_state()
