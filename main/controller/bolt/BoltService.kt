package main.controller.bolt

interface BoltService {

    fun isActive(): Boolean

    fun getTaxis(): List<Taxi>
}