from AIDM_module.AIDM_classes import AlgorithmNodeTrack, AlgorithmNode
import json


def mapped_dict_to_algorithm_node_track_factory(node_track_as_dict: dict) -> AlgorithmNodeTrack:
    return AlgorithmNodeTrack(**node_track_as_dict)


def node_track_list_from_json_factory(json_string) -> list:
    json_dict = json.loads(json_string)
    return [mapped_dict_to_algorithm_node_track_factory(node_track) for node_track in json_dict['NodeTracks']]


def print_vars_of_node_track_list(node_track_list) -> None:
    for el in node_track_list:
        print(vars(el))


def case_with_two_tracks() -> None:
    json_string = ("{\n"
                   "  \"ID\": 161,\n"
                   "  \"Code\": \"85AR\",\n"
                   "  \"NodeTracks\": [\n"
                   "    {\n"
                   "      \"ID\": 162,\n"
                   "      \"Code\": \"1\",\n"
                   "      \"DebugString\": \"stationtrack:85AR_{StationTrack SID = 34138}\"\n"
                   "    },\n"
                   "    {\n"
                   "      \"ID\": 163,\n"
                   "      \"Code\": \"2\",\n"
                   "      \"DebugString\": \"stationtrack:85AR_{StationTrack SID = 34140}\"\n"
                   "    }\n"
                   "  ],\n"
                   "  \"DebugString\": \"station:85AR\"\n"
                   "}")

    AlgorithmNode.from_json_dict_factory(json.loads(json_string))


def case_with_no_tracks() -> None:
    json_string = ("{\n"
                   "  \"ID\": 161,\n"
                   "  \"Code\": \"85AR\",\n"
                   "  \"NodeTracks\": [\n"
                   "  ],\n"
                   "  \"DebugString\": \"station:85AR\"\n"
                   "}")

    AlgorithmNode.from_json_dict_factory(json.loads(json_string))


def main():
    case_with_two_tracks()
    case_with_no_tracks()


if __name__ == '__main__':
    main()
