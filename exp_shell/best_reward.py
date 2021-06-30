from ray.tune import ExperimentAnalysis
from ray.tune import Analysis

analysis = ExperimentAnalysis(experiment_checkpoint_path="~/ray_results/yulin_hierarchy_eta1_0.9_eta2_0.1/experiment_state-2021-06-25_11-21-44.json")

last_checkpoint = analysis.get_last_checkpoint()
# if there are multiple trials, select a specific trial or automatically
# choose the best one according to a given metric
last_checkpoint = analysis.get_last_checkpoint(
    metric="episode_reward_mean", mode="max"
)
print(last_checkpoint)

