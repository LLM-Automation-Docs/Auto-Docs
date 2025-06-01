package main.repository

import main.controllers.car.Car

interface ICarRepository {

    suspend fun getCars(): List<Car>
}