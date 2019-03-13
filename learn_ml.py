import json
import time
import numpy as np
from mlagents.envs.environment import UnityEnvironment
from mlagents.envs.brain import BrainInfo
from mlagents.trainers.benchmark import BenchmarkManager


def extract_camera_config(config_file):

	config = []
	with open(config_file, 'r') as data_file:
		data = json.load(data_file)
		params = data['parameters']
		if params['camera1_type'][0] != 0:
			config += [{
				"height": params['camera1_res_y'][0],
				"width": params['camera1_res_x'][0],
				"blackAndWhite": False
			}]
		if params['camera2_type'][0] != 0:
			config += [{
				"height": params['camera2_res_y'][0],
				"width": params['camera2_res_x'][0],
				"blackAndWhite": False
			}]
		if params['camera3_type'][0] != 0:
			config += [{
				"height": params['camera3_res_y'][0],
				"width": params['camera3_res_x'][0],
				"blackAndWhite": False
			}]

	return config

def get_env_config(curriculum_folder):

	try:
		with open(curriculum_folder) as data_file:
			data = json.load(data_file)
	except IOError:
		raise IOError()

	config = {}
	parameters = data['parameters']
	for key in parameters:
		config[key] = parameters[key][0]

	check_config_validity(config)

	return config

def check_config_validity(config):

	if config['camera1_type'] < 0 or config['camera1_type'] > 6:
		raise ValueError('camera1_type')
	if config['camera2_type'] < 0 or config['camera2_type'] > 6:
		raise ValueError('camera2_type')
	if config['camera3_type'] < 0 or config['camera3_type'] > 6:
		raise ValueError('camera3_type')

	if config['camera1_type'] != 0 and (config['camera1_res_x'] == 0 or config['camera1_res_y'] == 0):
		raise ValueError('camera1_res')
	if config['camera2_type'] != 0 and (config['camera2_res_x'] == 0 or config['camera2_res_y'] == 0):
		raise ValueError('camera2_res')
	if config['camera3_type'] != 0 and (config['camera3_res_x'] == 0 or config['camera3_res_y'] == 0):
		raise ValueError('camera3_res')

	if config['weather_id'] < 0 or config['weather_id'] > 10:
		raise ValueError('weather_id')
	if config['time_id'] < 0 or config['time_id'] >= 24:
		raise ValueError('time_id')
	if config['road_width'] <= 0:
		raise ValueError('road_width')

# Reference to brain.py, BrainInfo, for the commented data structure details
def decide(brain_info: BrainInfo):

		# Given the brain_info, decide which action for each agent,

		##################################
		#        Action Index
		#
		#          +1   0 -0.3  throttle power
		# -30       0   1   2
		# 0         3   4   5
		# +30       6   7   8
		# steering
		# angle
		#
		##################################

		# Sample placeholder, type = ndarray, shape = (agent_amount, 1)
		sample_action = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 0]).transpose()

		# sample_action = np.array([5]).transpose()
		# TODO Design your own decide algorithm here

		return sample_action

def main():

	env_path = 'AutoBenchExecutable/AutoBenchExecutable'
	# env_path = None
	curriculum_file = 'config/curricula/autobench/AutoBenchBrain.json'
	no_graphics = False  # True if you want Unity Environment to train in background
	max_step = 1e10  # total training step

	# Set True: 100x time scale, small window, 10 agents
	# Set False: 1x time scale, big window, 1 agents with observation camera
	fast_simulation = False
	benchmark = False
	benchmark_episode = 1000


	# Setup the Unity Environment
	env_config = get_env_config(curriculum_file)
	env = UnityEnvironment(file_name=env_path,
	                       no_graphics=no_graphics,
	                       camera_res_overwrite=extract_camera_config(curriculum_file))
	brain_name = env.brain_names[0]  # Get brain_name, assume only have 1 brain

	curr_info = env.reset(config=env_config,train_mode=fast_simulation)[brain_name]
	agent_size = len(curr_info.agents)

	BenchmarkManager(agent_amount=agent_size, benchmark_episode=benchmark_episode,
	                 success_threshold=env_config['goal_reward']+env_config['time_penalty'],
	                 verbose=False)

	last_update_time = time.clock()

	### Standard RL training loop
	for global_step in range(int(max_step)):

		# Implement your own decide algorithm
		action = decide(curr_info)

		# Send Action into Unity Environment and return new_info, type = BrainInfo
		# You can refer to brain.py, I've commented the detail data structure
		new_info = env.step(vector_action={brain_name: action},
		                    memory={brain_name: None},
							text_action={brain_name: None})[brain_name]
		if benchmark:
			BenchmarkManager.add_result(new_info)
			if BenchmarkManager.is_complete():
				BenchmarkManager.analyze()
				break

		# Calculate and Print training speed
		if global_step % 100 == 0:
			print("Steps:{:,}".format(global_step), " ||  Speed:",
				  format(100 / (time.clock() - last_update_time), ".2f"))
			last_update_time = time.clock()

		# Assign new_info to curr_info for next timestep training
		curr_info = new_info

	env.close()


if __name__ == '__main__':
	main()