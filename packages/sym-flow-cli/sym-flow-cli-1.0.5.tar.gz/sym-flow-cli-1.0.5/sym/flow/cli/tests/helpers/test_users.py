import copy
from typing import List

import pytest

from sym.flow.cli.helpers.api_operations import OperationType
from sym.flow.cli.helpers.users import UserUpdateSet
from sym.flow.cli.models.service import BaseService
from sym.flow.cli.models.user import CSVMatcher, Identity, User
from sym.flow.cli.tests.factories.users import UserFactory


class TestCSVMatcher:
    def test_dict_init(self):
        matcher = {"email": "user@symops.io"}
        service = BaseService(slug="sym", external_id="cloud")
        csv_matcher = CSVMatcher.from_dict(service=service, matcher=matcher)
        assert csv_matcher.value == "user@symops.io"
        assert csv_matcher.to_dict() == matcher

    def test_unknown_mapping(self):
        service = BaseService(slug="twitter", external_id="cloud")
        value = '{"some_unknown_service":"user@sus.io"}'
        matcher = CSVMatcher(service=service, value=value)
        assert matcher.to_dict() == {"some_unknown_service": "user@sus.io"}

    def test_invalid_unknown_mapping(self):
        service = BaseService(slug="twitter", external_id="cloud")
        value = "this is not json"
        matcher = CSVMatcher(service=service, value=value)
        with pytest.raises(ValueError, match="should be valid json"):
            matcher.to_dict() == {"some_unknown_service": "user@sus.io"}


class TestIdentity:
    def test_regular_init(self):
        matcher = {"email": "user@symops.io"}
        service = BaseService(slug="google", external_id="symops.io")
        identity = Identity(matcher=matcher, service=service)
        assert identity.to_csv() == matcher["email"]

    def test_from_csv(self):
        matcher = {"email": "user@symops.io"}
        identity = Identity.from_csv(
            service_key="google:symops.io", matcher_value=matcher["email"]
        )
        assert identity.to_csv() == matcher["email"]

    def test_parse_service_key(self):
        service_type, external_id = Identity.parse_service_key("google:symops.io")
        assert service_type == "google"
        assert external_id == "symops.io"

    def test_equality(self):
        assert Identity.parse_service_key(
            "slack:symops.io"
        ) != Identity.parse_service_key("google:symops.io")
        assert Identity.parse_service_key(
            "google:symops.io"
        ) == Identity.parse_service_key("google:symops.io")


class TestUserUpdateSet:
    @pytest.fixture
    def original_data(self):
        users: List[User] = UserFactory.create_batch(5)
        return users

    @pytest.fixture
    def edited_data(self, original_data):
        edited_data = copy.deepcopy(original_data)
        # Edit user identity
        edited_data[0].identities[1].matcher = {"email": "new_email@symops.io"}
        # Delete user identity
        del edited_data[1].identities[1]
        # Delete an user
        del edited_data[-1]
        # Add an user
        edited_data.append(UserFactory.create())

        return edited_data

    def test_from_dict_init(self, original_data):
        user_set = UserUpdateSet(user_data=original_data)
        assert len(user_set.users) == len(original_data)

    def test_compare_sets(self, original_data, edited_data):
        original_set = UserUpdateSet(user_data=original_data)
        edited_set = UserUpdateSet(user_data=edited_data)
        result = UserUpdateSet.compare_user_sets(original_set, edited_set)

        assert len(result.update_user_ops) == 2
        assert result.update_user_ops[0].operation_type == OperationType.update_user

        assert len(result.delete_identities_ops) == 1
        assert (
            result.delete_identities_ops[0].operation_type
            == OperationType.delete_identity
        )

        assert len(result.delete_user_ops) == 1
        assert result.delete_user_ops[0].operation_type == OperationType.delete_user
