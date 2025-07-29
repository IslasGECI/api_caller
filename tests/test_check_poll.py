import requests
import requests_mock


def test_poll_finished():
    with requests_mock.Mocker() as m:
        entrypoint = "http://islasgeci.org:100/write_population_status/123"
        m.get(entrypoint, json={"status": "finished"})
        obtained = requests.get(entrypoint)
        assert m.call_count == 1
