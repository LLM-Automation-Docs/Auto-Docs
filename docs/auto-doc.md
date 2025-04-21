## RestService

Interfejs `RestService` definiuje metody:

* **`isActive()`**: Zwraca wartość booleanową wskazującą, czy usługa jest aktywna.
* **`getTaxis()`**: Zwraca listę obiektów `Taxi`.
* **`getCars()`**: Zwraca listę obiektów `Car`.


## Taxi

Klasa danych `Taxi` reprezentuje taksówkę i posiada następujące pola:

* **`id`**:  `String` - identyfikator taksówki.
* **`phone`**: `String` - numer telefonu taksówki.

## Car

Klasa danych `Car` reprezentuje samochód i posiada następujące pola:

* **`id`**: `Int` - identyfikator samochodu.
* **`name`**: `String` - nazwa samochodu.
* **`model`**: `String` - model samochodu.
* **`year`**: `Int` - rok produkcji samochodu.
