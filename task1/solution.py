import unittest


def strict(func):
    def wrapper(*args, **kwargs):
        dct = func.__annotations__  # Исправлено на __annotations__
        keys = list(dct.keys())
        for i, v in enumerate(args):
            if not isinstance(v, dct[keys[i]]):  # Используем isinstance для проверки типа
                raise TypeError(f'В вызове функции {func.__name__} несоответствие типов в параметре {keys[i]}. Ожидается {dct[keys[i]]}, получено {type(v)}')
        return func(*args, **kwargs)  # Возвращаем результат вызова функции
    return wrapper


@strict
def sum_two(a: float, b: int):
    return a + b


class TestStrictDecorator(unittest.TestCase):
    def test_sum_two_valid(self):
        self.assertEqual(sum_two(1.0, 2), 3)

    def test_sum_two_invalid(self):
        with self.assertRaises(TypeError) as context:
            sum_two(1.5, 2.4)
        self.assertIn("В вызове функции sum_two несоответствие типов в параметре b. Ожидается <class 'int'>, получено <class 'float'>", str(context.exception))


if __name__ == "__main__":
    unittest.main()
