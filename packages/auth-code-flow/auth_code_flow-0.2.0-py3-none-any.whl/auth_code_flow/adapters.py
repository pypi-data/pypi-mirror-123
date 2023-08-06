from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

exponential_backoff_retry = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
    backoff_factor=1,
)

exponential_backoff_adapter = HTTPAdapter(max_retries=exponential_backoff_retry)
