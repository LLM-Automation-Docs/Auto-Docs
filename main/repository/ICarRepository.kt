package main.repository

import main.controller.car.Car

interface ICarRepository {

    suspend fun getCars(): List<Car>
}