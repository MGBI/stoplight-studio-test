# Ogólne informacje
API oparte jest na protokole HTTP, a treść wszystkich żądań i odpowiedzi
przekazywana jest w formie obiektów języka JavaScript (JSON).

W nagłówku HTTP `Content-Type` każdego żądania API przesyłanego metodą POST
i zawierającego w treści obiekt JSON należy ustawić wartość `application/json`.

W żądaniach API przesyłanych metodą GET parametry należy umieścić w query
stringu.

Każda metoda API może zwrócić jeden z kilku możliwych kodów odpowiedzi HTTP.
Nagłówki i parametry odpowiedzi opisane poniżej dla każdej z metod zwracane są
tylko dla kodu 200 (OK).

# Autentykacja
<SecurityDefinitions />
