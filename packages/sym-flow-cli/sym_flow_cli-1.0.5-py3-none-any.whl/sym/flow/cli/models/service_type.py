from enum import Enum
from typing import Callable, List, NamedTuple, Optional


class ServiceTypeMeta(NamedTuple):
    type_name: str
    external_id_name: str
    validator: Optional[Callable[[str], bool]] = None
    help_str: Optional[str] = None


class ServiceType(ServiceTypeMeta, Enum):
    """All Service Types recognized by the Sym API"""

    @classmethod
    def all(cls) -> List[str]:
        """Returns all service_type names accepted by the CLI"""
        return [key.value.type_name for key in cls]

    SYM = ServiceTypeMeta("sym", "Org Slug")
    SLACK = ServiceTypeMeta(
        "slack",
        "Workspace ID",
        lambda id: id.startswith("T") and id.isupper(),
        "Must start with 'T' and be all upper case",
    )
    AWS_SSO = ServiceTypeMeta(
        "aws_sso",
        "Instance ARN",
        lambda arn: arn.startswith("arn:aws:sso:::instance/"),
        "Must start with 'arn:aws:sso:::instance/'",
    )
    PAGERDUTY = ServiceTypeMeta("pagerduty", "Account Number")
    AWS_IAM = ServiceTypeMeta(
        "aws_iam",
        "Account #",
        lambda acct_num: acct_num.isdigit() and len(acct_num) == 12,
        "Must be a 12 digit account number",
    )
    APTIBLE = ServiceTypeMeta("aptible", "Organization ID")
    GOOGLE = ServiceTypeMeta("google", "Email Domain")
    AUTH0 = ServiceTypeMeta("auth0", "External ID")
    OKTA = ServiceTypeMeta("okta", "Okta Domain")
