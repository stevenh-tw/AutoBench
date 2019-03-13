from mlagents.envs.brain import BrainInfo
import numpy as np

class BenchmarkManager(object):

	agent_status = [[]]
	agent_amount = None
	agent_benchmark_result = [] #[episode_len, cumulative_reward, success_goal]
	success_threshold = None
	# agent_benchmark_result = [[5,100,True],[6,120,False], [10,255,True]]
	benchmark_episode = None
	verbose = False

	@staticmethod
	def is_complete():
		return len(BenchmarkManager.agent_benchmark_result) >= BenchmarkManager.benchmark_episode

	@staticmethod
	def add_result(info: BrainInfo):

		for agent_index in range(BenchmarkManager.agent_amount):

			BenchmarkManager.agent_status[agent_index][0] += 1
			BenchmarkManager.agent_status[agent_index][1] += info.rewards[agent_index]

			if info.local_done[agent_index]:
				if BenchmarkManager.verbose:
					print('Episode Length', BenchmarkManager.agent_status[agent_index][0])
					print('Cumulative Reward', BenchmarkManager.agent_status[agent_index][1])

				u = BenchmarkManager.agent_status[agent_index][:]

				if info.rewards[agent_index] >= BenchmarkManager.success_threshold:
					u.append(True)
				else:
					u.append(False)

				BenchmarkManager.agent_benchmark_result.append(u[:])
				BenchmarkManager.agent_status[agent_index][0] = 0
				BenchmarkManager.agent_status[agent_index][1] = 0

	@staticmethod
	def analyze():

		result = np.array(BenchmarkManager.agent_benchmark_result)

		print('Episode Length: Avg = %.2f, Std = %.2f' % (np.average(result[:,0]), np.std(result[:,0])))
		print('Reward: Avg = %.2f, Std = %.2f' % (np.average(result[:,1]), np.std(result[:,1])))
		print(
			'Success Rate: ',
			'{:.0%}'.format(np.sum(result[:,2]) / len(BenchmarkManager.agent_benchmark_result))
		)


	def __init__(self, agent_amount, benchmark_episode, success_threshold, verbose):

		BenchmarkManager.agent_status = [[0 for x in range(2)] for y in range(agent_amount)]
		BenchmarkManager.agent_amount = agent_amount
		BenchmarkManager.benchmark_episode = benchmark_episode
		BenchmarkManager.success_threshold = success_threshold
		BenchmarkManager.verbose = verbose

