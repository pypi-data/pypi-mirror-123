class GLOBAL:
    func_dict = {}


def register(func):
    print(f"registering {func.__name__}")
    GLOBAL.func_dict[func.__name__] = func
    return func

