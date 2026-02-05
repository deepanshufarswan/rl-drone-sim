import gym
import numpy as np
from gym import spaces
import subprocess
import time

class DroneEnv(gym.Env):
    """
    RL Environment Skeleton for Autonomous Drone Navigation
    (Gazebo-based, PX4-ready, GUI-expandable)
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super(DroneEnv, self).__init__()

        # ----------------------------
        # ACTION SPACE
        # ----------------------------
        # vx, vy, vz, yaw_rate
        self.action_space = spaces.Box(
            low=np.array([-1.0, -1.0, -1.0, -1.0]),
            high=np.array([1.0, 1.0, 1.0, 1.0]),
            dtype=np.float32
        )

        # ----------------------------
        # OBSERVATION SPACE
        # ----------------------------
        # [x, y, z, vx, vy, vz, goal_dx, goal_dy, goal_dz]
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(9,),
            dtype=np.float32
        )

        # ----------------------------
        # ENV STATE
        # ----------------------------
        self.drone_pos = np.zeros(3)
        self.drone_vel = np.zeros(3)
        self.goal_pos = np.array([5.0, 0.0, 1.0])

        self.max_steps = 500
        self.current_step = 0

        print("[RL ENV] DroneEnv initialized")

    # ----------------------------
    # RESET
    # ----------------------------
    def reset(self):
        print("[RL ENV] Resetting environment")

        self.current_step = 0

        # Reset drone state (placeholder)
        self.drone_pos = np.array([0.0, 0.0, 1.0])
        self.drone_vel = np.zeros(3)

        obs = self._get_obs()
        return obs

    # ----------------------------
    # STEP
    # ----------------------------
    def step(self, action):
        self.current_step += 1

        # Apply action (placeholder physics)
        self.drone_vel = action[:3]
        self.drone_pos += self.drone_vel * 0.1

        obs = self._get_obs()
        reward = self._compute_reward()
        done = self._check_done()

        info = {
            "distance_to_goal": np.linalg.norm(self.goal_pos - self.drone_pos)
        }

        return obs, reward, done, info

    # ----------------------------
    # OBSERVATION
    # ----------------------------
    def _get_obs(self):
        goal_delta = self.goal_pos - self.drone_pos
        obs = np.concatenate([
            self.drone_pos,
            self.drone_vel,
            goal_delta
        ])
        return obs.astype(np.float32)

    # ----------------------------
    # REWARD FUNCTION
    # ----------------------------
    def _compute_reward(self):
        distance = np.linalg.norm(self.goal_pos - self.drone_pos)

        reward = -distance

        if distance < 0.3:
            reward += 100.0

        return reward

    # ----------------------------
    # TERMINATION
    # ----------------------------
    def _check_done(self):
        if self.current_step >= self.max_steps:
            return True

        if np.linalg.norm(self.goal_pos - self.drone_pos) < 0.3:
            print("[RL ENV] Goal reached!")
            return True

        return False

    # ----------------------------
    # RENDER (OPTIONAL)
    # ----------------------------
    def render(self, mode="human"):
        pass

    def close(self):
        pass
