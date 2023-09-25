def construct_entrypoint_url(service_name, port=10000):
    return f"http://{service_name}:{port}"
