"""Contains a list of custom lane change controllers."""

from flow.controllers.base_lane_changing_controller import \
    BaseLaneChangeController


class SimLaneChangeController(BaseLaneChangeController):
    """A controller used to enforce sumo lane-change dynamics on a vehicle.

    Usage: See base class for usage example.
    """

    def get_lane_change_action(self, env):
        """See parent class."""
        return None


class StaticLaneChanger(BaseLaneChangeController):
    """A lane-changing model used to keep a vehicle in the same lane.

    Usage: See base class for usage example.
    """

    def get_lane_change_action(self, env):
        """See parent class."""
        return 0

class SimpleMergeLaneChanger(BaseLaneChangeController):
    """A lane-changing model to control the amount of vehicles to do lane changing
    """

    def get_lane_change_action(self, env):
    """Specify the lane change action to be performed.

        If discrete lane changes are being performed, the action is a direction

        * -1: lane change right
        * 0: no lane change
        * 1: lane change left

        Parameters
        ----------
        env : flow.envs.Env
            state of the environment at the current time step

        Returns
        -------
        float or int
            requested lane change action
        """

        return 1
    
