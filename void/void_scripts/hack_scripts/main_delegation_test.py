import AlgorithmInterfaceCommunicationLayer
from void import AlgorithmTypeCheck
from AIDM_module import AIDM_classes


def custom_dir(c, add): return dir(type(c)) + list(c.__dict__.keys()) + add


class GetAttr:
    """Base class for attr accesses in `self._xtra` passed down to `self.default`"""

    @property
    def _xtra(self): return [o for o in dir(self.default) if not o.startswith('_')]

    def __getattr__(self, k):
        if k in self._xtra: return getattr(self.default, k)
        raise AttributeError(k)

    def __dir__(self): return custom_dir(self, self._xtra)


def initialise_algorithm_node_from_dict(node_as_dict: dict) -> AIDM_classes.AlgorithmNode:
    return AIDM_classes.AlgorithmNode(ID=node_as_dict['ID'],
                                      Code=node_as_dict['Code'],
                                      NodeTracks=node_as_dict['NodeTracks'],
                                      DebugString=node_as_dict['DebugString'])


def initialise_algorithm_node_list(list_of_nodes_as_dict: list) -> list:
    return [initialise_algorithm_node_from_dict(node_as_dict) for node_as_dict in list_of_nodes_as_dict]


def initialise_algorithm_section_track_from_dict(section_track_as_dict: dict) -> AIDM_classes.AlgorithmSectionTrack:
    return AIDM_classes.AlgorithmSectionTrack(ID=section_track_as_dict['ID'],
                                              Code=section_track_as_dict['Code'],
                                              SectionCode=section_track_as_dict['SectionCode'],
                                              DebugString=section_track_as_dict['DebugString'],
                                              Weight=section_track_as_dict['Weight'])


def initialise_algorithm_section_track_list(list_of_sections_dict: list) -> list:
    return [initialise_algorithm_section_track_from_dict(section_as_dict) for section_as_dict in list_of_sections_dict]


def check_attributes_by_list(obj, attribute_names: list):
    for attribute_name in attribute_names:
        assert (hasattr(obj, attribute_name)), 'attribute {0} is missing'.format(attribute_name)


class GenericObjectFromJson:
    def __init__(self, json_as_dict):
        vars(self).update(json_as_dict)


class TrainPathNode(GenericObjectFromJson):
    def __init__(self, json_as_dict: dict):
        GenericObjectFromJson.__init__(self, json_as_dict)
        train_path_nodes_attribute_list = ['ID', 'SectionTrackID', 'NodeID', 'NodeTrackID', 'FormationID',
                                           'ArrivalTime',
                                           'DepartureTime', 'MinimumRunTime', 'MinimumStopTime', 'StopStatus',
                                           'SequenceNumber']
        check_attributes_by_list(self, train_path_nodes_attribute_list)


class AlgorithmTrain(GenericObjectFromJson):
    TrainPathNodes: list

    def __init__(self, json_as_dict: dict):
        GenericObjectFromJson.__init__(self, json_as_dict)
        attribute_list = ['ID', 'DebugString', 'TrainPathNodes']
        check_attributes_by_list(self, attribute_list)
        # cast train path nodes:
        for i in range(len(self.TrainPathNodes)):
            self.TrainPathNodes[i] = TrainPathNode(self.TrainPathNodes[i])


class AlgorithmicPlatformInterface(GetAttr):
    __communication_layer: AlgorithmInterfaceCommunicationLayer.CommunicationLayer

    def __init__(self, base_url: str):
        self.__communication_layer = AlgorithmInterfaceCommunicationLayer.CommunicationLayer(base_url)
        print()

    def __enter__(self):
        return self  # to be used in with statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__communication_layer.currentSession.close()

    @property
    def base_url(self) -> str:
        return self.__communication_layer.base_url

    def notify_user(self, message_level_1: str, message_level_2: str) -> None:
        """
        Allows to notify the user on the other side of the api
        :param message_level_1: str
        :param message_level_2: str
        """
        AlgorithmTypeCheck.assert_parameter_is_str(message_level_1, 'message_level_1', 'notify_user')
        AlgorithmTypeCheck.assert_parameter_is_str(message_level_2, 'message_level_2', 'notify_user')
        request_body = {'messageLevel1': message_level_1, 'messageLevel2': message_level_2}
        self.__communication_layer.do_post_request('notifications', request_body)

    def show_status_message(self, short_message: str, long_message=None) -> None:
        """
        Notify the user of VIRIATO with information on the status bar
        :param short_message: str
        :param long_message: str, None if not required
        """
        AlgorithmTypeCheck.assert_parameter_is_str(short_message, 'short_message', 'show_status_message')
        if not (long_message is None):
            AlgorithmTypeCheck.assert_parameter_is_str(short_message, 'long_message', 'show_status_message')
        request_body = {'shortMessage': short_message, 'longMessage': long_message}
        self.__communication_layer.do_post_request('status-message', request_body)

    def get_neighbor_nodes(self, node_id: int) -> list:
        """
        Returns a list of all neighbor nodes of the given node x with nodeID == node_id, that is, all nodes y such
        that there exists at least one section track directly from x to y.
        :param node_id: int
        :return: list, containing all tracks
        """
        AlgorithmTypeCheck.assert_parameter_is_int(node_id, 'node_id', 'get_neighbor_nodes')
        api_response = self.__communication_layer.do_get_request('neighbor-nodes/{0}'.format(node_id))
        return initialise_algorithm_node_list(api_response.json())

    def get_node(self, node_id: int) -> AIDM_classes.AlgorithmNode:
        """
        Returns an IAlgorithm​Node dict for the given node_id
        :param node_id: int
        :return: dict,
        """
        AlgorithmTypeCheck.assert_parameter_is_int(node_id, 'node_id', 'get_node')
        api_response = self.__communication_layer.do_get_request('nodes/{0}'.format(node_id))
        return initialise_algorithm_node_from_dict(api_response.json())

    def get_directed_section_tracks(self, first_node_id: int, second_node_id: int) -> list:
        """
        get all tracks in direction of the section between the two nodes. Direction given by order of the nodes
        :param first_node_id: int
        :param second_node_id: int
        :return: tuple, containing all tracks, empty if no tracks exist
        """
        AlgorithmTypeCheck.assert_parameter_is_int(first_node_id, 'first_node_id', 'get_directed_section_tracks')
        AlgorithmTypeCheck.assert_parameter_is_int(second_node_id, 'second_node_id', 'get_directed_section_tracks')
        url_tail = 'section-tracks-between/{0}/{1}'.format(first_node_id, second_node_id)
        api_response = self.__communication_layer.do_get_request(url_tail)
        return initialise_algorithm_section_track_list(api_response.json())

    def get_parallel_section_tracks(self, section_track_id: int) -> list:
        """
        Returns a list of all section tracks starting and ending at the same nodes as the section track with id
        section_track_id independent of the traffic-ability.
        The track with id section_track_id is included in the result.
        :param section_track_id: int
        :return: tuple
        """
        AlgorithmTypeCheck.assert_parameter_is_int(section_track_id, 'section_track_id', 'get_parallel_section_tracks')
        api_response = self.__communication_layer.do_get_request(
            'section-tracks-parallel-to/{0}'.format(section_track_id))
        return initialise_algorithm_section_track_list(api_response.json())

    def get_train_classification(self, train_id: int) -> dict:
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'get_train_classification')
        api_response = self.__communication_layer.do_get_request('train-classification/{0}'.format(train_id))
        return api_response.json()

    def get_train_classifications(self) -> dict:
        api_response = self.__communication_layer.do_get_request('train-classifications')
        return api_response.json()

    def cancel_train_from(self, train_path_node_id: int) -> AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_od', 'cancel_train_from')
        post_request_body = {'trainPathNodeID': train_path_node_id}
        api_response = self.__communication_layer.do_post_request('cancel-train-from', request_body=post_request_body)
        return AlgorithmTrain(api_response.json())

    def cancel_train_to(self, train_path_node_id: int) -> AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_od', 'cancel_train_to')
        post_request_body = {'trainPathNodeID': train_path_node_id}
        api_response = self.__communication_layer.do_post_request('cancel-train-to', request_body=post_request_body)
        return AlgorithmTrain(api_response.json())

    def clone_train(self, train_id: int) -> AlgorithmTrain:
        # Cancel an existing Algorithm​Train partially and return the resulting Algorithm​Train.
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'clone_train')
        post_request_body = {'TrainID': train_id}
        api_response = self.__communication_layer.do_post_request('clone-train', request_body=post_request_body)
        return AlgorithmTrain(api_response.json())

    def set_station_track(self, train_path_node_id: int, section_track_id: int) -> AlgorithmTrain:
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', 'set_station_track')
        AlgorithmTypeCheck.assert_parameter_is_int(section_track_id, 'section_track_id', 'set_station_track')
        post_request_body = {'trainPathNodeID': train_path_node_id, 'sectionTrackID': section_track_id}
        api_response = self.__communication_layer.do_post_request('set-section-track', request_body=post_request_body)
        return AlgorithmTrain(api_response.json())

    def update_train_times(self, train_id: int, update_train_times_node: list) -> AlgorithmTrain:
        AlgorithmTypeCheck.assert_parameter_is_int(train_id, 'train_id', 'update_train_times')
        url_tail = 'trains/{0}/train-path-nodes'.format(train_id)
        put_body_list = [{'TrainPathNodeId': node.TrainPathNodeID, 'ArrivalTime': node.ArrivalTime,
                          'DepartureTime': node.DepartureTime, 'MinimumRunTime': node.MinimumRunTime,
                          'MinimumStopTime': node.MinimumStopTime, 'StopStatus': node.StopStatus}
                         for node in update_train_times_node]
        api_response = self.__communication_layer.do_put_request(url_tail, request_body=put_body_list)
        return AlgorithmTrain(api_response.json())


if __name__ == '__main__':
    IF = AlgorithmicPlatformInterface('http://localhost:8080')
    IF.base_url


