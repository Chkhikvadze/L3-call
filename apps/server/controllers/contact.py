
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import create_engine, MetaData, text
from concurrent.futures import ThreadPoolExecutor

from models.contact import ContactModel
from models.config import ConfigModel
from typings.contact import ContactOutput, ContactInput
from utils.auth import authenticate
from typings.auth import UserAccount
from utils.contact import convert_contacts_to_contact_list, convert_model_to_response
from exceptions import ContactNotFoundException
from typings.config import ConfigQueryParams

router = APIRouter()

@router.post("", status_code=201, response_model=ContactOutput)
def create_contact(contact: ContactInput, auth: UserAccount = Depends(authenticate)) -> ContactOutput:
    """
    Create a new contact with configurations.

    Args:
        contact (ContactInput): Data for creating a new contact with configurations.
        auth (UserAccount): Authenticated user account.

    Returns:
        ContactOutput: Created contact object.
    """
    # Consider adding try-except for error handling during creation if needed
    db_contact = ContactModel.create_contact(db, contact=contact, user=auth.user, account=auth.account)
    return convert_model_to_response(ContactModel.get_contact_by_id(db, db_contact.id, auth.account))

@router.put("/{id}", status_code=200, response_model=ContactOutput)  # Changed status code to 200
def update_contact(id: str, contact: ContactInput, auth: UserAccount = Depends(authenticate)) -> ContactOutput:
    """
    Update an existing contact with configurations.

    Args:
        id (str): ID of the contact to update.
        contact (ContactInput): Data for updating the contact with configurations.
        auth (UserAccount): Authenticated user account.

    Returns:
        ContactOutput: Updated contact object.
    """
    try:
        db_contact = ContactModel.update_contact(db, 
                                           id=id, 
                                           contact=contact, 
                                           user=auth.user, 
                                           account=auth.account)
        return convert_model_to_response(ContactModel.get_contact_by_id(db, db_contact.id, auth.account))
    
    except ContactNotFoundException:
        raise HTTPException(status_code=404, detail="Contact not found")


@router.get("", response_model=List[ContactOutput])
def get_contacts(auth: UserAccount = Depends(authenticate)) -> List[ContactOutput]:
    """
    Get all contacts by account ID.

    Args:
        auth (UserAccount): Authenticated user account.

    Returns:
        List[ContactOutput]: List of contacts associated with the account.
    """
    db_contacts = ContactModel.get_contacts(db=db, account=auth.account)
    return convert_contacts_to_contact_list(db_contacts)

@router.get("/{id}", response_model=ContactOutput)
def get_contact_by_id(id: str, auth: UserAccount = Depends(authenticate)) -> ContactOutput:
    """
    Get a contact by its ID.

    Args:
        id (str): ID of the contact.
        auth (UserAccount): Authenticated user account.

    Returns:
        ContactOutput: Contact associated with the given ID.
    """
    db_contact = ContactModel.get_contact_by_id(db, contact_id=id, account=auth.account)
    
    if not db_contact or db_contact.is_deleted:
        raise HTTPException(status_code=404, detail="Contact not found")  # Ensure consistent case in error messages

    return convert_model_to_response(db_contact)

@router.delete("/{contact_id}", status_code=200)  # Changed status code to 204
def delete_contact(contact_id: str, auth: UserAccount = Depends(authenticate)):
    """
    Delete a contact by its ID. Performs a soft delete by updating the is_deleted flag.

    Args:
        contact_id (str): ID of the contact to delete.
        auth (UserAccount): Authenticated user account.

    Returns:
        dict: A dictionary indicating the success or failure of the deletion.
    """
    try:
        ContactModel.delete_by_id(db, contact_id=contact_id, account=auth.account)
        return { "message": "Contact deleted successfully" }

    except ContactNotFoundException:
        raise HTTPException(status_code=404, detail="Contact not found")

