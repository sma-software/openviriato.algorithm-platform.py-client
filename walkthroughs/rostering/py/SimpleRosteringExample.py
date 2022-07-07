import argparse
from typing import List

from py_client.algorithm_interface import algorithm_interface_factory
from py_client.aidm.aidm_link_classes import AlgorithmRosterLinkDefinition
from py_client.aidm.aidm_algorithm_classes import AlgorithmTrain
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface

from EmptyRunCreator import EmptyRunCreator
from Activities import CommonActivity
from CommonActivitiesFactory import CommonActivitiesFactory


def create_link_definitions_between_two_common_activities(source_common_activity: CommonActivity, target_common_activity: CommonActivity) -> List[AlgorithmRosterLinkDefinition]:
    unlinked_target_activities = list(target_common_activity.single_activities)
    roster_link_definitions = []
    for source_single_activity in source_common_activity.single_activities:
        for target_single_activity in unlinked_target_activities:
            common_rolling_stock_type = source_single_activity.rolling_stock_type_id == target_single_activity.rolling_stock_type_id
            if common_rolling_stock_type:
                # @AlgorithmRosterLinkDefinitionExample[:]
                roster_link_definition = AlgorithmRosterLinkDefinition(
                    source_single_activity.arrival_tpn_id,
                    target_single_activity.departure_tpn_id,
                    source_single_activity.position,
                    target_single_activity.position)
                roster_link_definitions.append(roster_link_definition)
                unlinked_target_activities.remove(target_single_activity)
                break
    return roster_link_definitions


def create_link_definitions_for_common_activities_of_one_train(common_activities_for_one_train: List[CommonActivity]) -> List[AlgorithmRosterLinkDefinition]:
    subsequent_common_activities = zip(common_activities_for_one_train[:-1], common_activities_for_one_train[1:])
    roster_link_definitions = []
    for source_common_activity, target_common_activity in subsequent_common_activities:
        roster_link_definitions += create_link_definitions_between_two_common_activities(source_common_activity, target_common_activity)
    return roster_link_definitions


def create_link_definitions_between_trains(algorithm_interface: AlgorithmInterface, preceding_train: AlgorithmTrain, succeeding_train: AlgorithmTrain)-> List[AlgorithmRosterLinkDefinition]:
    common_activity_factory = CommonActivitiesFactory(algorithm_interface)

    # create common activities
    common_activities_preceding_train = common_activity_factory.to_common_activities(preceding_train)
    common_activities_succeeding_train = common_activity_factory.to_common_activities(succeeding_train)
    last_common_activity_preceding_train = common_activities_preceding_train[-1]
    first_common_activity_succeeding_train = common_activities_succeeding_train[0]

    # create link definitions within each train run
    links_between_common_activities_preceding_train = create_link_definitions_for_common_activities_of_one_train(common_activities_preceding_train)
    links_between_common_activities_succeeding_train = create_link_definitions_for_common_activities_of_one_train(common_activities_succeeding_train)

    link_only_within_trains = last_common_activity_preceding_train.single_activities[0].arrival_time > first_common_activity_succeeding_train.single_activities[0].departure_time
    if link_only_within_trains:
        algorithm_interface.notify_user("Warning!", "Cannot add links between the two trains as succeeding train departs before preceding train has arrived." )
        return links_between_common_activities_preceding_train + links_between_common_activities_succeeding_train

    needs_empty_run = preceding_train.train_path_nodes[-1].node_id != succeeding_train.train_path_nodes[0].node_id
    if needs_empty_run:
        # case 1: create empty run common activity and link the common activities of the two trains through this
        empty_run_creator = EmptyRunCreator(algorithm_interface, common_activity_factory)
        empty_run_common_activity = empty_run_creator.create_empty_run_common_activity(first_common_activity_succeeding_train, last_common_activity_preceding_train, preceding_train)

        links_between_preceeding_train_and_empty_run_train = create_link_definitions_between_two_common_activities(
            last_common_activity_preceding_train, empty_run_common_activity)
        links_between_empty_run_train_and_succeeding_train = create_link_definitions_between_two_common_activities(
            empty_run_common_activity, first_common_activity_succeeding_train)
        links_between_different_trains = links_between_preceeding_train_and_empty_run_train + links_between_empty_run_train_and_succeeding_train
    else:
        # case 2: just link the common activities of the two trains
        links_between_different_trains = create_link_definitions_between_two_common_activities(last_common_activity_preceding_train, first_common_activity_succeeding_train)

    return links_between_common_activities_preceding_train + links_between_different_trains + links_between_common_activities_succeeding_train


def run(api_url: str) -> None:
    with algorithm_interface_factory.create(api_url) as algorithm_interface:
        preceding_train = algorithm_interface.get_algorithm_train_parameter("trainFrom")
        succeeding_train = algorithm_interface.get_algorithm_train_parameter("trainTo")

        roster_links_to_create = create_link_definitions_between_trains(algorithm_interface, preceding_train, succeeding_train)
        algorithm_interface.create_roster_links(roster_links_to_create)


def parse_api_url_from_command_line_arguments() -> str:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-u", "--api_url", required=True)
    command_line_arguments = vars(argument_parser.parse_args())
    api_url: str = command_line_arguments["api_url"]
    return api_url


def main():
    api_url = parse_api_url_from_command_line_arguments()
    run(api_url=api_url)


if __name__ == '__main__':
    main()
