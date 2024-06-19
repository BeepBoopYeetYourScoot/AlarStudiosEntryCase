FIRST_TABLE_ID_RANGE = list(range(1, 11)) + list(range(31, 41))
SECOND_TABLE_ID_RANGE = list(range(11, 21)) + list(range(41, 51))
THIRD_TABLE_ID_RANGE = list(range(21, 31)) + list(range(51, 61))

FIRST_TABLE_TEST_DATA = [
    {"id": num, "name": f"Test {num}"} for num in FIRST_TABLE_ID_RANGE
]
SECOND_TABLE_TEST_DATA = [
    {"id": num, "name": f"Test {num}"} for num in SECOND_TABLE_ID_RANGE
]
THIRD_TABLE_TEST_DATA = [
    {"id": num, "name": f"Test {num}"} for num in THIRD_TABLE_ID_RANGE
]

TABLENAME_TO_CONTENTS = {
    "first_table": FIRST_TABLE_TEST_DATA,
    "second_table": SECOND_TABLE_TEST_DATA,
    "third_table": THIRD_TABLE_TEST_DATA,
}
