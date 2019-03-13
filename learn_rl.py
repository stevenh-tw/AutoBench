import json
from trainer_controller import TrainerController


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

def get_env_config(curriculum_file):

	try:
		with open(curriculum_file) as data_file:
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

def main():
	try:
		print('''

						▄▄▄▓▓▓▓
				   ╓▓▓▓▓▓▓█▓▓▓▓▓
			  ,▄▄▄m▀▀▀'  ,▓▓▓▀▓▓▄                           ▓▓▓  ▓▓▌
			▄▓▓▓▀'      ▄▓▓▀  ▓▓▓      ▄▄     ▄▄ ,▄▄ ▄▄▄▄   ,▄▄ ▄▓▓▌▄ ▄▄▄    ,▄▄
		  ▄▓▓▓▀        ▄▓▓▀   ▐▓▓▌     ▓▓▌   ▐▓▓ ▐▓▓▓▀▀▀▓▓▌ ▓▓▓ ▀▓▓▌▀ ^▓▓▌  ╒▓▓▌
		▄▓▓▓▓▓▄▄▄▄▄▄▄▄▓▓▓      ▓▀      ▓▓▌   ▐▓▓ ▐▓▓    ▓▓▓ ▓▓▓  ▓▓▌   ▐▓▓▄ ▓▓▌
		▀▓▓▓▓▀▀▀▀▀▀▀▀▀▀▓▓▄     ▓▓      ▓▓▌   ▐▓▓ ▐▓▓    ▓▓▓ ▓▓▓  ▓▓▌    ▐▓▓▐▓▓
		  ^█▓▓▓        ▀▓▓▄   ▐▓▓▌     ▓▓▓▓▄▓▓▓▓ ▐▓▓    ▓▓▓ ▓▓▓  ▓▓▓▄    ▓▓▓▓`
			'▀▓▓▓▄      ^▓▓▓  ▓▓▓       └▀▀▀▀ ▀▀ ^▀▀    `▀▀ `▀▀   '▀▀    ▐▓▓▌
			   ▀▀▀▀▓▄▄▄   ▓▓▓▓▓▓,                                      ▓▓▓▓▀
				   `▀█▓▓▓▓▓▓▓▓▓▌
						¬`▀▀▀█▓

		''')
	except:
		print('\n\n\tUnity Technologies\n')

	# Docker Parameters
	docker_target_name = None

	# General parameters
	env_path = 'AutoBenchExecutable/AutoBenchExecutable'
	#env_path = None
	run_id = '1'
	load_model = True
	train_model = True
	save_freq = 10000
	keep_checkpoints = 10000
	worker_id = 0
	run_seed = 0
	curriculum_folder = 'config/curricula/autobench/'
	curriculum_file = 'config/curricula/autobench/AutoBenchBrain.json'
	lesson = 0
	fast_simulation = True
	no_graphics = False
	trainer_config_path = 'config/trainer_config.yaml'
	camera_res_overwrite = extract_camera_config(curriculum_file)
	benchmark = False
	benchmark_episode = 100
	benchmark_verbose = True
	env_config = get_env_config(curriculum_file)

	# Create controller and launch environment.
	tc = TrainerController(env_path, run_id,
						   save_freq, curriculum_folder, fast_simulation,
						   load_model, train_model, worker_id,
						   keep_checkpoints, lesson, run_seed,
						   docker_target_name, trainer_config_path, no_graphics,
						   camera_res_overwrite, benchmark, benchmark_episode,
						   env_config['goal_reward'] + env_config['time_penalty'], benchmark_verbose)

	# Begin training
	tc.start_learning()

if __name__ == '__main__':
	main()
