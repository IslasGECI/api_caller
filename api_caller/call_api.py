def construct_entrypoint_url(service_name, port=10000, entrypoint_name=""):
    return f"http://{service_name}:{port}{entrypoint_name}"
