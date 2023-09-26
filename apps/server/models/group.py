from __future__ import annotations
from typing import List, Optional
import uuid

from sqlalchemy import Column, String, Boolean, UUID, func, or_, ForeignKey, Index
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from typings.group import GroupInput
from exceptions import GroupNotFoundException
class GroupModel(BaseModel):
    """
    Represents an group entity.

    Attributes:
        id (UUID): Unique identifier of the group.
        name (str): Name of the group.
        role (str): Role of the group.
        description (str): Description of the group.
        is_deleted (bool): Flag indicating if the group has been soft-deleted.
        is_template (bool): Flag indicating if the group is a template.
        user_id (UUID): ID of the user associated with the group.
        account_id (UUID): ID of the account associated with the group.
        is_public (bool): Flag indicating if the group is a system group.
    """
    __tablename__ = 'group'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False, index=True)
    workspace_id = Column(UUID, ForeignKey('workspace.id', ondelete='CASCADE'), nullable=True, index=True)
    account_id = Column(UUID, ForeignKey('account.id', ondelete='CASCADE'), nullable=True, index=True)
    
    created_by = Column(UUID, ForeignKey('user.id', name='fk_created_by', ondelete='CASCADE'), nullable=True, index=True)
    modified_by = Column(UUID, ForeignKey('user.id', name='fk_modified_by', ondelete='CASCADE'), nullable=True, index=True)
    creator = relationship("UserModel", foreign_keys=[created_by], lazy='select')
    
    # Define indexes
    Index('ix_group_model_workspace_id_is_deleted', 'workspace_id', 'is_deleted')
    Index('ix_group_model_account_id_is_deleted', 'account_id', 'is_deleted')
    
    def __repr__(self) -> str:
        return (
            f"Group(id={self.id}, "
            f"name='{self.name}', source_type='{self.source_type}', description='{self.description}', "
            f"is_deleted={self.is_deleted}, is_public={self.is_public}, account_id={self.account_id})"
        )

    @classmethod
    def create_group(cls, db, group, user, account):
        """
        Creates a new group with the provided configuration.

        Args:
            db: The database object.
            group_with_config: The object containing the group and configuration details.

        Returns:
            Group: The created group.

        """
        db_group = GroupModel(
            created_by=user.id, 
            account_id=account.id,
        )

        cls.update_model_from_input(db_group, group)
        db.session.add(db_group)
        db.session.flush()  # Flush pending changes to generate the group's ID
        db.session.commit()
        
        return db_group
       
    @classmethod
    def update_group(cls, db, id, group, user, account):
        """
        Creates a new group with the provided configuration.

        Args:
            db: The database object.
            group_with_config: The object containing the group and configuration details.

        Returns:
            Group: The created group.

        """
        old_group = cls.get_group_by_id(db=db, group_id=id, account=account)
        if not old_group:
            raise GroupNotFoundException("Group not found")

        db_group = cls.update_model_from_input(group_model=old_group, group_input=group)
        db_group.modified_by = user.id
        
        db.session.add(db_group)
        db.session.commit()

        return db_group
     
    @classmethod
    def update_model_from_input(cls, group_model: GroupModel, group_input: GroupInput):
        for field in GroupInput.__annotations__.keys():
            setattr(group_model, field, getattr(group_input, field))
        return group_model  

    @classmethod
    def get_groups(cls, db, account):
        groups = (
            db.session.query(GroupModel)
            .filter(GroupModel.account_id == account.id, or_(or_(GroupModel.is_deleted == False, GroupModel.is_deleted is None), GroupModel.is_deleted is None))
            .all()
        )
        return groups

    @classmethod
    def get_group_by_id(cls, db, group_id, account):
        """
            Get Group from group_id

            Args:
                session: The database session.
                group_id(int) : Unique identifier of an Group.

            Returns:
                Group: Group object is returned.
        """
        # return db.session.query(GroupModel).filter(GroupModel.account_id == account.id, or_(or_(GroupModel.is_deleted == False, GroupModel.is_deleted is None), GroupModel.is_deleted is None)).all()
        groups = (
            db.session.query(GroupModel)
            .filter(GroupModel.id == group_id, or_(or_(GroupModel.is_deleted == False, GroupModel.is_deleted is None), GroupModel.is_deleted is None))
            .first()
        )
        return groups

    @classmethod
    def delete_by_id(cls, db, group_id, account):
        db_group = db.session.query(GroupModel).filter(GroupModel.id == group_id, GroupModel.account_id==account.id).first()

        if not db_group or db_group.is_deleted:
            raise GroupNotFoundException("Group not found")

        db_group.is_deleted = True
        db.session.commit()

    

    