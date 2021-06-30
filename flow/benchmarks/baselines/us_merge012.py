"""Evaluates the baseline performance of merge without RL control.

Baseline is no AVs.
"""

import numpy as np
from flow.core.experiment import Experiment
from flow.core.params import InitialConfig
from flow.core.params import TrafficLightParams
from flow.benchmarks.us_merge_baseline import flow_params


def merge_baseline(num_runs):
    """Run script for all merge baselines.

    Parameters
    ----------
        num_runs : int
            number of rollouts the performance of the environment is evaluated
            over
        flow_params : dict
            the flow meta-parameters describing the structure of a benchmark.
            Must be one of the merge flow_params

    Returns
    -------
        flow.core.experiment.Experiment
            class needed to run simulations
    """
    exp_tag = flow_params['exp_tag']
    sim_params = flow_params['sim']
    vehicles = flow_params['veh']
    env_params = flow_params['env']
    net_params = flow_params['net']
    initial_config = flow_params.get('initial', InitialConfig())
    traffic_lights = flow_params.get('tls', TrafficLightParams())

    # set the evaluation flag to True
    env_params.evaluate = True

    # import the scenario class
    module = __import__('flow.scenarios', fromlist=[flow_params['scenario']])
    scenario_class = getattr(module, flow_params['scenario'])

    # create the scenario object
    scenario = scenario_class(
        name=exp_tag,
        vehicles=vehicles,
        net_params=net_params,
        initial_config=initial_config,
        traffic_lights=traffic_lights
    )

    # import the environment class
    module = __import__('flow.envs', fromlist=[flow_params['env_name']])
    env_class = getattr(module, flow_params['env_name'])

    # create the environment object
    env = env_class(env_params, sim_params, scenario)

    exp = Experiment(env)

    results = exp.run(num_runs, env_params.horizon, convert_to_csv=True)
    avg_speed = np.mean(results['mean_returns'])

    return avg_speed


if __name__ == '__main__':
    runs = 30  # number of simulations to average over
    res = merge_baseline(num_runs=runs)

    print('---------')
    print('TODO SEEMS WRONG The average speed across {} runs is {}'.format(runs, res))
