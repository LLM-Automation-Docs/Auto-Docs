package main.controllers.car

class CarRentalService: ICarRentalService {
    override suspend fun isOpenNow(): Boolean = true

    override suspend fun getAvailableCars(): List<Car> = listOf(
        Car(
            id = 1,
            model = "Toyota CHR",
            year = 2016,
            maxSpeed = 200,
            acceleration = 5,
        )
    )

    override suspend fun getCar(id: Int): Car? = getAvailableCars().find { it.id == id }

    override suspend fun getCarByModel(model: String): Car? = getAvailableCars().find { it.model == model }
}