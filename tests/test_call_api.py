from api_caller import construct_entrypoint_url


def test_construct_entrypoint_url():
    entrypoint_name = "write_something"

    construct_entrypoint_url(entrypoint_name)
