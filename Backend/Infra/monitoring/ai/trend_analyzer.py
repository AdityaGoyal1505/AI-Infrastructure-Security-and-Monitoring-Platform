from django.db.models import Count

from monitoring.models import Alert,TrendSnapshot


def analyze_alert_trends():

    TrendSnapshot.objects.all().delete()

    current_count = Alert.objects.count()

    previous_count = max(current_count - 5,0)

    if previous_count == 0:
        change = 100

    else:

        change = ((current_count-previous_count)/previous_count) * 100

    trend_type = "STABLE"

    if change > 20:

        trend_type = "INCREASING"

    elif change < -20:

        trend_type = "DECREASING"

    TrendSnapshot.objects.create(

        workspace=Alert.objects.first().workspace,

        metric_name="alert_volume",

        current_value=current_count,

        previous_value=previous_count,

        change_percentage=change,

        trend_type=trend_type
    )