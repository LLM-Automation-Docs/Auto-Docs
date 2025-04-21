package main.controllers.car

interface CarRentalService {
    suspend fun isOpenNow(): Boolean
    suspend fun getAvailableCars(): List<Car>
}