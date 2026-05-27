import re


def detect_severity(log_message):

    log_message = log_message.upper()

    if 'CRITICAL' in log_message:
        return 'CRITICAL'

    elif 'ERROR' in log_message:
        return 'ERROR'

    elif 'WARNING' in log_message:
        return 'WARNING'

    return 'INFO'


def calculate_anomaly_score(log_message):

    score = 0

    keywords = [
        'FAILED',
        'TIMEOUT',
        'CRITICAL',
        'EXCEPTION',
        'ERROR',
        'UNREACHABLE',
    ]

    upper_message = log_message.upper()

    for keyword in keywords:

        if keyword in upper_message:

            score += 0.2

    return min(score, 1.0)


def extract_metadata(log_message):

    metadata = {}

    cpu_match = re.search(
        r'CPU=(\d+)',
        log_message
    )

    memory_match = re.search(
        r'MEMORY=(\d+)',
        log_message
    )

    if cpu_match:

        metadata['cpu_usage'] = int(
            cpu_match.group(1)
        )

    if memory_match:

        metadata['memory_usage'] = int(
            memory_match.group(1)
        )

    return metadata