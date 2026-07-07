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

# Szyfrowanie
API umożliwia tworzenie filtrów z wartościami zaszyfrowanymi po stronie klienta.

Przed utworzeniem takiego filtra należy skontaktować się z opiekunem klienta i w
bezpieczny sposób przekazać następujące informacje:
* `crypto_key_name` - unikalna nazwa klucza (nadana przez użytkownika)
* `crypto_key_file` - plik zawierający materiał klucza kryptograficznego:
  * dla AES – klucz kryptograficzny,
  * dla RSA – klucz publiczny
* `crypto_algorithm` - pełna nazwa algorytmu kryptograficznego,
np. AES-256-GCM lub RSA-OAEP-SHA256

Po zakończeniu konfiguracji możliwe jest szyfrowanie wartości wykorzystywanych
w filtrach dla każdego z poniższych pól:
* `content.nip`
* `content.regon`
* `content.krs`
* `content.pesel`
* `content.krz_signature`
* `content.msig_signature`
* `content.person_name`

Przy tworzeniu filtra należy przekazać nazwę użytego klucza w parametrze `crypto_key_name`.
