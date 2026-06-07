from datetime import timedelta

from django.utils import timezone
from .alert_engine import create_rule_alert
from .models import Rule
from .models import RuleMatch

from .rules import OPERATORS


COOLDOWN_MINUTES = 5


def evaluate_rules(workspace,node_id,metadata,event=None):

    active_rules = Rule.objects.filter(
        is_active=True
    )

    for rule in active_rules:

        value = metadata.get(
            rule.metric
        )

        if value is None:
            continue

        operator = OPERATORS.get(
            rule.operator
        )

        if operator is None:
            continue

        try:

            if operator(

                float(value),

                float(rule.threshold)
            ):

                recent_match = RuleMatch.objects.filter(

                    rule=rule,

                    node_id=node_id,

                    created_at__gte=(

                        timezone.now()

                        - timedelta(
                            minutes=COOLDOWN_MINUTES
                        )
                    )
                ).exists()

                if recent_match:

                    continue

                rule_match= RuleMatch.objects.create(

                    rule=rule,

                    node_id=node_id,

                    event=event,

                    observed_value=value
                )
                if rule.severity in ["WARNING","CRITICAL"]:
                    create_rule_alert(
                        workspace,
                        rule_match
                    )
                print(

                    f"[RULE MATCH] "

                    f"{rule.name} "

                    f"Node={node_id} "

                    f"Value={value}"
                )

        except Exception as error:

            print(
                f"[RULE ERROR] "
                f"{error}"
            )