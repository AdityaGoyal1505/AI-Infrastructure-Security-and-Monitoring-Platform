def get_health_bucket(score):

    if score is None:
        return -1

    return int(score // 5)