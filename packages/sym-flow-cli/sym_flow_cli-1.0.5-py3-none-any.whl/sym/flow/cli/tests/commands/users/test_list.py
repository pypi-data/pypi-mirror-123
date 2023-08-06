from unittest.mock import patch

import pytest

from sym.flow.cli.commands.users.list import get_user_data
from sym.flow.cli.errors import NotAuthorizedError
from sym.flow.cli.helpers.constants import DEFAULT_API_URL
from sym.flow.cli.symflow import symflow as click_command


class TestUsersList:
    @patch("sym.flow.cli.commands.users.list.click.echo")
    @patch(
        "sym.flow.cli.commands.users.list.get_user_data",
        return_value="some data",
    )
    def test_click_calls_execution_method(
        self,
        mock_get_user,
        mock_click_echo,
        click_setup,
    ):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["users", "list"])
            assert result.exit_code == 0

        mock_get_user.assert_called_once_with(DEFAULT_API_URL)
        mock_click_echo.assert_called_once_with("some data")

    @patch(
        "sym.flow.cli.commands.users.list.get_user_data",
        side_effect=ValueError("random error"),
    )
    def test_click_call_catches_unknown_error(
        self, mock_get_integration_data, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["users", "list"])
            assert result.exit_code == 1
            assert isinstance(result.exception, ValueError)
            assert str(result.exception) == "random error"

        mock_get_integration_data.assert_called_once_with(DEFAULT_API_URL)

    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_users",
        side_effect=NotAuthorizedError,
    )
    def test_users_list_not_authorized_errors(
        self,
        mock_get_users,
    ):
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            get_user_data("http://fake.symops.com/api/v1")
        mock_get_users.assert_called_once()
