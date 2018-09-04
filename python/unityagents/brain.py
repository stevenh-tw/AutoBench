from typing import Dict


class BrainInfo:
    def __init__(self, visual_observation, vector_observation, text_observations, memory=None,
                 reward=None, agents=None, local_done=None,
                 vector_action=None, text_action=None, max_reached=None):
        """
        Describes experience at current step of all agents linked to a brain.
        """

        # list of np.ndarray, ndarray's shape = (agent_amount, height, width, 1)
        self.visual_observations = visual_observation

        # ndarray, shape = (agent_amount, vector_obs_size)
        self.vector_observations = vector_observation

        # Basically ignore it
        self.text_observations = text_observations

        # Basically ignore it
        self.memories = memory

        # list of agents' reward, len = agent_size
        self.rewards = reward

        # list of boolen, len = agent_size
        self.local_done = local_done

        # list of boolen, len = agent_size
        self.max_reached = max_reached

        # list of agent ID
        self.agents = agents

        # ndarray, shape = (agent_size, action_size), action_size = 1 for discrete action
        self.previous_vector_actions = vector_action

        # Basically ignore it
        self.previous_text_actions = text_action


AllBrainInfo = Dict[str, BrainInfo]


class BrainParameters:
    def __init__(self, brain_name, brain_param):
        """
        Contains all brain-specific parameters.
        :param brain_name: Name of brain.
        :param brain_param: Dictionary of brain parameters.
        """
        self.brain_name = brain_name
        self.vector_observation_space_size = brain_param["vectorObservationSize"]
        self.num_stacked_vector_observations = brain_param["numStackedVectorObservations"]
        self.number_visual_observations = len(brain_param["cameraResolutions"])
        self.camera_resolutions = brain_param["cameraResolutions"]
        self.vector_action_space_size = brain_param["vectorActionSize"]
        self.vector_action_descriptions = brain_param["vectorActionDescriptions"]
        self.vector_action_space_type = ["discrete", "continuous"][brain_param["vectorActionSpaceType"]]
        self.vector_observation_space_type = ["discrete", "continuous"][brain_param["vectorObservationSpaceType"]]

    def __str__(self):
        return '''Unity brain name: {0}
        Number of Visual Observations (per agent): {1}
        Vector Observation space type: {2}
        Vector Observation space size (per agent): {3}
        Number of stacked Vector Observation: {4}
        Vector Action space type: {5}
        Vector Action space size (per agent): {6}
        Vector Action descriptions: {7}'''.format(self.brain_name,
                                                  str(self.number_visual_observations),
                                                  self.vector_observation_space_type,
                                                  str(self.vector_observation_space_size),
                                                  str(self.num_stacked_vector_observations),
                                                  self.vector_action_space_type,
                                                  str(self.vector_action_space_size),
                                                  ', '.join(self.vector_action_descriptions))
