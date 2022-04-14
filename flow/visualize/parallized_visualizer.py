"""Visualizer for rllib experiments.

Attributes
----------
EXAMPLE_USAGE : str
    Example call to the function, which is
    ::

        python ./visualizer_rllib.py /tmp/ray/result_dir 1

parser : ArgumentParser
    Command-line argument parser
"""

import argparse
from datetime import datetime
import gym
import numpy as np
import os
import sys
import time
import pprint
import matplotlib.pyplot as plt
import glob
import ray
import copy
#from ray.tune.utils import merge_dicts
from ray.rllib.utils import merge_dicts
import pickle
try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from ray.tune.registry import register_env,get_trainable_cls
from ray.rllib import _register_all
from flow.core.util import emission_to_csv
from flow.utils.registry import make_create_env
from flow.utils.rllib import get_flow_params
from flow.utils.rllib import get_rllib_config
from flow.utils.rllib import get_rllib_pkl
from ray.rllib.agents.callbacks import DefaultCallbacks
from flow.scenarios import scenario_dir_path
from flow.envs.multiagent.highway_MOR import MultiAgentHighwayPOEnvMerge4CollaborateMOR
from flow.envs.multiagent import MultiAgentHighwayPOEnvMerge4Hierarchy
from flow.core.params import InFlows, VehicleParams
from flow.controllers import IDMController, RLController, SimCarFollowingController
from flow.controllers import SimLaneChangeController
from flow.core.params import EnvParams, NetParams, InitialConfig, InFlows, \
                             VehicleParams, SumoParams, \
                             SumoCarFollowingParams, SumoLaneChangeParams

from flow.visualize.visualizer_util import add_vehicles, add_vehicles_no_lane_change, add_vehicles_with_lane_change, add_preset_inflows, reset_inflows, reset_inflows_i696, set_argument

from tools.matplotlib_plot import PlotWriter
import tensorflow as tf
from IPython.core.debugger import set_trace
import flow

EXAMPLE_USAGE = """
example usage:
    python ./visualizer_rllib.py /ray_results/experiment_dir/result_dir 1

Here the arguments are:
1 - the path to the simulation results
2 - the number of the checkpoint
"""

# global variables configuring diagnostics
PRINT_TO_SCREEN = False
SUMMARY_PLOTS = False
REALTIME_PLOTS = False
# The averge metrics (including inflow, outflow, speed) is measured as an
# average of the recent 1000 time steps, if MEASUREMENT_RATE=1000
MEASUREMENT_RATE=4000
#MEASUREMENT_RATE=2000

def generateHtmlplots(actions, rewards, states):
    import plotly.graph_objs as go
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    # time series
    plot([go.Scatter(x=[i for i in range(len(actions))], y=[a[0] for a in actions])], filename="actions-plot-checkpoint_" + args.checkpoint_num)
    plot([go.Scatter(x=[i for i in range(len(rewards))], y=rewards)], filename="rewards-plot-checkpoint_" + args.checkpoint_num)
    plot([go.Scatter(x=[i for i in range(len(states))], y=[s[0] for s in states])], filename="state0-plot_" + args.checkpoint_num)
    plot([go.Scatter(x=[i for i in range(len(states))], y=[s[1] for s in states])], filename="state1-plot_" + args.checkpoint_num)
    plot([go.Scatter(x=[i for i in range(len(states))], y=[s[2] for s in states])], filename="state2-plot_" + args.checkpoint_num)
    # histograms
    plot([go.Histogram(x=[a[0] for a in actions], nbinsx=100)], filename="actions-hist_" + args.checkpoint_num)
    plot([go.Histogram(x=rewards, nbinsx=100)], filename="rewards-hist_" + args.checkpoint_num)
    plot([go.Histogram(x=[s[0] for s in states], nbinsx=100)], filename="state0-hist_" + args.checkpoint_num)
    plot([go.Histogram(x=[s[1] for s in states], nbinsx=100)], filename="state1-hist_" + args.checkpoint_num)
    plot([go.Histogram(x=[s[2] for s in states], nbinsx=100)], filename="state2-hist_" + args.checkpoint_num)
    # 3d scatter of policy
    trace1 = go.Scatter3d(
        x=[s[0] for s in states],
        y=[s[2] for s in states],
        z=[np.clip(a[0], -5, 5) for a in actions],
        mode='markers',
        marker=dict(
            size=0.5,
            line=dict(
                color='rgba(217, 217, 217, 0.14)',
                width=0.1
            ),
            opacity=0.8
        )
    ) 
    data = [trace1]
    layout = go.Layout(
      margin=dict(
          l=0,
          r=0,
          b=0,
          t=0
      ),
      scene = dict(
        xaxis = dict( title='speed' ),
        yaxis = dict( title='distance' ),
        zaxis = dict( title='action' ) # not supported here, but appears in example?
      )
    )
    plot(go.Figure(data=data, layout=layout), filename='speed-dist-2-action')

class MyCallbacks(DefaultCallbacks):
    def on_episode_start(self, worker, base_env, policies, episode, **kwargs):
        # save env state when an episode starts
        env = base_env.get_unwrapped()[0]
        state = env.get_state()
        episode.user_data["initial_state"] = state

def init_agent_from_policy_dir(policy_dir, checkpoint_num):
    if checkpoint_num is None:
        folder_names=[x[0] for x in os.walk(policy_dir)]
        print("folder_names", folder_names)
        max_checkpoint=None
        for fname in folder_names:
            #print(fname)
            if "checkpoint_" in fname:
                checkpoint_index=fname.index("checkpoint_")+len("checkpoint_")
                checkpoint_num=int(fname[checkpoint_index:])
                if max_checkpoint is None or max_checkpoint<checkpoint_num:
                    max_checkpoint=checkpoint_num
    else:
        max_checkpoint=checkpoint_num
    #print("max checkpoint", max_checkpoint)
    if max_checkpoint is not None:
        from flow.envs.multiagent.trained_policy import init_policy_agent 
        checkpoint_dir=os.path.join(policy_dir, 'checkpoint_'+str(max_checkpoint),'checkpoint-'+str(max_checkpoint))
        return init_policy_agent(policy_dir, checkpoint_dir)
    return None

def plot_metrics_per_time_step(args, recorded_inflow, recorded_outflow, total_num_cars_per_step, final_inflows, final_outflows, vel, rollout_index, horizon):
    # plot the inflows, outflow, avg_speed, reward at each time step
    # handles to print the metrics along the history
    if args.print_vehicles_per_time_step_in_file is not None:
        title_spec=args.print_metric_per_time_step_in_file
        separator_index=title_spec.rfind("/")
        title_spec=title_spec[separator_index+1:]
        title_spec=title_spec.replace("_", "-")

    if args.print_vehicles_per_time_step_in_file is not None and i==0:
        veh_plot=PlotWriter("Time steps", "Number of vehicles") 
        veh_plot.set_title(title_spec) 
        veh_plot.set_plot_range(0, horizon, 0, 100) 
        veh_plot.add_human=False
        veh_plot.add_plot("model", total_num_cars_per_step)
        veh_plot.write_plot(args.print_vehicles_per_time_step_in_file+"_veh.tex", 1)

    inflow_plot=None
    outflow_plot=None
    speed_plot=None
    reward_plot=None

    if args.print_vehicles_per_time_step_in_file is not None and rollout_index==0:
        inflow_plot=PlotWriter("Time steps", "Inflow") 
        inflow_plot.set_title(title_spec+" inflow: %f" % np.mean(final_inflows)) 
        inflow_plot.set_plot_range(0, horizon, 2600, 3200) 
        outflow_plot=PlotWriter("Time steps", "Outflow") 
        outflow_plot.set_title(title_spec+" outflow: %f" % np.mean(final_outflows)) 
        outflow_plot.set_plot_range(0, horizon, 2600, 3200) 
        speed_plot=PlotWriter("Time steps", "Speed") 
        speed_plot.set_title(title_spec+" speed: %f" % np.mean(vel)) 
        speed_plot.set_plot_range(0, horizon, 0, 40) 
        reward_plot=PlotWriter("Time steps", "Reward") 
        reward_plot.set_title(title_spec+" reward") 
        reward_plot.set_plot_range(0, horizon, 0, 2000) 
        
        inflow_outflow_plot=PlotWriter("Time steps", "Inflow Outflow") 
        inflow_outflow_plot.set_plot_range(0, horizon, 2600, 3200) 

        averaged_inflow_outflow_plot=PlotWriter("Time steps", "Averaged Inflow Outflow") 
        averaged_inflow_outflow_plot.set_title(title_spec+" avg inflow outflow") 
        averaged_inflow_outflow_plot.set_plot_range(0, horizon, 2600, 3200) 
        
        inflow_outflow_mean_plot=PlotWriter("Time steps", "Inflow Outflow") 
        inflow_outflow_mean_plot.set_plot_range(0, horizon, 2600, 3200) 

        inflow_outflow_var_plot=PlotWriter("Time steps", "Inflow Outflow Var") 
        inflow_outflow_var_plot.set_plot_range(0, horizon, 0, 100) 

        inflow_mean=np.mean(recorded_inflow[-1000:])
        inflow_std=np.std(recorded_inflow[-1000:])
        outflow_mean=np.mean(recorded_outflow[-1000:])
        outflow_std=np.std(recorded_outflow[-1000:])
        if args.print_inflow_outflow_var_in_file is not None:
            inflow_outflow_mean_var_log= open(args.print_inflow_outflow_var_in_file+".txt", "a")
            inflow_outflow_mean_var_log.write(title_spec+" inflow: %.2f, %.2f" % (inflow_mean, inflow_std)+" outflow: %.2f, %.2f\n" % (outflow_mean, outflow_std))
            print("****mean and variance",inflow_mean, inflow_std, outflow_mean, outflow_std, len(inflow_per_time_step), len(outflow_per_time_step))
            inflow_outflow_mean_var_log.close()

        inflow_outflow_plot.set_title(title_spec+" inflow: %.2f, %.2f" % (inflow_mean, inflow_std)+" outflow: %.2f, %.2f" % (outflow_mean, outflow_std)) 
        inflow_outflow_plot.add_plot("Inflow", inflow_per_time_step)
        inflow_outflow_plot.add_plot("Outflow", outflow_per_time_step)
        
        avg_inflow_per_time=list()
        avg_outflow_per_time=list()
        inflow_var_per_time=list()
        outflow_var_per_time=list()
        #set_trace()
        for i_k in range(env_params.horizon):
            left_start=-1000+i_k+1
            if left_start<0:
                left_start=0
            avg_inflow_per_time.append((i_k, np.mean(recorded_inflow[left_start:i_k+1]), np.std(recorded_inflow[left_start:i_k+1])))
            avg_outflow_per_time.append((i_k, np.mean(recorded_outflow[left_start:i_k+1]), np.std(recorded_outflow[left_start:i_k+1])))
            inflow_var_per_time.append((i_k, np.std(recorded_inflow[left_start:i_k+1]), 0))
            outflow_var_per_time.append((i_k, np.std(recorded_outflow[left_start:i_k+1]), 0))
                
        inflow_outflow_mean_plot.add_plot("Avg Inflow", avg_inflow_per_time)
        inflow_outflow_mean_plot.add_plot("Avg Outflow", avg_outflow_per_time)

        inflow_outflow_var_plot.add_plot("Inflow Var", inflow_var_per_time)
        inflow_outflow_var_plot.add_plot("Outflow Var", outflow_var_per_time)

        # This is a default design of plot, which added human baseline automataicaly. We may want to change this. Here I do not want to break the existing code for plot.
        inflow_plot.add_human=False
        outflow_plot.add_human=False
        speed_plot.add_human=False
        reward_plot.add_human=False
        inflow_outflow_mean_plot.add_human=False
        inflow_outflow_var_plot.add_human=False
    
        inflow_plot.add_plot("Inflow", inflow_per_time_step)
        outflow_plot.add_plot("Outflow", outflow_per_time_step)
        speed_plot.add_plot("Speed", avg_speed_per_time_step)
        #reward_plot.add_plot("Reward", reward_per_time_step)

        inflow_plot.write_plot(args.print_metric_per_time_step_in_file+"_inflow.tex", 1)
        outflow_plot.write_plot(args.print_metric_per_time_step_in_file+"_outflow.tex", 1)
        speed_plot.write_plot(args.print_metric_per_time_step_in_file+"_speed.tex", 1)
        reward_plot.write_plot(args.print_metric_per_time_step_in_file+"_reward.tex", 1)
        inflow_outflow_plot.write_plot(args.print_metric_per_time_step_in_file+"_ioflow.tex", 1)
        inflow_outflow_mean_plot.write_plot(args.print_metric_per_time_step_in_file+"_ioflow_mean.tex", 1)
        inflow_outflow_var_plot.write_plot(args.print_metric_per_time_step_in_file+"_ioflow_var.tex", 1)

def print_result_summary(rets, mean_speed, std_speed, final_inflows, final_outflows, throughput_efficiency, times, multiagent):
    print('==== Summary of results ====')
    print("Return:")
    if multiagent:
        for agent_id, rew in rets.items():
            print('For agent', agent_id)
            print(rew)
            print('Average, std return: {}, {} for agent {}'.format(
                np.mean(rew), np.std(rew), agent_id))
    else:
        print(rets)
        print('Average, std: {:.2f}, {:.2f}'.format(
            np.mean(rets), np.std(rets)))

    print("\nSpeed, mean (m/s):")
    print(mean_speed)
    print('Average, std: {:.2f}, {:.2f}'.format(np.mean(mean_speed), np.std(
        mean_speed)))
    print("\nSpeed, std (m/s):")
    print(std_speed)
    print('Average, std: {:.2f}, {:.2f}'.format(np.mean(std_speed), np.std(
        std_speed)))

    # Compute arrival rate of vehicles in the last 500 sec of the run
    print("\nOutflows (veh/hr):")
    print(final_outflows)
    print('Average, std: {:.2f}, {:.2f}'.format(np.mean(final_outflows),
                                        np.std(final_outflows)))
    # Compute departure rate of vehicles in the last 500 sec of the run
    print("Inflows (veh/hr):")
    print(final_inflows)
    print('Average, std: {:.2f}, {:.2f}'.format(np.mean(final_inflows),
                                        np.std(final_inflows)))
    # Compute throughput efficiency in the last 500 sec of the
    print("Throughput efficiency (veh/hr):")
    print(throughput_efficiency)
    print('Average, std: {:.2f}, {:.2f}'.format(np.mean(throughput_efficiency),
                                        np.std(throughput_efficiency)))
    print("Time Delay")
    print(times)
    print("Time for certain number of vehicles to exit {:.2f},{:.2f}".format((np.mean(times)),np.std(times)))


@ray.remote
def visualizer_rllib(args, do_print_metric_per_time_step=False, seed=None):
    """Visualizer for RLlib experiments.

    This function takes args (see function create_parser below for
    more detailed information on what information can be fed to this
    visualizer), and renders the experiment associated with it.
    """
    result_dir = args.result_dir if args.result_dir[-1] != '/' \
        else args.result_dir[:-1]

    config = get_rllib_config(result_dir)

    # check if we have a multiagent environment but in a
    # backwards compatible way
    if config.get('multiagent', {}).get('policies', None):
        multiagent = True
        pkl = get_rllib_pkl(result_dir)
        config['multiagent'] = pkl['multiagent']
    else:
        multiagent = False

    config['callbacks'] = MyCallbacks
    # Run on only one cpu for rendering purposes
    config['num_workers'] = 0

    flow_params = get_flow_params(config)

    if args.lateral_resolution:
        flow_params['sim'].lateral_resolution=args.lateral_resolution

    # replace the project path to the scenario xml, if the result to be
    # visualized is generated from another project.
    try:
        net_params=flow_params['net']
        template_dict=net_params.template
        feature_path = 'flow/scenarios/'
        # fix the network xml
        net_path=template_dict['net']
        if feature_path in net_path:
            occur_index = net_path.rindex(feature_path)
            new_net_path = os.path.join(scenario_dir_path, net_path[occur_index + len(feature_path):])
        template_dict['net']=new_net_path
        # fix the route xml
        rou_path_list=template_dict['rou']
        new_rou_path_list=[]
        for path in rou_path_list:
            if feature_path in path:
                occur_index=path.rindex(feature_path)
                new_path=os.path.join(scenario_dir_path, path[occur_index+len(feature_path):])
                new_rou_path_list.append(new_path)
        template_dict['rou']=new_rou_path_list
    except:
        pass

    seed_tmp = None
    if seed:
        with open(seed, 'rb') as f:
            seed_tmp = pickle.load(f)
        config['seed'] = int(seed_tmp['rllib_seed'])
    elif args.use_seeds:
        with open(args.use_seeds, 'rb') as f:
            seed_tmp = pickle.load(f)
        config['seed'] = int(seed_tmp['rllib_seed'])

    # seed flow using the same random seed
    #if 'seed' in config.keys():
    #    #random.seed(config['seed'])
    #    tf.random.set_seed(config['seed'])

    # hack for old pkl files
    # TODO(ev) remove eventually
    sim_params = flow_params['sim']
    setattr(sim_params, 'num_clients', 1)
    if seed_tmp:
        #setattr(sim_params, 'seed', seed_tmp['sumo_seed'])
        sim_params.seed = int(int(seed_tmp['sumo_seed'])/10**6)
        print(sim_params.seed)
    # Determine agent and checkpoint
    config_run = config['env_config']['run'] if 'run' in config['env_config'] \
        else None
    if args.run and config_run:
        if args.run != config_run:
            print('visualizer_rllib.py: error: run argument '
                  + '\'{}\' passed in '.format(args.run)
                  + 'differs from the one stored in params.json '
                  + '\'{}\''.format(config_run))
            sys.exit(1)
    
    # Merge with `evaluation_config`.
    evaluation_config = copy.deepcopy(config.get("evaluation_config", {}))
    config = merge_dicts(config, evaluation_config) 
    
    if args.run:
        agent_cls = get_trainable_cls(args.run)
    elif config_run:
        agent_cls = get_trainable_cls(config_run)
    else:
        print('visualizer_rllib.py: error: could not find flow parameter '
              '\'run\' in params.json, '
              'add argument --run to provide the algorithm or model used '
              'to train the results\n e.g. '
              'python ./visualizer_rllib.py /tmp/ray/result_dir 1 --run PPO')
        sys.exit(1)

    sim_params.restart_instance = True
    dir_path = os.path.dirname(os.path.realpath(__file__))
    emission_path = '{0}/test_time_rollout/'.format(dir_path)
    sim_params.emission_path = emission_path if args.gen_emission else None

    # pick your rendering mode
    if args.render_mode == 'sumo_web3d':
        sim_params.num_clients = 2
        sim_params.render = False
    elif args.render_mode == 'drgb':
        sim_params.render = 'drgb'
        sim_params.pxpm = 4
    elif args.render_mode == 'sumo_gui':
        sim_params.render = True
        print('NOTE: With render mode {}, an extra instance of the SUMO GUI '
              'will display before the GUI for visualizing the result. Click '
              'the green Play arrow to continue.'.format(args.render_mode))
    elif args.render_mode == 'no_render':
        sim_params.render = False
    if args.save_render:
        sim_params.render = 'drgb'
        sim_params.pxpm = 4
        sim_params.save_render = True
    #if seed is not None: 
    #    print(seed)
    #    flow_params["env"].additional_params["use_seeds"] = seed
    #    input()
    #else:
    #    flow_params["env"].additional_params["use_seeds"] = args.use_seeds
    #sim_params.save_state_time=100
    #sim_params.save_state_file='states.xml'
    #sim_params.load_state='states.xml'
    if args.horizon:
        config['horizon'] = args.horizon
        flow_params['env'].horizon = args.horizon
    
    env_params = flow_params['env']
    env_params.restart_instance = True
    net_params=flow_params['net']


    if args.highway_len and flow_params['env_name']==MultiAgentHighwayPOEnvMerge4CollaborateMOR:
        net_params.additional_params['highway_length']=args.highway_len
    if args.on_ramps and flow_params['env_name']==MultiAgentHighwayPOEnvMerge4CollaborateMOR:
        net_params.additional_params['on_ramps_pos']=args.on_ramps

    # handset inflows, reset main merge inflows for human baseline, or convert inflows to probabaility depending on user input 
    if args.i696 is True:
        print("reset inflows for i696")
        reset_inflows_i696(args, flow_params)
    else:
        print("reset inflows")
        reset_inflows(args, flow_params)
    #print(flow_params['net'].inflows.get())
    

    # AV Penetration
    if args.handset_avp:
        env_params.additional_params['handset_avp']=(args.handset_avp/100.0)
    if args.policy_dir is not None:
        accel_result_dir=args.policy_dir    
        #flow_params['env'].additional_params['trained_dir']=result_dir
        #flow_params['env'].additional_params['env_name']=env_name
        if args.policy_checkpoint is not None:
            accel_checkpoint_dir = accel_result_dir + '/checkpoint_' + args.policy_checkpoint+"/"+'checkpoint-' + args.policy_checkpoint
        else:
            accel_checkpoint_dir = accel_result_dir + '/checkpoint_500' + "/"+'checkpoint-500'

        env_params.additional_params['trained_dir']=accel_result_dir
        env_params.additional_params['checkpoint']=accel_checkpoint_dir

    elif flow_params['env_name']==MultiAgentHighwayPOEnvMerge4Hierarchy:
        result_dir=env_params.additional_params['trained_dir']
        checkpoint_dir=env_params.additional_params['checkpoint']
    #trained_agent_ref=init_policy_agent(result_dir, checkpoint_dir)

    if args.window_size is not None:
        env_params.additional_params['window_size']=tuple(args.window_size)

    # Remove previous env; Create and register a gym+rllib env
    env_dict = gym.envs.registration.registry.env_specs.copy()
    for env in env_dict:
        del gym.envs.registration.registry.env_specs[env]
    create_env, env_name = make_create_env(params=flow_params, version=0, seeds_file=seed)
    register_env(env_name, create_env)

    if args.evaluate:
        env_params.evaluate = True

    # lower the horizon if testing
    if args.horizon:
        config['horizon'] = args.horizon
        env_params.horizon = args.horizon
    # create the agent that will be used to compute the actions
    checkpoint = result_dir + '/checkpoint_' + args.checkpoint_num
    checkpoint = checkpoint + '/checkpoint-' + args.checkpoint_num
    print("begin to initialize agent from checkpoint", checkpoint)
    agent = agent_cls(env=env_name, config=config)
    agent.restore(checkpoint)
    if args.agent_action_policy_dir:
        # TODO (yulin): load the env_name and config of the agent class
        # restore the agent from the checkpoint
        agent=init_agent_from_policy_dir(args.agent_action_policy_dir, None)    
    
    if hasattr(agent, "local_evaluator") and \
            os.environ.get("TEST_FLAG") != 'True':
        env = agent.local_evaluator.env
    else:
        env = gym.make(env_name)

       
    if multiagent:
        rets = {}
        # map the agent id to its policy
        print(config['multiagent']['policy_mapping_fn'])
        policy_map_fn = config['multiagent']['policy_mapping_fn']#.func

        for key in config['multiagent']['policies'].keys():
            rets[key] = []
    else:
        rets = []

    if config['model']['use_lstm']:
        use_lstm = True
        if multiagent:
            state_init = {}
            # map the agent id to its policy
            policy_map_fn = config['multiagent']['policy_mapping_fn'].func
            size = config['model']['lstm_cell_size']
            for key in config['multiagent']['policies'].keys():
                state_init[key] = [np.zeros(size, np.float32),
                                   np.zeros(size, np.float32)]
        else:
            state_init = [
                np.zeros(config['model']['lstm_cell_size'], np.float32),
                np.zeros(config['model']['lstm_cell_size'], np.float32)
            ]
    else:
        use_lstm = False

    env.restart_simulation(
        sim_params=sim_params, render=sim_params.render)
    
    
    # Simulate and collect metrics
    final_outflows = []
    final_inflows = []
    mean_speed = []
    std_speed = []

    # check inflows
    #print(flow_params['net'].inflows.get())
    # initialize variable to enable recording of total vehicles in the network
    if args.print_vehicles_per_time_step_in_file:
        flow.envs.enable_total_num_of_vehicles=True

    # record for visualization purposes
    actions = []
    rewards = []
    states = []
    times = []
    info = {}; info['main_inflow']=[]; info['merge_inflow']=[]
    WARMUP = args.warmup
    #total_num_cars_per_step=list()
    num_steps_vec = np.arange(0, env_params.horizon, 1)
    for i in range(args.num_rollouts):
        vel = []
        time_to_exit = 0
        state = env.reset()
        #get inflow setting and log into info here
        info['main_inflow']=env._main_inflow
        info['merge_inflow']=env._merge_inflow
        if multiagent:
            ret = {key: [0] for key in rets.keys()}
        else:
            ret = 0

        total_num_cars_per_step=list()

        # record the inflow, outflow, avg speed, reward if necessary        
        inflow_per_time_step=None
        outflow_per_time_step=None
        avg_speed_per_time_step=None
        reward_per_time_step=None
        
        # record the inflow and outflow only 
        recorded_inflow=list()
        recorded_outflow=list()
        if do_print_metric_per_time_step and i==args.num_rollouts-1: # last rollouts
            inflow_per_time_step=[]
            outflow_per_time_step=[]
            avg_speed_per_time_step=[]
            reward_per_time_step=[]

        env.action_space.seed(0) 
        for i_k in range(env_params.horizon):
            time_to_exit += 1;
            vehicles = env.unwrapped.k.vehicle
            #print("time step:", i_k)
            avg_speed_at_k=np.mean(vehicles.get_speed(vehicles.get_ids()))
            if avg_speed_at_k>0:
                vel.append(avg_speed_at_k)
            #print("after mean:", vel)
            #vel.append(np.mean(vehicles.get_speed(vehicles.get_ids())))
            #if len(state.keys()):
            #    set_trace()
            if multiagent:
                action = {}
                for agent_id in state.keys():
                    if use_lstm:
                        action[agent_id], state_init[agent_id], logits = \
                            agent.compute_action(
                            state[agent_id], state=state_init[agent_id],
                            policy_id=policy_map_fn(agent_id), explore=False)
                    else:
                        action[agent_id] = agent.compute_action(
                                state[agent_id], policy_id=policy_map_fn(agent_id), explore=False)
            else:
                action = agent.compute_action(state)
            state, reward, done, infos = env.step(action)
            # update the number of vehicles in the network
            if args.print_vehicles_per_time_step_in_file is not None and i==0:
                total_num_cars_per_step.append((i_k, infos['total_num_cars_per_step'], 0))

            inflow = vehicles.get_inflow_rate(MEASUREMENT_RATE) 
            if inflow_per_time_step is not None:
                inflow_per_time_step.append((i_k, inflow, 0)) 

            outflow = vehicles.get_outflow_rate(MEASUREMENT_RATE) 
            if outflow_per_time_step is not None:
                outflow_per_time_step.append((i_k, outflow, 0)) 

            if avg_speed_per_time_step is not None:
                avg_speed_per_time_step.append((i_k, avg_speed_at_k, 0)) 

            if reward_per_time_step is not None:
                reward_per_time_step.append((i_k, reward, 0)) 
            
            recorded_inflow.append(inflow)
            recorded_outflow.append(outflow)
            

            if multiagent:
                for actor, rew in reward.items():
                    ret[policy_map_fn(actor)][0] += rew
            else:
                ret += reward
            
            if multiagent and done['__all__']:
                break
            if not multiagent and done:
                break
            if args.use_delay>0:
                if vehicles.get_num_arrived()>=args.use_delay :
                    break
            
        if multiagent:
            for key in rets.keys():
                rets[key].append(ret[key])
        else:
            rets.append(ret)
         
                
        outflow = vehicles.get_outflow_rate(MEASUREMENT_RATE) # original: 5000
        final_outflows.append(outflow)
        inflow = vehicles.get_inflow_rate(MEASUREMENT_RATE)# original: 5000
        final_inflows.append(inflow)
        times.append(time_to_exit)

        plot_metrics_per_time_step(args, recorded_inflow, recorded_outflow, total_num_cars_per_step, final_inflows, final_outflows, vel, i, env_params.horizon)
        if np.all(np.array(final_inflows) > 1e-5):
            throughput_efficiency = [x / y for x, y in
                                     zip(final_outflows, final_inflows)]
        else:
            throughput_efficiency = [0] * len(final_inflows)
        mean_speed.append(np.mean(vel))
        std_speed.append(np.std(vel))

        
        if multiagent:
            for agent_id, rew in rets.items():
                print('Round {}, Return: {} for agent {}'.format(
                    i, ret, agent_id))
        else:
            print('Round {}, Return: {}'.format(i, ret))
    
    env.close()
    if multiagent:
        mean_rewards = []
        for agent_id, rew in rets.items():
            mean_rewards.extend(rew)
        if len(mean_rewards) > 0:
            mean_reward = np.mean(mean_rewards)
        else:
            mean_reward = 0
    else:
        mean_reward = np.mean(rets)

    #print_result_summary(rets, mean_speed, std_speed, final_inflows, final_outflows, throughput_efficiency, times, multiagent)
    
    # terminate the environment
    env.unwrapped.terminate()
   
    # if prompted, convert the emission file into a csv file
    if args.gen_emission:
        time.sleep(0.1)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        emission_filename = '{0}-emission.xml'.format(env.network.name)

        emission_path = \
            '{0}/test_time_rollout/{1}'.format(dir_path, emission_filename)

        # convert the emission file into a csv file
        emission_to_csv(emission_path)

        # print the location of the emission csv file
        emission_path_csv = emission_path[:-4] + ".csv"
        print("\nGenerated emission file at " + emission_path_csv)

        # delete the .xml version of the emission file
        os.remove(emission_path)
        

    # if we wanted to save the render, here we create the movie
    if args.save_render:
        dirs = os.listdir(os.path.expanduser('~')+'/flow_rendering')
        # Ignore hidden files
        dirs = [d for d in dirs if d[0] != '.']
        dirs.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d-%H%M%S"))
        recent_dir = dirs[-1]
        # create the movie
        movie_dir = os.path.expanduser('~') + '/flow_rendering/' + recent_dir
        save_dir = os.path.expanduser('~') + '/flow_movies'
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        os_cmd = "cd " + movie_dir + " && ffmpeg -i frame_%06d.png"
        os_cmd += " -pix_fmt yuv420p " + dirs[-1] + ".mp4"
        os_cmd += "&& cp " + dirs[-1] + ".mp4 " + save_dir + "/"
        os.system(os_cmd)
    mean_speed, mean_inflows, mean_outflows = np.mean(mean_speed), np.mean(final_inflows), np.mean(final_outflows)
    # remove agent and its resources
    del agent
    del env
 
    if multiagent:
        #return mean_speed, final_inflows, final_outflows, mean_reward, info
        return rets, mean_speed, std_speed, final_inflows, final_outflows, throughput_efficiency, times, multiagent, mean_reward, info
    #return mean_speed, final_inflows, final_outflows, mean_reward, info
    return rets, mean_speed, std_speed, final_inflows, final_outflows, throughput_efficiency, times, multiagent, mean_reward, info

def create_parser():
    """Create the parser to capture CLI arguments."""
    """
    return args
    """
    return set_argument(evaluate=True) 

from subprocess import check_output
import signal
import json

def get_pid(name):
    return  check_output(["pidof", name]).split()
    
if __name__ == '__main__':
    args= create_parser()
    if args.window_size is not None:
        if len(args.window_size)!=2:
            print("The window size has to be two elements: the left distance to the junction, and the right distance to the junction")
            exit(-1)
    if args.measurement_rate is not None:
        MEASUREMENT_RATE=args.measurement_rate*0.5 # TODO: here we assume that thte simulation step is 0.5
        print("measurement_rate", MEASUREMENT_RATE) 

    Speed = []
    Inflow = []
    Outflow = []
    Reward = []
    MainInflow = []
    MergeInflow = []
    cpus=1
    if args.cpu is not None:
        cpus=args.cpu
    ray.init(num_cpus=cpus, num_gpus=0, object_store_memory=1024*1024*1024)

    # connect to the existing ray cluster which should be initilized in the shell.
    #ray.init(address="127.0.0.1:6379", _redis_password="mitc_flow")
    #ray.init(address='auto', _redis_password='mitc_flow')

    if args.measurement_rate is not None:
        MEASUREMENT_RATE = args.measurement_rate


    if args.seed_dir:
        seed_filename = glob.glob(args.seed_dir+"/eval_seeds/*/seeds.pkl")
    else:
        seed_filename = glob.glob("eval_seeds/*/seeds.pkl")
    print(seed_filename)
    print("Using ", len(seed_filename), " random seeds")
    import random
    seed_filename.sort()
    result_dict=dict()
    for i in range(len(seed_filename)):
        if args.run_random_seed>=0:
            i=args.run_random_seed
        k=random.choice(np.arange(len(seed_filename)))
        k=i
        seed = seed_filename[k]
        print("Using seed ",k,": ", seed)
        do_print_metric_per_time_step=False
        if i==0 and args.print_metric_per_time_step_in_file is not None:
            do_print_metric_per_time_step=True
        result_id = visualizer_rllib.remote(args, do_print_metric_per_time_step, seed)
        result_dict[i]=result_id
    i=0
    for seed_index, result_id in result_dict.items(): 
        #speed, inflow, outflow, reward, info = ray.get(result_id)#visualizer_rllib(args, do_print_metric_per_time_step, seed)
        rets, mean_speed, std_speed, final_inflows, final_outflows, throughput_efficiency, times, multiagent, mean_reward, info=ray.get(result_id)
        print_result_summary(rets, mean_speed, std_speed, final_inflows, final_outflows, throughput_efficiency, times, multiagent)
        speed=mean_speed
        inflow=final_inflows
        outflow=final_outflows
        reward=mean_reward

        Speed.append(speed)
        Inflow.append(inflow)
        Outflow.append(np.mean(outflow))
        Reward.append(reward)
        if 'main_inflow' in info.keys():
            MainInflow.append(info['main_inflow'])
        if 'merge_inflow' in info.keys():
            MergeInflow.append(info['merge_inflow'])
        print("Round ",i+1, ":", speed, inflow, outflow, reward)
        print("Moving Stats at Round ", i+1, ":")
        print("Reward: {:.2f}, {:.2f}".format(np.mean(Reward), np.std(Reward)))
        print("Speed: {:.2f}, {:.2f}".format(np.mean(Speed), np.std(Speed)))
        print("Inflow: {:.2f}, {:.2f}".format(np.mean(Inflow), np.std(Inflow)))
        print("Outflow: {:.2f}, {:.2f}".format(np.mean(Outflow), np.std(Outflow)))
        print("MainInflow Setting: {}".format(info['main_inflow']))
        print("MergeInflow Setting: {}".format(info['merge_inflow']))
        i+=1
        if args.output:
            data = {}
            data['main_inflow']=MainInflow
            data['merge_inflow']=MergeInflow
            data['outflow']=Outflow
            with open(args.output,'w') as f: 
                json.dump(data,f)
        if args.render_mode =="sumo_gui":
            break    
        if args.run_random_seed>=0:
            break
    ray.shutdown()
