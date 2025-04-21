package main.controllers

interface RestService {

    fun isActive(): Boolean

    fun getTaxis(): List<Taxi>
}