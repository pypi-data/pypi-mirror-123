import uuid
from functools import cached_property
from typing import Dict, List, Optional

from sym.flow.cli.models.service import Service
from sym.flow.cli.models.user import Identity, User


class UserUpdateSet:
    def __init__(
        self, service_data: List[Service] = [], user_data: List[User] = []
    ) -> None:
        self.users: List[User] = user_data
        self.services: List[Service] = service_data

    def add_csv_row(self, row: Dict) -> None:
        user_id = row.pop("User ID", "")
        # If no user id is empty, assume a temporary uuid for user creation
        if user_id == "":
            user_id = str(uuid.uuid4())

        user = User(id=user_id, identities=[])

        for service_key, matcher_value in row.items():
            if matcher_value != "":
                user.identities.append(
                    Identity.from_csv(
                        matcher_value=matcher_value, service_key=service_key
                    )
                )

        self.users.append(user)

    @classmethod
    def compare_user_sets(cls, original, edited) -> "OperationSets":
        from sym.flow.cli.helpers.api_operations import (
            Operation,
            OperationSets,
            OperationType,
        )

        old_users = set([user.id for user in original.users])
        new_users = set([user.id for user in edited.users])

        update_user_ops = []
        delete_user_identity_operations = []
        delete_user_ops = []

        created_users = new_users - old_users
        updated_users = new_users.intersection(old_users)
        deleted_users = old_users - new_users

        for user_id in created_users:
            new_user = edited.get_user_by_id(user_id)
            operation = Operation(
                operation_type=OperationType.update_user,
                original_value=new_user,
                new_value=new_user,
            )
            update_user_ops.append(operation)

        for user_id in updated_users:
            old_user = original.get_user_by_id(user_id)
            new_user = edited.get_user_by_id(user_id)

            old_idents = set(
                [
                    ident.service.service_key
                    for ident in old_user.identities_without_sym_service
                ]
            )
            new_idents = set(
                [
                    ident.service.service_key
                    for ident in new_user.identities_without_sym_service
                ]
            )

            created_or_updated_idents = new_idents.intersection(old_idents) | (
                new_idents - old_idents
            )
            deleted_idents = old_idents - new_idents

            for service_key in created_or_updated_idents:
                old_identity = old_user.get_identity_from_key(service_key)
                new_identity = new_user.get_identity_from_key(service_key)

                if old_identity == new_identity:
                    continue

                # Either User doesn't have this identity yet or has this identity but the value is different, update it
                operation = Operation(
                    operation_type=OperationType.update_user,
                    original_value=old_user,
                    new_value=new_user,
                )

                update_user_ops.append(operation)

            for _ in deleted_idents:
                # Identity has been deleted from the set, remove it
                operation = Operation(
                    operation_type=OperationType.delete_identity,
                    original_value=old_user,
                    new_value=new_user,
                )
                delete_user_identity_operations.append(operation)

        for user_id in deleted_users:
            user_to_delete = original.get_user_by_id(user_id)

            # User doesn't exist anymore, delete it
            operation = Operation(
                operation_type=OperationType.delete_user, original_value=user_to_delete
            )
            delete_user_ops.append(operation)

        return OperationSets(
            update_user_ops=update_user_ops,
            delete_identities_ops=delete_user_identity_operations,
            delete_user_ops=delete_user_ops,
        )

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return next(iter([user for user in self.users if user.id == user_id]), None)

    @cached_property
    def headers(self) -> List[str]:
        """The list of headers from the CSV file."""
        return [s.service_key for s in self.services]
