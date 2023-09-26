from __future__ import annotations
from typing import List, Optional
import uuid

from sqlalchemy import Column, String, Boolean, UUID, func, or_, ForeignKey, Index
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from typings.contact import ContactInput
from exceptions import ContactNotFoundException

class ContactModel(BaseModel):
    """
    Represents an contact entity.

    Attributes:
        id (UUID): Unique identifier of the contact.
        name (str): Name of the contact.
        role (str): Role of the contact.
        description (str): Description of the contact.
        is_deleted (bool): Flag indicating if the contact has been soft-deleted.
        is_template (bool): Flag indicating if the contact is a template.
        user_id (UUID): ID of the user associated with the contact.
        account_id (UUID): ID of the account associated with the contact.
        is_public (bool): Flag indicating if the contact is a system contact.
    """
    __tablename__ = 'contact'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String, nullable=True)
    phone = Column(String) 
    email = Column(String) 
    status = Column(String)
    is_deleted = Column(Boolean, default=False, index=True)
    group_id = Column(UUID, ForeignKey('group.id', ondelete='CASCADE'), nullable=True, index=True)
    workspace_id = Column(UUID, ForeignKey('workspace.id', ondelete='CASCADE'), nullable=True, index=True)
    account_id = Column(UUID, ForeignKey('account.id', ondelete='CASCADE'), nullable=True, index=True)
    
    created_by = Column(UUID, ForeignKey('user.id', name='fk_created_by', ondelete='CASCADE'), nullable=True, index=True)
    modified_by = Column(UUID, ForeignKey('user.id', name='fk_modified_by', ondelete='CASCADE'), nullable=True, index=True)
    creator = relationship("UserModel", foreign_keys=[created_by], lazy='select')
    
    # Define indexes
    Index('ix_contact_model_workspace_id_is_deleted', 'workspace_id', 'is_deleted')
    Index('ix_contact_model_account_id_is_deleted', 'account_id', 'is_deleted')
    
    def __repr__(self) -> str:
        return (
            f"Contact(id={self.id}, "
            f"name='{self.name}', source_type='{self.source_type}', description='{self.description}', "
            f"is_deleted={self.is_deleted}, is_public={self.is_public}, account_id={self.account_id})"
        )

    @classmethod
    def create_contact(cls, db, contact, user, account):
        """
        Creates a new contact with the provided configuration.

        Args:
            db: The database object.
            contact_with_config: The object containing the contact and configuration details.

        Returns:
            Contact: The created contact.

        """
        db_contact = ContactModel(
            created_by=user.id, 
            account_id=account.id,
        )

        cls.update_model_from_input(db_contact, contact)
        db.session.add(db_contact)
        db.session.flush()  # Flush pending changes to generate the contact's ID
        db.session.commit()
        
        return db_contact
       
    @classmethod
    def update_contact(cls, db, id, contact, user, account):
        """
        Creates a new contact with the provided configuration.

        Args:
            db: The database object.
            contact_with_config: The object containing the contact and configuration details.

        Returns:
            Contact: The created contact.

        """
        old_contact = cls.get_contact_by_id(db=db, contact_id=id, account=account)
        if not old_contact:
            raise ContactNotFoundException("Contact not found")

        db_contact = cls.update_model_from_input(contact_model=old_contact, contact_input=contact)
        db_contact.modified_by = user.id
        
        db.session.add(db_contact)
        db.session.commit()

        return db_contact
     
    @classmethod
    def update_model_from_input(cls, contact_model: ContactModel, contact_input: ContactInput):
        for field in ContactInput.__annotations__.keys():
            setattr(contact_model, field, getattr(contact_input, field))
        return contact_model  

    @classmethod
    def get_contacts(cls, db, account):
        contacts = (
            db.session.query(ContactModel)
            .filter(ContactModel.account_id == account.id, or_(or_(ContactModel.is_deleted == False, ContactModel.is_deleted is None), ContactModel.is_deleted is None))
            .all()
        )
        return contacts

    @classmethod
    def get_contact_by_id(cls, db, contact_id, account):
        """
            Get Contact from contact_id

            Args:
                session: The database session.
                contact_id(int) : Unique identifier of an Contact.

            Returns:
                Contact: Contact object is returned.
        """
        # return db.session.query(ContactModel).filter(ContactModel.account_id == account.id, or_(or_(ContactModel.is_deleted == False, ContactModel.is_deleted is None), ContactModel.is_deleted is None)).all()
        contacts = (
            db.session.query(ContactModel)
            .filter(ContactModel.id == contact_id, or_(or_(ContactModel.is_deleted == False, ContactModel.is_deleted is None), ContactModel.is_deleted is None))
            .first()
        )
        return contacts

    @classmethod
    def delete_by_id(cls, db, contact_id, account):
        db_contact = db.session.query(ContactModel).filter(ContactModel.id == contact_id, ContactModel.account_id==account.id).first()

        if not db_contact or db_contact.is_deleted:
            raise ContactNotFoundException("Contact not found")

        db_contact.is_deleted = True
        db.session.commit()

    

    