from datetime import datetime


def simple_logger_decorator(main_func):

    def new_function(*args, **kwargs):
        result = main_func(*args, **kwargs)
        log = f'Вызвана функция "{main_func.__name__}" с аргументами: {args}, {kwargs}.' \
              f'Результат выполнения: {result}.\nВызов функции произведен: {datetime.now()}'
        print(log)
        with open('log_list.txt', 'a', encoding='utf-8') as f:
            f.write(f"{log}\n")

        return result

    return new_function


def path_logger_decorator(file_path):

    def decorator(main_func):

        def new_function(*args, **kwargs):
            result = main_func(*args, **kwargs)
            log = f'Вызвана функция "{main_func.__name__}" с аргументами: {args}, {kwargs}.' \
                  f'Результат выполнения: {result}.\nВызов функции произведен: {datetime.now()}'
            print(log)
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f"{log}\n")

            return result

        return new_function

    return decorator


@simple_logger_decorator
def find_capacity(length, width, height):
    params = [length < 0, width < 0, height < 0]
    if any(params):
        return "some of parameter less than zero"
    else:
        return length * width * height


@path_logger_decorator('logger_decorator.txt')
def find_square(length, width):
    if length < 0 or width < 0:
        return "wrong parameter"
    else:
        square = length * width
    return square


def main():
    find_square(17, 8)
    find_capacity(7, 2, 3)


if __name__ == '__main__':
    main()


