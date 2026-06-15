from collections import Counter

from monitoring.models import (
    RCAInsight,
    RootCauseAnalysis,
    Correlation
)

def generate_correlation_trends():

    RCAInsight.objects.filter(
        insight_type="COMMON_CORRELATION"
    ).delete()

    correlations = list(
        Correlation.objects.filter(
            is_active=True
        ).values_list(
            "correlation_type",
            flat=True
        )
    )

    counts = Counter(correlations)

    first_correlation = Correlation.objects.first()

    if not first_correlation:
        return

    for correlation_type, count in counts.items():

        if count < 1:
            continue

        RCAInsight.objects.create(

            workspace=first_correlation.workspace,

            insight_type="COMMON_CORRELATION",

            title=correlation_type,

            description=(
                f"Occurred {count} times "
                f"across monitored nodes"
            ),

            occurrence_count=count
        )

def generate_rca_trends():

    RCAInsight.objects.filter(insight_type="COMMON_ROOT_CAUSE").delete()

    root_causes = list(RootCauseAnalysis.objects.values_list("root_cause",flat=True))

    counts = Counter(root_causes)

    for root_cause, count in counts.items():

        first_analysis = RootCauseAnalysis.objects.first()

        if not first_analysis:
            return

        if count < 2:
            continue

        RCAInsight.objects.create(

            workspace=first_analysis,

            insight_type="COMMON_ROOT_CAUSE",

            title=root_cause,

            description=(

                f"Occurred "
                f"{count} times"
            ),

            occurrence_count=count
        )


def generate_node_trends():

    RCAInsight.objects.filter(insight_type="NODE_PATTERN").delete()

    node_counter = {}

    analyses = RootCauseAnalysis.objects.all()

    if not analyses.exists():
        return

    for analysis in analyses:

        key = (analysis.node_id,analysis.root_cause)

        node_counter[key] = (node_counter.get(key,0) + 1)

    for (node_id,root_cause), count in node_counter.items():

        if count < 2:
            continue

        RCAInsight.objects.create(

            workspace=analyses.first().workspace,

            insight_type="NODE_PATTERN",

            title=node_id,

            description=(

                f"{root_cause} "
                f"occurred "
                f"{count} times"
            ),

            occurrence_count=count
        )