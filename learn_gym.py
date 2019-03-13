import json
from gym_unity.envs import UnityEnv

def extract_camera_config_gym(config_file):

	config = []
	use_visual = True
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

	if len(config) == 0:
		use_visual = False

	if len(config) > 1:
		config = config[0:1]

	return config, use_visual

def check_config_validity_gym(config):

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

	if (config['camera1_type'] != 0) + (config['camera2_type'] != 0) + (config['camera3_type'] != 0) > 1:
		raise ValueError('Gym only support 1 visual observation')

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

	check_config_validity_gym(config)

	return config

def main():

	env_path = 'AutoBenchExecutable/AutoBenchExecutable'
	curriculum_file = 'config/curricula/autobench/AutoBenchBrain.json'
	camera_res_overwrite, use_visual = extract_camera_config_gym(curriculum_file)
	# Setup the Unity Environment
	env = UnityEnv(environment_filename=env_path, worker_id=0, use_visual=use_visual,
				   multiagent=True, env_config=get_env_config(curriculum_file),
				   camera_res_overwrite=camera_res_overwrite)

if __name__ == '__main__':
	main()