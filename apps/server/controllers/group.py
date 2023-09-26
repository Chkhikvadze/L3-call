
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import create_engine, MetaData, text
from concurrent.futures import ThreadPoolExecutor

from models.group import GroupModel
from models.config import ConfigModel
from typings.group import GroupOutput, GroupInput
from utils.auth import authenticate
from typings.auth import UserAccount
from utils.group import convert_groups_to_group_list, convert_model_to_response
from exceptions import GroupNotFoundException
from typings.config import ConfigQueryParams

router = APIRouter()

@router.post("", status_code=201, response_model=GroupOutput)
def create_group(group: GroupInput, auth: UserAccount = Depends(authenticate)) -> GroupOutput:
    """
    Create a new group with configurations.

    Args:
        group (GroupInput): Data for creating a new group with configurations.
        auth (UserAccount): Authenticated user account.

    Returns:
        GroupOutput: Created group object.
    """
    # Consider adding try-except for error handling during creation if needed
    db_group = GroupModel.create_group(db, group=group, user=auth.user, account=auth.account)
    return convert_model_to_response(GroupModel.get_group_by_id(db, db_group.id, auth.account))

@router.put("/{id}", status_code=200, response_model=GroupOutput)  # Changed status code to 200
def update_group(id: str, group: GroupInput, auth: UserAccount = Depends(authenticate)) -> GroupOutput:
    """
    Update an existing group with configurations.

    Args:
        id (str): ID of the group to update.
        group (GroupInput): Data for updating the group with configurations.
        auth (UserAccount): Authenticated user account.

    Returns:
        GroupOutput: Updated group object.
    """
    try:
        db_group = GroupModel.update_group(db, 
                                           id=id, 
                                           group=group, 
                                           user=auth.user, 
                                           account=auth.account)
        return convert_model_to_response(GroupModel.get_group_by_id(db, db_group.id, auth.account))
    
    except GroupNotFoundException:
        raise HTTPException(status_code=404, detail="Group not found")


@router.get("", response_model=List[GroupOutput])
def get_groups(auth: UserAccount = Depends(authenticate)) -> List[GroupOutput]:
    """
    Get all groups by account ID.

    Args:
        auth (UserAccount): Authenticated user account.

    Returns:
        List[GroupOutput]: List of groups associated with the account.
    """
    db_groups = GroupModel.get_groups(db=db, account=auth.account)
    return convert_groups_to_group_list(db_groups)

@router.get("/{id}", response_model=GroupOutput)
def get_group_by_id(id: str, auth: UserAccount = Depends(authenticate)) -> GroupOutput:
    """
    Get a group by its ID.

    Args:
        id (str): ID of the group.
        auth (UserAccount): Authenticated user account.

    Returns:
        GroupOutput: Group associated with the given ID.
    """
    db_group = GroupModel.get_group_by_id(db, group_id=id, account=auth.account)
    
    if not db_group or db_group.is_deleted:
        raise HTTPException(status_code=404, detail="Group not found")  # Ensure consistent case in error messages

    return convert_model_to_response(db_group)

@router.delete("/{group_id}", status_code=200)  # Changed status code to 204
def delete_group(group_id: str, auth: UserAccount = Depends(authenticate)):
    """
    Delete a group by its ID. Performs a soft delete by updating the is_deleted flag.

    Args:
        group_id (str): ID of the group to delete.
        auth (UserAccount): Authenticated user account.

    Returns:
        dict: A dictionary indicating the success or failure of the deletion.
    """
    try:
        GroupModel.delete_by_id(db, group_id=group_id, account=auth.account)
        return { "message": "Group deleted successfully" }

    except GroupNotFoundException:
        raise HTTPException(status_code=404, detail="Group not found")

