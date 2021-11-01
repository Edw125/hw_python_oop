class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
            self,
            training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float
    ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывод строки с информационным сообщением."""
        string = (
            'Тип тренировки: {}; '
            'Длительность: {:.3f} ч.; '
            'Дистанция: {:.3f} км; '
            'Ср. скорость: {:.3f} км/ч; '
            'Потрачено ккал: {:.3f}.'
        ).format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )
        return string


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result = (self.action * self.LEN_STEP) / self.M_IN_KM
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result = self.get_distance() / self.duration
        return result

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        class_instance = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return class_instance


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        result = ((self.COEFF_CALORIE_1
                   * self.get_mean_speed()
                   - self.COEFF_CALORIE_2)
                  * self.weight
                  / self.M_IN_KM
                  * (self.duration * 60))
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 2
    COEFF_CALORIE_3 = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        result = ((self.COEFF_CALORIE_1 * self.weight
                   + (self.get_mean_speed()
                      ** self.COEFF_CALORIE_2
                      // self.height)
                   * self.COEFF_CALORIE_3
                   * self.weight)
                  * (self.duration * 60))
        return result


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании в бассейне."""
        result = ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                  * self.COEFF_CALORIE_2
                  * self.weight)
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании в бассейне."""
        result = ((self.length_pool * self.count_pool)
                  / self.M_IN_KM
                  / self.duration)
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    catalog = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in catalog.keys():
        raise KeyError(
            'Ошибка распознавания типа тренировки workout_type.'
            ' Необходимо проверить кэширующий словарь catalog'
        )
    class_instance = catalog[workout_type]
    return class_instance(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
