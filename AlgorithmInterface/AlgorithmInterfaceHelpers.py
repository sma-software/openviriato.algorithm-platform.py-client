
def merge_query_parameters(query_parameter_dictionaries: list):
    return {parameter: value
            for parameter_dict in query_parameter_dictionaries
            for parameter, value in parameter_dict.items()}
