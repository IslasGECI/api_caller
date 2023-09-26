from api_caller import construct_entrypoint_url, wrap_arguments


def test_construct_entrypoint_url():
    service_name = "eradication_progress"
    obtained_url = construct_entrypoint_url(service_name)
    expect_url = "http://eradication_progress:10000"
    assert obtained_url == expect_url

    port = 10001
    service_name = "edr_api"
    obtained_url = construct_entrypoint_url(service_name, port)
    expect_url = "http://edr_api:10001"
    assert obtained_url == expect_url

    entrypoint_name = "/write_csv"
    obtained_url = construct_entrypoint_url(service_name, port, entrypoint_name, option_one="first")
    expect_url = "http://edr_api:10001/write_csv?option_one=first"
    assert obtained_url == expect_url

    entrypoint_name = "/write_csv"
    options = {"uno": 1, "dos": "dos"}
    obtained_url = construct_entrypoint_url(service_name, port, entrypoint_name, **options)
    expect_url = "http://edr_api:10001/write_csv?uno=1&dos=dos"
    assert obtained_url == expect_url


def test_wrap_arguments():
    window_length = 1
    input_path = "data.csv"
    bootstrapping_number = 13
    obtained = wrap_arguments(window_length, input_path, bootstrapping_number)
    assert isinstance(obtained, dict)
    assert obtained["window_length"] == window_length
    assert obtained["input_path"] == input_path
    assert obtained["bootstrapping_number"] == bootstrapping_number
