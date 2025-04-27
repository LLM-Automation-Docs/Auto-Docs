## RestService

## Taxi

Klasa danych `Taxi` reprezentuje taksówkę i posiada następujące pola:

* **`id`**:  `String` - identyfikator taksówki.
* **`phone`**: `String` - numer telefonu taksówki.

## Car

Klasa danych `Car` reprezentuje samochód i posiada następujące pola:

* **`id`**: `Int` - identyfikator samochodu.
* **`model`**: `String` - model samochodu.
* **`year`**: `Int` - rok produkcji samochodu.
* **`maxSpeed`**: `Int` - maksymalna prędkość samochodu.
* **`acceleration`**: `Int` - przyspieszenie samochodu.

## CarRentalService

Klasa `CarRentalService` implementuje interfejs `ICarRentalService`.

## ICarRentalService

Interfejs `ICarRentalService` definiuje metody:

* **`isOpenNow()`**: Zwraca wartość booleanową wskazującą, czy wypożyczalnia jest otwarta.
* **`getAvailableCars()`**: Zwraca listę dostępnych obiektów `Car`.
* **`getCar(id: Int)`**: Zwraca obiekt `Car` o podanym identyfikatorze lub null, jeśli samochód nie istnieje.
* **`getCarByModel(model: String)`**: Zwraca obiekt `Car` o podanym modelu lub null, jeśli samochód nie istnieje.

## Worker

Klasa danych `Worker` reprezentuje pracownika i posiada następujące pola:

* **`name`**: `String` - imię pracownika.
* **`surname`**: `String` - nazwisko pracownika.
* **`salary`**: `Double` - pensja pracownika.
* **`profession`**: `String` - zawód pracownika.

## BoltService

Interfejs `BoltService` definiuje metody:

* **`isActive()`**: Zwraca wartość booleanową wskazującą, czy usługa jest aktywna.
* **`getTaxis()`**: Zwraca listę obiektów `Taxi`.
