"""Empty init file to handle deprecations."""

# base scenario class
from flow.scenarios.base import Scenario

# custom scenarios
from flow.scenarios.bay_bridge import BayBridgeScenario
from flow.scenarios.bay_bridge_toll import BayBridgeTollScenario
from flow.scenarios.bottleneck import BottleneckScenario
from flow.scenarios.figure_eight import FigureEightScenario
from flow.scenarios.traffic_light_grid import TrafficLightGridScenario
from flow.networks.bottleneck import BottleneckNetwork3to2
from flow.scenarios.highway import HighwayScenario
from flow.scenarios.ring import RingScenario
from flow.scenarios.merge import MergeScenario
from flow.scenarios.multi_ring import MultiRingScenario
from flow.scenarios.minicity import MiniCityScenario
from flow.scenarios.highway_ramps import HighwayRampsScenario

from flow.scenarios.i696 import i696Scenario

# deprecated classes whose names have changed
from flow.scenarios.figure_eight import Figure8Scenario
from flow.scenarios.loop import LoopScenario
from flow.scenarios.grid import SimpleGridScenario
from flow.scenarios.multi_loop import MultiLoopScenario

# obtain directory path
from flow.scenarios.directory_path import scenario_dir_path 

__all__ = [
    "Scenario",
    "BayBridgeScenario",
    "BayBridgeTollScenario",
    "BottleneckScenario",
    "FigureEightScenario",
    "TrafficLightGridScenario",
    "HighwayScenario",
    "RingScenario",
    "MergeScenario",
    "MultiRingScenario",
    "MiniCityScenario",
    "HighwayRampsScenario",
    "i696Scenario",
    # deprecated classes
    "Figure8Scenario",
    "LoopScenario",
    "SimpleGridScenario",
    "MultiLoopScenario",
    "i696Scenario",
    "BottleneckNetwork3to2",
]
