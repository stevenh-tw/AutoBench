# # Unity ML-Agents Toolkit
# ## ML-Agent Learning

import logging

import os
from docopt import docopt

from unitytrainers.trainer_controller import TrainerController

if __name__ == '__main__':
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

	##### Parameters
	logger = logging.getLogger("unityagents")
	docker_target_name = ''
	run_id = 'SCurveBackward1-3-mlv0.4' # folder name that write model checkpoint and summary
	seed = 0 # setup whatever random seed you like
	load_model = True # if load pre-train model
	train_model = True # if train the model
	save_freq = 30000 # model saving frequency
	env_path = None # leave it None
	keep_checkpoints = 10000 # maximum model checkpoint allowed
	worker_id = 0 # leave it 0
	curriculum_file = None
	lesson = 1

	# if true, training mode, 100x time scale, small window
	# if false, inference mode, 1x time scale, big window, with observe camera
	fast_simulation = False
	no_graphics = False # True if you want Unity Environment to train in background

	# Constants
	# Assumption that this yaml is present in same dir as this file
	base_path = os.path.dirname(__file__)
	TRAINER_CONFIG_PATH = os.path.abspath(os.path.join(base_path, "trainer_config.yaml"))

	tc = TrainerController(env_path, run_id, save_freq, curriculum_file, fast_simulation, load_model, train_model,
						   worker_id, keep_checkpoints, lesson, seed, docker_target_name, TRAINER_CONFIG_PATH,
						   no_graphics)
	##### Actually start the training process
	tc.start_learning()