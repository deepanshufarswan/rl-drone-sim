import numpy as np
from env.drone_env import DroneEnv

def run_demo():
    env = DroneEnv()
    obs = env.reset()

    print("\n--- DEMO EPISODE START ---")

    total_reward = 0.0

    for step in range(10):
        goal_delta = obs[6:9]
        avoidance = np.zeros(3)

        # DEMO obstacle trigger (mid-trajectory)
        if 3.0 < np.linalg.norm(goal_delta) < 4.5:
            avoidance[1] = 0.8
            print("  [AVOIDANCE] Obstacle detected → sidestepping")

        action = np.clip(goal_delta + avoidance, -1.0, 1.0)

        obs, reward, done, info = env.step(action)
        total_reward += reward

        print(
        f"Step {step:02d} | "
        f"Distance: {info['distance_to_goal']:.2f} | "
        f"Reward: {reward:.2f}"
        )

        if done:
            print("Episode finished early")
            break


    print("--- DEMO EPISODE END ---")
    print(f"Total reward: {total_reward:.2f}")

if __name__ == "__main__":
    run_demo()
