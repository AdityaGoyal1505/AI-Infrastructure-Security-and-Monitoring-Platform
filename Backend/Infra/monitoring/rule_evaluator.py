# monitoring/rule_evaluator.py

from .models import Rule
from .models import RuleMatch

from .rules import OPERATORS


def evaluate_rules(
    node_id,
    metadata,
    event=None
):

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

                RuleMatch.objects.create(

                    rule=rule,

                    node_id=node_id,

                    event=event,

                    observed_value=value
                )

                print(
                    f"[RULE MATCH] "
                    f"{rule.name}"
                )

        except Exception as error:

            print(
                f"[RULE ERROR] "
                f"{error}"
            )