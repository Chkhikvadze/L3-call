from models.group import GroupModel
from typing import List, Optional
from typings.group import GroupOutput, GroupInput
from utils.type import convert_value_to_type

def convert_model_to_response(group_model: GroupModel) -> GroupOutput:
    group_data = {}
    
    # Extract attributes from GroupModel using annotations of Group
    for key in GroupOutput.__annotations__.keys():
        if hasattr(group_model, key):
            target_type = GroupOutput.__annotations__.get(key)
            group_data[key] = convert_value_to_type(value=getattr(group_model, key), target_type=target_type)

    return GroupOutput(**group_data)


def convert_groups_to_group_list(groups: List[GroupModel]) -> List[GroupOutput]:
    return [convert_model_to_response(group_model) for group_model in groups]