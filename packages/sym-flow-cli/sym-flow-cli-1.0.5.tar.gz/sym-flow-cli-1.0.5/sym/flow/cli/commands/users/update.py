import csv
import tempfile
from typing import Dict

import click

from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.api_operations import OperationHelper
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.users import UserUpdateSet
from sym.flow.cli.models.user import User


@click.command(name="update", short_help="Edit Users' Identities")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def users_update(options: GlobalOptions) -> None:
    """Create, delete or modify Sym Users and their identities such as AWS SSO IDs. This will trigger an interactive prompt to edit data in CSV format.

    \b
    Example:
        `symflow users update`
    """

    api = SymAPI(url=options.api_url)

    users = api.get_users()
    services = api.get_services()

    initial_data = UserUpdateSet(user_data=users, service_data=services)
    headers = ["User ID", *initial_data.headers]

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers, quotechar="`")
        writer.writeheader()
        for user in initial_data.users:
            writer.writerow(prepare_user_row(initial_data=initial_data, user=user))

    click.edit(filename=csv_file.name, require_save=True)

    edited_data = UserUpdateSet(service_data=services)
    with open(csv_file.name) as csv_update_file:
        reader = csv.DictReader(csv_update_file, headers, quotechar="`")
        next(reader)  # Skip header line
        for row in reader:
            if len(row) != len(headers):
                click.secho(f'Skipping row "{row}" due to invalid column count.')
                continue
            edited_data.add_csv_row(row)

    operations = UserUpdateSet.compare_user_sets(initial_data, edited_data)
    operation_helper = OperationHelper(api_url=options.api_url, operations=operations)
    operation_helper.apply_changes()


def prepare_user_row(initial_data: UserUpdateSet, user: User) -> Dict[str, str]:
    row = {}
    for service in initial_data.services:
        repr_identity = user.identity_repr_for_service(service)
        row[service.service_key] = repr_identity
    row["User ID"] = user.id
    return row
