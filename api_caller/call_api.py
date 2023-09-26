def construct_entrypoint_url(service_name, port=10000, entrypoint_name="", **kwargs):
    base_url = f"http://{service_name}:{port}{entrypoint_name}"
    options = "?"
    for key, value in kwargs.items():
        options += str(key) + "=" + str(value) + "&"
    return base_url + options[:-1]


def wrap_arguments(variable, input_path, bootstrapping_number, output_path):
    arguments_dict = {
        "window_length": variable,
        "input_path": input_path,
        "bootstrapping_number": bootstrapping_number,
        "output_path": output_path,
    }
    return arguments_dict
