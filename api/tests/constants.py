from db.models import FirstTable, SecondTable, ThirdTable

DATA_ENDPOINT_URL = "/collect-data"
DATA_ENDPOINT_INITIAL_TEST_DATA = {
    FirstTable: {
        "id": 1,
        "name": "kazhdiy",
    },
    SecondTable: {
        "id": 11,
        "name": "ohotnik",
    },
    ThirdTable: {
        "id": 21,
        "name": "zhelaet",
    },
}
DATA_ENDPOINT_MERGED_RESULT = sorted(
    list(DATA_ENDPOINT_INITIAL_TEST_DATA.values()), key=lambda obj: obj["id"]
)
