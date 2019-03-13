# Training Process
### Reinforcement Learning<br>
Using Proximal Policy Optimzation (PPO)
* Locates ```learn_rl.py```
* Modify the parameters [(more info)](Setup-Configuration-Files.md#python-script)
* Run ```learn_rl.py```

### General Machine Learning
* Locates ```learn_ml.py```
* Modify the parameters [(more info)](Setup-Configuration-Files.md#python-script)
* Implement your own decision algorithm in ```def decide(brain_info: BrainInfo) function```
* Run ```learn_ml.py```

### OpenAI Gym Compitable
* Sample Code: ```learn_gym.py```
```
from gym_unity.envs import UnityEnv

env = UnityEnv(environment_filename, worker_id=0, use_visual, multiagent, env_config,camera_res_overwrite)
```
* Limitation: 
By default the first visual observation is provided as the observation, if present. Otherwise vector observations are provided.<br>
All BrainInfo output from the environment can still be accessed from the info provided by ```env.step(action)```


### Inference
* Set ```load_model = True``` Load the pre-train model
* Set ```train_model = False``` Don't run any learning algorithm
* Set ```fast_simulation = False``` Enable inference mode, allow you to use WASD-controled Observe Camera
* Run ```learn_rl.py```

### Runing the Pre-train model
* [Details about Pre-train model](Pretrain-Model-Details.md)
