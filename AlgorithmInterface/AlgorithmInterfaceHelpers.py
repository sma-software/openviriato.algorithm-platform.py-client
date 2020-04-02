import AIDMClasses.AIDM_RoutingPoint_classes


def add_node_filter_to_get_request_params(get_request_param_dict, nodeIDs):
    get_request_param_dict["NodeFilter"] = nodeIDs
    return get_request_param_dict


def add_cut_train_to_get_request_params(get_request_param_dict):
    get_request_param_dict["CutTrain"] = True
    return get_request_param_dict


def extract_parameters_from_routing_point(routing_point: AIDMClasses.AIDM_RoutingPoint_classes.RoutingPoint):
    get_request_params = {}
    if routing_point.NodeTrackID is not None:
        get_request_params["EndNodeTrackID"] = routing_point.NodeTrackID
    return get_request_params
