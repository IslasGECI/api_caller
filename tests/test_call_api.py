from api_caller import construct_entrypoint_url


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
