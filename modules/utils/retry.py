import time


from config import MAX_RETRIES, RETRY_DELAY


def retry(func, retries=MAX_RETRIES, delay=RETRY_DELAY, *args, **kwargs):
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < retries - 1:
                time.sleep(delay)

    return None