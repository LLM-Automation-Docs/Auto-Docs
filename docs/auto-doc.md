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
* **`model`**: `String` - model samochodu.
* **`year`**: `Int` - rok produkcji samochodu.

## CarRentalService

Interfejs `CarRentalService` definiuje metody:

* **`isOpenNow()`**: Zwraca wartość booleanową wskazującą, czy wypożyczalnia jest obecnie otwarta.  Metoda jest teraz zawieszająca (suspend).
* **`getAvailableCars()`**: Zwraca listę dostępnych obiektów `Car`. Metoda jest teraz zawieszająca (suspend).
* **`getCar(id: Int)`**: Zwraca obiekt `Car` o podanym identyfikatorze lub null, jeśli samochód nie istnieje. Metoda jest teraz zawieszająca (suspend).

