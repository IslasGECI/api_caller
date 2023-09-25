from api_caller import construct_entrypoint_url


def test_construct_entrypoint_url():
    service_name = "eradication_progress"
    obtained_url = construct_entrypoint_url(service_name)
    expect_url = "https://eradication_progress"
    assert obtained_url == expect_url

    service_name = "edr_api"
    obtained_url = construct_entrypoint_url(service_name)
    expect_url = "https://edr_api"
    assert obtained_url == expect_url
