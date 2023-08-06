from unittest.mock import patch

from sym.flow.cli.helpers.users import UserUpdateSet
from sym.flow.cli.models.user import User
from sym.flow.cli.symflow import symflow as click_command

MOCK_GET_USERS = [User(id="123", identities=[]), User(id="456", identities=[])]


class TestUsersUpdate:
    @patch("sym.flow.cli.commands.users.list.click.echo")
    @patch("sym.flow.cli.commands.users.list.click.edit")
    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_services",
        return_value={},
    )
    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_users",
        return_value={},
    )
    @patch("sym.flow.cli.helpers.api_operations.OperationHelper.apply_changes")
    def test_click_calls_execution_method(
        self,
        mock_operation_apply_changes,
        mock_get_user,
        mock_get_services,
        mock_click_edit,
        mock_click_echo,
        click_setup,
    ):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["users", "update"])
            assert result.exit_code == 0

        mock_click_edit.assert_called_once()
        mock_operation_apply_changes.assert_called_once()

    @patch("sym.flow.cli.commands.users.list.click.edit")
    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_services",
        return_value={},
    )
    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_users",
        return_value=MOCK_GET_USERS,
    )
    @patch("sym.flow.cli.helpers.users.UserUpdateSet.add_csv_row")
    def test_edit_the_correct_amount_of_users(
        self,
        mock_add_csv_row,
        mock_get_user,
        mock_get_services,
        mock_click_edit,
        click_setup,
    ):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["users", "update"])
            assert result.exit_code == 0

        assert mock_add_csv_row.call_count == len(
            UserUpdateSet(user_data=MOCK_GET_USERS).users
        )
