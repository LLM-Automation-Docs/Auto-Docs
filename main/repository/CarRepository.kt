package main.repository

import main.controller.car.Car

class CarRepository: ICarRepository {
    override suspend fun getCars(): List<Car> = listOf(
        Car(
            id = 1,
            model = "Toyota CHR",
            year = 2016,
            maxSpeed = 200,
            acceleration = 5,
        )
    )
}