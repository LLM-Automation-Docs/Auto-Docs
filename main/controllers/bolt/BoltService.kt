package main.controllers.bolt

interface BoltService {

    fun isActive(): Boolean

    fun getTaxis(): List<Taxi>
}