package main.controllers.car

interface CarRentalService {
    suspend fun isOpenNow(): Boolean
    suspend fun getAvailableCars(): List<Car>
    suspend fun getCar(id: Int): Car?
}