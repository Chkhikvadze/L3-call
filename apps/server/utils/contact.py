from models.contact import ContactModel
from typing import List, Optional
from typings.contact import ContactOutput, ContactInput
from utils.type import convert_value_to_type

def convert_model_to_response(contact_model: ContactModel) -> ContactOutput:
    contact_data = {}
    
    # Extract attributes from ContactModel using annotations of Contact
    for key in ContactOutput.__annotations__.keys():
        if hasattr(contact_model, key):
            target_type = ContactOutput.__annotations__.get(key)
            contact_data[key] = convert_value_to_type(value=getattr(contact_model, key), target_type=target_type)

    return ContactOutput(**contact_data)


def convert_contacts_to_contact_list(contacts: List[ContactModel]) -> List[ContactOutput]:
    return [convert_model_to_response(contact_model) for contact_model in contacts]