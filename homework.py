class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance
        """Получить дистанцию в км."""

    def get_mean_speed(self) -> float:
        self.speed = self.get_distance() / self.duration
        return self.speed
        """Получить среднюю скорость движения."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        information = InfoMessage(self.__class__.__name__, self.duration,
                                  self.get_distance(),
                                  self.get_mean_speed(),
                                  self.get_spent_calories())
        return information
        """Вернуть информационное сообщение о выполненной тренировке."""


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        self.calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                         * self.get_mean_speed()
                         + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                         / self.M_IN_KM * (self.duration * self.MIN_IN_H))
        return self.calories
        """Тренировка: бег."""

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class SportsWalking(Training):
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        self.calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                         + ((self.get_mean_speed()
                          * self.KMH_IN_MSEC) ** 2)
                          / (self.height / self.CM_IN_M)
                         * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                         * self.weight) * (self.duration * self.MIN_IN_H))
        return self.calories
        """Тренировка: спортивная ходьба."""

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class Swimming(Training):
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_WEIGHT_SHIFT = 1.1
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.weight = weight
        """Тренировка: плавание."""

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        self.calories = ((self.get_mean_speed()
                         + self.CALORIES_WEIGHT_SHIFT)
                         * self.CALORIES_WEIGHT_MULTIPLIER
                         * self.weight
                         * self.duration)
        return self.calories

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    training_type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return training_type[workout_type](*data)
    """Прочитать данные полученные от датчиков."""


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
