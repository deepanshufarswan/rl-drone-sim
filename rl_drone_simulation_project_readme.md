# RL Drone Simulation Project

## 1. Project Overview
This project implements a **reinforcement-learning–ready autonomous drone path planning using Reinforcement learning framework** using **Gazebo** for simulation and a **Gym-compatible Python environment** for control, evaluation, and future learning.

The system is designed in **two layers**:
1. **Simulation layer (Gazebo)** – visual world, drone model, obstacles
2. **Decision layer (Python RL env)** – state, action, reward, termination logic

The current implementation demonstrates **goal-directed navigation with obstacle avoidance**, suitable for live demos and extendable to full RL training (PPO/SAC) during final evaluation.

---

## 2. Repository Structure
```
rl_drone_sim/
│
├── worlds/
│   └── rl_test.world            # Gazebo world (ground, obstacles, start, goal)
│
├── models/
│   └── simple_quad/             # Drone model (sphere-based abstraction)
│
├── plugins/
│   ├── simple_controller.cc     # Gazebo plugin (baseline motion logic)
│   ├── CMakeLists.txt
│   └── build/
│
├── rl/
│   ├── env/
│   │   └── drone_env.py         # Gym-compatible RL environment
│   └── run_demo_episode.py      # Deterministic demo + evaluation script
│
└── README.md (this file)
```

---

## 3. Software Stack

### 3.1 Core Tools
- **Ubuntu 22.04 (Jammy)**
- **Gazebo Classic** – physics-based simulation
- **Python 3.10** – RL logic
- **NumPy** – vector math
- **OpenAI Gym (0.26.x)** – environment abstraction
- **Git + GitHub** – version control and milestones

### 3.2 Why This Stack
- Gazebo provides **realistic physics + visuals**
- Gym enforces **standard RL interfaces** (reset, step, reward)
- Python allows rapid iteration and future integration with RL libraries

---

## 4. Gazebo Simulation Layer

### 4.1 World File (`rl_test.world`)
Defines:
- Ground plane
- Lighting
- Static obstacles (boxes/cylinders)
- Start region
- Goal marker

Purpose:
> To visually validate navigation, obstacle placement, and scalability to larger environments.

### 4.2 Drone Model (`models/simple_quad`)
- Simplified spherical drone
- Collision geometry enabled
- Minimal mass and inertia

Reason:
> Reduces complexity while validating navigation and RL logic.

### 4.3 Gazebo Plugin (`simple_controller.cc`)
Role:
- Demonstrates deterministic baseline control
- Proves Gazebo ↔ controller integration

Used as:
> A sanity-check baseline before RL replaces control logic.

---

## 5. Reinforcement Learning Layer

### 5.1 Environment (`drone_env.py`)
Implements `gym.Env`:

#### Action Space
```
Box(-1, 1, shape=(4,))
```
- Velocity commands (x, y, z)
- Reserved channel for future yaw/thrust

#### Observation Space (9D)
```
[drone_position(3), drone_velocity(3), goal_delta(3)]
```

#### Internal State
- Drone position & velocity
- Goal position
- Logical obstacle list

---

### 5.2 Reward Function
```python
reward = -distance_to_goal

if collision:
    reward -= 50

if goal_reached:
    reward += 100
```

Why:
- Encourages smooth goal convergence
- Strongly penalizes unsafe behavior
- Clear terminal signals for RL

---

### 5.3 Episode Termination
Episode ends when:
- Goal is reached
- Collision occurs
- Max steps exceeded

This ensures:
> Stable RL training and interpretable evaluation.

---

## 6. Demo & Evaluation Script

### `run_demo_episode.py`
Purpose:
- Deterministic navigation demo
- Obstacle avoidance without learning
- Generates interpretable logs

Key Features:
- Real obstacle repulsion logic
- Step-by-step distance reporting
- Episode summary (success/collision/timeout)

Used in:
> Mid-term demo and final evaluation walkthrough.

---

## 7. System Architecture (Conceptual)

```
+---------------------+
|   Gazebo Simulator  |
|                     |
|  World + Obstacles  |
|        + Drone      |
+----------+----------+
           |
           | (state abstraction)
           v
+---------------------+
|   DroneEnv (Gym)    |
|  - Observation      |
|  - Reward           |
|  - Termination      |
+----------+----------+
           |
           | (action)
           v
+---------------------+
| Controller / RL     |
|  - Demo Heuristic   |
|  - (Future PPO)     |
+---------------------+
```

---

## 8. Current Project Status

### ✅ Completed (~85–90%)
- Custom Gazebo world
- Drone model + collisions
- Gym-compatible RL environment
- Obstacle-aware navigation
- Deterministic demo episode
- Version-controlled milestones

### 🔜 Planned (Final Evaluation)
- Larger dynamic world
- GUI-based control (Qt / RViz / Web)
- PX4 + ROS2 bridge
- PPO / SAC policy training

---

## 9. Key Design Decisions (Viva-Ready)

- **Separated simulation from learning** → modularity
- **Logical obstacles in RL env** → faster prototyping
- **Deterministic demo first** → reduces risk
- **Reward shaping** → stable learning later

---

## 10. How to Run

```bash
cd ~/rl_drone_sim

gazebo worlds/rl_test.world

cd rl
python3 run_demo_episode.py
```

---

## 11. Conclusion
This project provides a **robust foundation for autonomous drone navigation using reinforcement learning**, with a working demo, clear architecture, and a direct path to full PX4-based control.

The current implementation prioritizes **clarity, correctness, and evaluability**, making it suitable for academic assessment and future extension.

