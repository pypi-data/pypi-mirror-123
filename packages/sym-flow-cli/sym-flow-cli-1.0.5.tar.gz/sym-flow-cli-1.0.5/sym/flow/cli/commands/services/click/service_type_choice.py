import click

from sym.flow.cli.models.service_type import ServiceType


class ServiceTypeChoice(click.Choice):
    """Custom click.Choice for ServiceType Enums

    Sets the choice to all valid enums, then converts the input str value to the ServiceType Enum
    """

    name = "service_type_choice"

    def __init__(self):
        accepted_choices = [
            s for s in ServiceType.all() if s != ServiceType.SYM.value.type_name
        ]

        super(ServiceTypeChoice, self).__init__(
            choices=accepted_choices, case_sensitive=False
        )

    def convert(self, value, param, ctx) -> ServiceType:
        service_type_str = super(ServiceTypeChoice, self).convert(value, param, ctx)
        # Service Types are defined as all uppercase enums
        return ServiceType[service_type_str.upper()]
