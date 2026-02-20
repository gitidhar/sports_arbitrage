import time
import random
import requests

def get_with_backoff(url: str, params: dict, timeout: int= 10, max_retries: int = 6) -> requests.Response:
    delay = 1.0
    for attempt in range(max_retries):
        resp = requests.get(url, params=params, timeout=timeout)
        if resp.status_code != 429:
            return resp
        
        retry_after = resp.headers.get("Retry-After")
        if retry_after:
            try:
                sleep_s = float(retry_after)
            except ValueError:
                sleep_s = delay * (1 + random.random())
        else:
            sleep_s = delay * (1 + random.random())

        delay = min(delay * 2, 60)
        time.sleep(sleep_s)
    return resp
