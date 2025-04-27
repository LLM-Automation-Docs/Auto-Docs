package main.controllers.bolt

interface TaxiService {

    fun isActive(): Boolean

    fun getTaxis(): List<Taxi>
}