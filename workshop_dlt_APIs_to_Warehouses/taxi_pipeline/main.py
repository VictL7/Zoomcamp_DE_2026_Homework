import dlt
from itertools import islice
from dlt.sources.rest_api import rest_api_source


def smoke_test() -> None:
    print(f"dlt version: {dlt.__version__}")
    print(f"rest_api_source loaded: {rest_api_source is not None}")
    print(f"islice sample: {list(islice(range(10), 3))}")


if __name__ == "__main__":
    smoke_test()
