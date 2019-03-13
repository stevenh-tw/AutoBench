# Benchmark
BenchmarkManager provides a set of APIs<br>
### Sample Code:
```
BenchmarkManager(agent_amount, benchmark_episode, success_threshold, verbose) # Initialize

while True:

	action = decide(curr_info)
	new_info = env.step(action)

	if use_benchmark:
		BenchmarkManager.add_result(new_info) # Add every brain info for analysis
    
		if BenchmarkManager.is_complete():
			BenchmarkManager.analyze() # Analyze and Print the result
			break

	curr_info = new_info
```
#### Agent_amount
Agent amount of the environment

#### Benchmark_episode
Number of episode needed for benchmarking

#### Success_threshold
Minimum reward threshold being considered success in current time step

#### Benchmark_verbose
Whether or not print out episode information if episode ends


### Limitation: 
* Only support 1 benchmark concurrently
