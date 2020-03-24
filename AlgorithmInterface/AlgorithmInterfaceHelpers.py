def add_node_filter_to_get_request_params(get_request_param_dict, nodeIDs):
    get_request_param_dict["NodeFilter"] = nodeIDs
    return get_request_param_dict


def add_cut_train_to_get_request_params(get_request_param_dict):
    get_request_param_dict["CutTrain"] = True
    return get_request_param_dict