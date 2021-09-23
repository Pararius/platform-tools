from src import optimization


def test_split_into_chunks():
    chunked_result = optimization.split_into_chunks([1, 2, 3, 4, 5], 2)

    assert list(chunked_result) == [[1, 2], [3, 4], [5]]
