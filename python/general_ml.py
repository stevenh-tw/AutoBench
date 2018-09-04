import time
import numpy as np

from unityagents import UnityEnvironment, BrainInfo

#########################
#
# This is the sample code for AutoBench General ML method
# Please implement decide(brain_info: BrainInfo) function
# run_general_ml() is the main training loop
#
#########################


# You can refer to brain.py for BrainInfo, I've commented the detail data structure
def decide(brain_info: BrainInfo):
	# decide which action for each agent, given the brain_info


	##################################
	#        Action Index
	#
	#         -30 0  +30  steering angle
	# +1      0   1   2
	# 0       3   4   5
	# -0.3    6   7   8
	# throttle
	#
	##################################

	# Sample placeholder, type = ndarray, shape = (agent_amount, action_size), for discrete action, size = 1
	sample_action = np.array([0,1,2,3,4,5,6,7,8,0]).transpose()

	# TODO Design your own decide algorithm here

	return sample_action

def run_general_ml():

	### Parameters
	env_path = None # leave it None
	curriculum_file = None # leave it None
	no_graphics = False # True if you want Unity Environment to train in background
	worker_id = 0 # leave it 0
	seed = 0 # setup whatever random seed you like
	max_step = 1e6 # total training step
	docker_training = False # leave it False

	# if true, training mode, 100x time scale, small window
	# if false, inference mode, 1x time scale, big window, with observe camera
	fast_simulation = False

	# Setup the Unity Environment
	env = UnityEnvironment(file_name=env_path, worker_id=worker_id,
	                       curriculum=curriculum_file, seed=seed,
	                       docker_training=docker_training,
	                       no_graphics=no_graphics)
	env.curriculum.set_lesson_number(1)
	brain_name = env.brain_names[0] # Get brain_name, assume only have 1 brain


	### Start learning
	curr_info = env.reset(train_mode=fast_simulation)[brain_name]
	last_update_time = time.clock()

	### Typical RL training loop
	for global_step in range(int(max_step)):

		# if step > environment's max_step (not agent's)
		if env.global_done:
			curr_info = env.reset(train_mode=fast_simulation)[brain_name]

		# Implement your own decide algorithm
		action = decide(curr_info)

		# Send Action into Unity Environment and return new_info, type = BrainInfo
		# You can refer to brain.py, I've commented the detail data structure
		new_info = env.step(vector_action={brain_name: action}, memory={brain_name: None},
		                    text_action={brain_name: None})[brain_name]

		# Calculate and Print training speed
		if global_step % 100 == 0:
			print("Steps:{:,}".format(global_step), " || Speed:",
			      format(100 / (time.clock() - last_update_time), ".2f"))
			last_update_time = time.clock()

		# Assign new_info to curr_info for next timestep training
		curr_info = new_info

	env.close()

if __name__ == '__main__':
	run_general_ml()