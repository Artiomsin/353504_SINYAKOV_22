def get_valid_input(prompt: str, type_cast, validation=lambda x: True, error_msg="Invalid input."):
    """Получение корректного ввода от пользователя."""
    while True:
        try:
            value = type_cast(input(prompt))
            if validation(value):
                return value
            print(error_msg)
        except ValueError:
            print(error_msg)
