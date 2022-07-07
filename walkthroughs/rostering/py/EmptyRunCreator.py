from datetime import timedelta
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface, AlgorithmMovementType
from py_client.aidm.aidm_algorithm_classes import AlgorithmTrain
from py_client.aidm.aidm_update_classes import UpdateStopTimesTrainPathNode, UpdateRunTimesTrainPathSegment
from CommonActivitiesFactory import CommonActivitiesFactory, CommonActivity


class EmptyRunCreator:
    __algorithm_interface: AlgorithmInterface
    __common_activity_factory: CommonActivitiesFactory

    def __init__(self, algorithm_interface: AlgorithmInterface, common_activity_factory: CommonActivitiesFactory):
        self.__algorithm_interface = algorithm_interface
        self.__common_activity_factory = common_activity_factory

    def __get_empty_run_movement_type(self):
        empty_run_movement_types = [movement_type for movement_type in self.__algorithm_interface.get_movement_types() if movement_type.is_empty_train]
        if len(empty_run_movement_types) == 0:
            self.__algorithm_interface.notify_user("Warning", "Did not find an empty run movement type. Please add one to the Database. Creating a productive run.")
            return None
        else:
            empty_run_movement_type_to_use = empty_run_movement_types[0]
            return empty_run_movement_type_to_use

    def create_empty_run_common_activity(self, first_common_activity_succeeding_train: CommonActivity, last_common_activity_preceding_train: CommonActivity, template_for_empty_run: AlgorithmTrain) -> CommonActivity:
        empty_run_train = self.__create_empty_run_train(last_common_activity_preceding_train, first_common_activity_succeeding_train, template_for_empty_run)

        # by definition of the empty train it has no formation changes and therefore only one empty run common_activity will be created
        empty_run_common_activity = self.__common_activity_factory.to_common_activities(empty_run_train)[0]
        return empty_run_common_activity

    def __create_empty_run_train(self, from_common_activity: CommonActivity, to_common_activity: CommonActivity, template_for_empty_run: AlgorithmTrain) -> AlgorithmTrain:
        empty_run_movement_type_to_use = self.__get_empty_run_movement_type()

        from_node_id = from_common_activity.single_activities[0].to_node_id
        to_node_id = to_common_activity.single_activities[0].from_node_id

        empty_run_train = self.__algorithm_interface.copy_train_and_replace_route(template_for_empty_run.id, [from_node_id, to_node_id])

        train_with_updated_times = self.__update_times_on_empty_run(empty_run_train, from_common_activity, to_common_activity)

        if empty_run_movement_type_to_use is not None:
            return self.__algorithm_interface.update_movement_type(
                empty_run_movement_type_to_use.id,
                train_with_updated_times.id,
                train_with_updated_times.train_path_nodes[0].id,
                train_with_updated_times.train_path_nodes[-1].id)
        else:
            return train_with_updated_times

    def __update_times_on_empty_run(self, empty_run_train: AlgorithmTrain, common_activity_before: CommonActivity, common_activity_after: CommonActivity) -> AlgorithmTrain:
        earliest_departure_time = common_activity_before.single_activities[0].arrival_time
        latest_arrival_time = common_activity_after.single_activities[0].departure_time
        maximum_empty_run_duration = latest_arrival_time - earliest_departure_time

        # Create arbitrary run duration
        empty_run_duration = maximum_empty_run_duration / 2
        departure_time = earliest_departure_time + empty_run_duration / 2
        arrival_time = departure_time + empty_run_duration

        train_with_updated_times = self.__algorithm_interface.update_train_trajectory_stop_times(
            empty_run_train.id,
            UpdateStopTimesTrainPathNode(empty_run_train.train_path_nodes[0].id, departure_time, departure_time, timedelta(0)))

        train_with_updated_times = self.__algorithm_interface.update_train_trajectory_run_times(
            train_with_updated_times.id,
            UpdateRunTimesTrainPathSegment(train_with_updated_times.train_path_nodes[-1].id, departure_time, arrival_time, timedelta(0)))

        return train_with_updated_times
