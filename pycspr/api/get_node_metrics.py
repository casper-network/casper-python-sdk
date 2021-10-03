from pycspr.api.constants import REST_GET_METRICS


def get_rest_name():
    return REST_GET_METRICS


def extract_result(response):
    data = response.content.decode("utf-8")
    data = sorted([i.strip()
                  for i in data.split("\n") if not i.startswith("#")])
    return data


def get_params(metric_id: int = None):
    # @TODO: use metric_id
    return {}
