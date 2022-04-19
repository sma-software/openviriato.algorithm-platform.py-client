from typing import List

from py_client.aidm.aidm_algorithm_classes import AlgorithmTrain, AlgorithmTrainPathNode
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from Activities import CommonActivity, SingleActivity

class CommonActivitiesFactory:
    __next_free_single_activity_id: int
    __algorithm_interface: AlgorithmInterface

    def __init__(self, algorithm_interface: AlgorithmInterface):
        self.__next_free_single_activity_id = 1
        self.__algorithm_interface = algorithm_interface

    def to_common_activities(self, train: AlgorithmTrain) -> List[CommonActivity]:
        train_path_nodes_with_changes_of_formation = self.__calculate_train_path_node_with_change_of_formation(train)

        departure_and_arrival_node_pairs_of_common_activities = zip(
            train_path_nodes_with_changes_of_formation[:-1],
            train_path_nodes_with_changes_of_formation[1:])

        common_activities = []
        for departure_node, arrival_node in departure_and_arrival_node_pairs_of_common_activities:
            single_activities = self.__create_single_activities(departure_node, arrival_node)
            common_activity = CommonActivity(single_activities)
            common_activities.append(common_activity)

        return common_activities

    def __calculate_train_path_node_with_change_of_formation(self, train: AlgorithmTrain):
        first_train_path_node = train.train_path_nodes[0]
        last_train_path_node = train.train_path_nodes[-1]
        train_path_node_with_change_last_seen = first_train_path_node
        train_path_nodes_with_change_of_formation = [train_path_node_with_change_last_seen]

        for train_path_node in train.train_path_nodes[1:]:
            change_of_formation_found = train_path_node_with_change_last_seen.formation_id != train_path_node.formation_id
            if change_of_formation_found:
                train_path_nodes_with_change_of_formation.append(train_path_node)
                train_path_node_with_change_last_seen = train_path_node

        return train_path_nodes_with_change_of_formation

    def __create_single_activities(self, departure_node: AlgorithmTrainPathNode, arrival_node: AlgorithmTrainPathNode) -> List[SingleActivity]:
        vehicles = self.__algorithm_interface.get_formation(departure_node.formation_id)
        activities = []
        for position, vehicle in enumerate(vehicles.vehicle_type_ids):
            activity = SingleActivity(
                self.__next_free_single_activity_id,
                departure_node.id,
                departure_node.departure_time,
                departure_node.node_id, arrival_node.id,
                arrival_node.arrival_time,
                arrival_node.node_id,
                position,
                vehicle)
            self.__next_free_single_activity_id += 1
            activities.append(activity)

        return activities