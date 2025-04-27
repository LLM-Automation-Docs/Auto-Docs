package main.controllers.car

interface ICarRentalService {
    suspend fun isOpenNow(): Boolean
    suspend fun getAvailableCars(): List<Car>
    suspend fun getCar(id: Int): Car?
    suspend fun getCarByModel(model: String): Car?
}