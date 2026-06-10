MAX_RETRIES = 5

def should_retry(attempt):
    return attempt < MAX_RETRIES