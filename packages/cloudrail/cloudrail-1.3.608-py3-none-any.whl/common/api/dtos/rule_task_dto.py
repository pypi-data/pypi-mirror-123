from dataclasses import dataclass
from typing import List, Dict

from dataclasses_json import DataClassJsonMixin


@dataclass
class RuleTaskDTO(DataClassJsonMixin):
    rule_id: str
    rule_name: str
    description: str
    rule_type: str
    security_layer: str
    resource_types: List[str]
    severity: str
    logic: str
    iac_remediation_steps: str
    console_remediation_steps: str
    last_validation: str
    account_config_ids: List[str]
    compliance: Dict[str, Dict[str, List[str]]]
