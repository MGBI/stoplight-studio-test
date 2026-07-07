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
Aby zapewnić bezpieczeństwo składowanych danych, możliwe jest tworzenie filtrów
z zaszyfrowanymi po stronie klienta wartościami.

W tym celu, skontaktuj się z obsługą klienta, by w bezpieczny sposób podać
następujące informacje:
* crypto_key_name - unikalna nazwa klucza (nadana przez użytkownika)
* crypto_key - klucz kryptograficzny (AES) lub klucz publiczny (RSA)
* crypto_algorithm - pełna nazwa algorytmu kryptograficznego, np. AES-256-GCM lub RSA-OAEP-SHA256

Podane wartości muszą być zgodne z algorytmem wykorzystanym przy szyfrowaniu
wartości na listach:
`content.nip`,
`content.regon`,
`content.krs`,
`content.pesel`,
`content.krz_signature`,
`content.msig_signature`,
`content.person_name`.

Przy tworzeniu filtra należy przekazać nazwę użytego klucza w parametrze `crypto_key_name`.
