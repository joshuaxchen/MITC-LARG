"""Empty init file to ensure documentation for multi-agent envs is created."""

from flow.envs.multiagent.base import MultiEnv
from flow.envs.multiagent.ring.wave_attenuation import \
    MultiWaveAttenuationPOEnv

from flow.envs.multiagent.ring.accel import MultiAgentAccelEnv
from flow.envs.multiagent.traffic_light_grid import MultiTrafficLightGridPOEnv
from flow.envs.multiagent.highway import MultiAgentHighwayPOEnv, MultiAgentHighwayPOEnvLocalReward,\
                        MultiAgentHighwayPOEnvDistanceMergeInfo, MultiAgentHighwayPOEnvDistanceMergeInfoCollaborate,\
                        MultiAgentHighwayPOEnvDistanceMergeInfoNegative, MultiAgentHighwayPOEnvNegative,\
                        MultiAgentHighwayPOEnvCollaborate,\
                        MultiAgentHighwayPOEnvNewStates, MultiAgentHighwayPOEnvNewStatesNegative,\
                        MultiAgentHighwayPOEnvNewStatesCollaborate, MultiAgentHighwayPOEnvNewStatesZero,\
                        MultiAgentHighwayPOEnvNewStatesNegativeInflow,MultiAgentHighwayPOEnvMerge4,\
                        MultiAgentHighwayPOEnvMerge4Negative, MultiAgentHighwayPOEnvMerge4Collaborate, MultiAgentHighwayPOEnvMerge4CollaborateAdvantage, MultiAgentHighwayPOEnvMerge4CollaborateWithVehiclesAhead,\
                        MultiAgentHighwayPOEnvAblationDistance,\
                        MultiAgentHighwayPOEnvAblationDistanceCollaborate,\
                        MultiAgentHighwayPOEnvAblationConjestion,\
                        MultiAgentHighwayPOEnvAblationConjestionCollaborate,\
                        MultiAgentHighwayPOEnvAblationConjestionArrive,\
                        MultiAgentHighwayPOEnvAblationMergeInfo,\
                        MultiAgentHighwayPOEnvAblationMergeInfoCollaborate,\
                        MultiAgentHighwayPOEnvWindow,\
                        MultiAgentHighwayPOEnvWindowCollaborate,\
                        MultiAgentHighwayPOEnvAblationConjestionDistance,\
                        MultiAgentHighwayPOEnvAblationConjestionDistanceCollaborate,\
                        MultiAgentHighwayPOEnvAblationConjestionMergeInfo,\
                        MultiAgentHighwayPOEnvAblationConjestionMergeInfoCollaborate,\
                        MultiAgentHighwayPOEnvMerge4ParameterizedWindowSizeCollaborate,\
                        MultiAgentHighwayPOEnvMerge4RandomMergeCollaborate,\
                        MultiAgentHighwayPOEnvMerge4RandomMergeModifyDistCollaborate,\
                        MultiAgentHighwayPOEnvMerge4ModifyDistCollaborate

from flow.envs.multiagent.highway_window import MultiAgentHighwayPOEnvWindowFull, \
                        MultiAgentHighwayPOEnvWindowFullCollaborate
from flow.envs.multiagent.CChighway import CCMultiAgentHighwayPOEnvMerge4Arrive
from flow.envs.multiagent.adaptive_headway import MultiAgentHighwayPOEnvMerge4AdaptiveHeadway, MultiAgentHighwayPOEnvMerge4AdaptiveHeadwayCountAhead
#,MultiAgentHighwayPOEnvMerge4HierarchicalAdaptiveHeadway
from flow.envs.multiagent.hierarchical_leader_follower import MultiAgentHighwayPOEnvMerge4Hierarchy, MultiAgentHighwayPOEnvMerge4HierarchyCountAhead, MultiAgentHighwayPOEnvMerge4HierarchyDensityAhead,MultiAgentHighwayPOEnvMerge4HierarchyVehiclesBetweenNextRL


__all__ = ['MultiEnv', 'MultiAgentAccelEnv', 'MultiWaveAttenuationPOEnv',
           'MultiTrafficLightGridPOEnv', 'MultiAgentHighwayPOEnv',
           'MultiAgentHighwayPOEnvNegative',
           'MultiAgentHighwayPOEnvLocalReward',
           'MultiAgentHighwayPOEnvCollaborate',
            
           'CCMultiAgentHighwayPOEnvMerge4Arrive',

           'MultiAgentHighwayPOEnvDistanceMergeInfo',
           'MultiAgentHighwayPOEnvDistanceMergeInfoNegative',
           'MultiAgentHighwayPOEnvDistanceMergeInfoCollaborate',

           'MultiAgentHighwayPOEnvNewStates',
           'MultiAgentHighwayPOEnvNewStatesZero',
           'MultiAgentHighwayPOEnvNewStatesNegative',
           'MultiAgentHighwayPOEnvNewStatesNegativeInflow',
           'MultiAgentHighwayPOEnvNewStatesCollaborate',

           'MultiAgentHighwayPOEnvMerge4',
           'MultiAgentHighwayPOEnvMerge4Negative',
           'MultiAgentHighwayPOEnvMerge4Collaborate',

           'MultiAgentHighwayPOEnvAblationDistance',
           'MultiAgentHighwayPOEnvAblationDistanceCollaborate',

           'MultiAgentHighwayPOEnvAblationConjestion',
           'MultiAgentHighwayPOEnvAblationConjestionCollaborate',
           'MultiAgentHighwayPOEnvAblationCOnjestionArrive',
           
           'MultiAgentHighwayPOEnvAblationConjestionDistance',
           'MultiAgentHighwayPOEnvAblationConjestionDistanceCollaborate',
           
           'MultiAgentHighwayPOEnvAblationConjestionMergeInfo',
           'MultiAgentHighwayPOEnvAblationConjestionMergeInfoCollaborate',
           
           'MultiAgentHighwayPOEnvAblationMergeInfo',
           'MultiAgentHighwayPOEnvAblationMergeInfoCollaborate',
           
           'MultiAgentHighwayPOEnvWindow',
           'MultiAgentHighwayPOEnvWindowCollaborate',

           'MultiAgentHighwayPOEnvWindowFull',
           'MultiAgentHighwayPOEnvWindowFullCollaborate'
           ]
