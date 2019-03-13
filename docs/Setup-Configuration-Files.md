# Setup Configuration Files

### Training Config
Located in config/trainer_config.yaml<br>
This is the configuration about Reinforcement Learning PPO trainer
```
AutoBenchBrain:
    batch_size: 1024
    beta: 1.0e-1
    buffer_size: 1024
    epsilon: 0.2
    gamma: 0.99
    hidden_units: 128
    lambd: 0.95
    learning_rate: 3.0e-4
    max_steps: 1.0e7
    memory_size: 256
    normalize: true
    num_epoch: 5
    num_layers: 2
    time_horizon: 512
    sequence_length: 64
    summary_freq: 3000   
    use_recurrent: true
```
### Environment Config
Located in config/curricula/autobench/AutoBenchBrain.json
This is about the configuration of Unity environment
```
{
  "measure": "progress",        #Ignore
  "thresholds": [],             #Ignore
  "min_lesson_length": 0,       #Ignore
  "signal_smoothing": false,    #Ignore
  "parameters": {
    "camera1_type": [0],
    "camera2_type": [3],
    "camera3_type": [0],
    "camera1_res_x": [0],
    "camera2_res_x": [50],
    "camera3_res_x": [0],
    "camera1_res_y": [0],
    "camera2_res_y": [50],
    "camera3_res_y": [0],
    "weather_id": [1],
    "time_id": [9],
    "road_width": [7],
    "forward": [true],
    "detail": [false],
    "goal_reward": [500],
    "time_penalty": [-1],
    "collision_penalty": [-300],
    "position_reward": [300],
    "velocity_reward": [1]
  }
}
```
Only need to focus on ```parameters``` section

### Python Script
Located in learn_rl.py, learn_ml.py, learn_gym.py<br>
The following uses learn_rl.py as an example
```
env_path = 'AutoBenchExecutable/AutoBenchExecutable' #Default executable path
run_id = '1'
load_model = False
train_model = True
save_freq = 10000
keep_checkpoints = 1000
worker_id = 0
run_seed = 0
curriculum_folder = 'config/curricula/autobench/'
curriculum_file = 'config/curricula/autobench/AutoBenchBrain.json'
lesson = 0
fast_simulation = True
no_graphics = False
trainer_config_path = 'config/trainer_config.yaml'
benchmark = False
benchmark_episode = 100
benchmark_verbose = True
```
#### Env_path
Path of the Unity executable
#### Run_id
Identifier for each run, suitable for fine-tunning parameters
#### Load_model
Whether load the tensorflow model
#### Train_model
Whether train the tensorflow model
#### Save_freq
Frequency of the tensorflow model saved
#### Keep_checkpoints
Maximum checkpoint allow for saving
#### Worker_id
Ignore and set to 0
#### Run_seed
Random seed of the Unity executable
#### Curriculum_folder
Folder of environment config file
#### Curriculum_file
Location of environment config file
#### Lesson
Ignore and set to 0
#### Fast_simulation
If set to True, small window, 100X time scale, 10 agents<br>
If set to False, large window, 1X time scale, 1 agent and WASD-controled Observe Camera
#### No_graphic
Whether not showing the windows of Unity environment
#### Trainer_config_path
Location of trainer config file
#### Benchmark
Whether benchmark the current model
#### Benchmark_episode
Number of episode needed for benchmarking
#### Benchmark_verbose
Whether or not print out episode information if episode ends
