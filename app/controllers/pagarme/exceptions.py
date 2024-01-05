class WrongUrlError(Exception):
    def __init__(self, base_url: str, path: str, path_params: dict):
        super().__init__(f"Wrong URL: base -> {base_url} path -> {path} params -> {path_params}")


class APIGetCustomerError(Exception):
    def __init__(self):
        super().__init__("API error on getting customers from pagarme.")
