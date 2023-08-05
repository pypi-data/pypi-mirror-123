# fmt: off

API_BASE_URL = "/public_api/v1"


class Urls:
    login        = API_BASE_URL + "/auth/login"
    query        = API_BASE_URL + "/query"

    columns_info = API_BASE_URL + "/columns_info"

    frames_url   = API_BASE_URL + "/frames/all"

    # Not working since using the old QE/DB
    bboxes       = API_BASE_URL + "/evaluation/bboxes"
    models       = API_BASE_URL + "/evaluation/frames/models"
    frames_ap    = API_BASE_URL + "/evaluation/frames/average_precision"

    sensors = API_BASE_URL + "/sequences/<drive_id>/sensors"

    # Not working since using the old Export API
    data         = API_BASE_URL + "/sequences/<drive_id>/data"

# fmt: on


URLS = Urls()
