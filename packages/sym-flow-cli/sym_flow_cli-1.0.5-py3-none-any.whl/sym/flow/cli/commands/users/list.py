from typing import List

import click
from tabulate import tabulate

from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.users import UserUpdateSet
from sym.flow.cli.models.user import User


@click.command(
    name="list",
    short_help="List your Users",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def users_list(options: GlobalOptions) -> None:
    """Prints a table view of Sym Users in your Organization and their corresponding identities to STDOUT.

    To modify users, use `symflow users update`.
    """
    click.echo(get_user_data(options.api_url))


def get_user_data(api_url: str) -> str:
    api = SymAPI(url=api_url)
    users = api.get_users()
    services = api.get_services()

    csv_data = UserUpdateSet(user_data=users, service_data=services)
    headers = ["User ID", *csv_data.headers]

    result = []
    for user in csv_data.users:
        result.append(prepare_user_row(csv_data=csv_data, user=user))
    return tabulate(result, headers=headers) + "\n"


def prepare_user_row(csv_data: UserUpdateSet, user: User) -> List:
    row = [user.id]
    for service in csv_data.services:
        repr_identity = user.identity_repr_for_service(service)
        row.append(repr_identity)
    return row
