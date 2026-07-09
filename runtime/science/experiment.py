class ExperimentProtocol:
    """
    ExperimentProtocol specifies inputs and target outputs for verification tests.
    """
    def __init__(self, input_value, expected_output, tolerance=0.01):
        self.input_value = input_value
        self.expected_output = expected_output
        self.tolerance = tolerance


class Experiment:
    """
    Experiment executes protocol verification trials.
    """
    def __init__(self, experiment_id, protocol):
        self.id = experiment_id
        self.protocol = protocol

    def run_trial(self, simulation_func):
        """
        Executes test using the simulation function, checking against tolerance.
        """
        actual_output = simulation_func(self.protocol.input_value)
        difference = abs(actual_output - self.protocol.expected_output)
        success = difference <= self.protocol.tolerance
        return success, actual_output
