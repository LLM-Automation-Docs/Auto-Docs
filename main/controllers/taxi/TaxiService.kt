package main.controllers.taxi

interface TaxiService {

    fun isActive(): Boolean

    fun getTaxis(): List<Taxi>
}