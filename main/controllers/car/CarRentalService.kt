package main.controllers.car

import main.repository.ICarRepository

class CarRentalService(
    private val carRepository: ICarRepository,
): ICarRentalService {
    override suspend fun isOpenNow(): Boolean = true

    override suspend fun getAvailableCars(): List<Car> = carRepository.getCars()

    override suspend fun getCar(id: Int): Car? = getAvailableCars().find { it.id == id }

    override suspend fun getCarByModel(model: String): Car? = getAvailableCars().find { it.model == model }
}