Interfejs programistyczny serwisu iMSiG.pl umożliwia wyszukiwanie i pobieranie
oryginalnej treści ogłoszeń publikowanych w Monitorze Sądowym i Gospodarczym (MSiG)
oraz w Krajowym Rejestrze Zadłużonych (KRZ), a także wyodrębnionych z nich danych
w ustrukturyzowanej formie.

W obecnej wersji API umożliwia dostęp do ogłoszeń dotyczących postępowań upadłościowych
i restrukturyzacyjnych, pochodzących z numerów MSiG wydanych (od 1 stycznia 2001 r.)
oraz z KRZ (od 1 grudnia 2021 r.).

Informacje o zasadach korzystania z interfejsu dostępne są na stronie usługi [Lista upadłości](https://www.imsig.pl/lista-upadlosci).

Słowa kluczowe:
* Monitor Sądowy i Gospodarczy API (MSIG API)
* Krajowy Rejestr Zadłużonych API (KRZ API)


## Źródło danych
Monitor Sądowy i Gospodarczy (MSiG) to oficjalny dziennik urzędowy, w którym publikowane
są ogłoszenia sądowe m.in. na podstawie przepisów kodeksu spółek handlowych, kodeksu
postępowania cywilnego i prawa upadłościowego. Nowe numery dziennika są udostępniane
codziennie w formie plików PDF na [stronie Ministerstwa Sprawiedliwości](https://ems.ms.gov.pl/msig/przegladaniemonitorow).

Krajowy Rejestr Zadłużonych (KRZ) to system teleinformatyczny Ministerstwa Sprawiedliwości,
w którym gromadzone są wszystkie informacje i dokumenty dotyczące przebiegu postępowań
upadłościowych i restrukturyzacyjnych prowadzonych przez polskie sądy (od 1 grudnia 2021 r.).


## Ustrukturyzowane informacje
Format pliku, w jakim udostępniany jest Monitor Sądowy i Gospodarczy, nie umożliwia
łatwego wyszukiwania ogłoszeń dotyczących poszczególnych osób fizycznych lub podmiotów.
Treść ogłoszeń jest nieustrukturyzowana, co uniemożliwia dalsze przetwarzanie zawartych
w niej informacji.

Nasz interfejs programistyczny umożliwia przeszukiwanie bazy ogłoszeń opublikowanych
w MSiG oraz KRZ na podstawie kilku różnych kryteriów, pobieranie ich oryginalnej wersji w dwóch
formatach, a także dostęp do wybranych informacji wyodrębnionych z tekstowej treści.

Aby sprawdzić, jakie ogłoszenia publikowane są w MSiG, przejdź na [stronę główną serwisu iMSiG.pl](
https://www.imsig.pl).


## Masowy dostęp
Wyszukiwarka ogłoszeń dostępna na stronie Ministerstwa Sprawiedliwości nie jest
przeznaczona do masowego dostępu do bazy ogłoszeń. Nie zostało również
udostępnione oficjalne API do integracji z systemami teleinformatycznymi.

W ramach naszego interfejsu programistycznego udostępniamy szereg kryteriów do
przeszukiwania bazy ogłoszeń dostępnych w systemie KRZ jak i MSiG. Umożliwia to
masowe pobieranie dokumentów bez konieczności ręcznego sprawdzania ogłoszeń
w dwóch różnych systemach.

Dodatkowo, wszystkie udostępniane przez nas ogłoszenia są uzupełniane o pominięte
w publicznym portalu dane doradców restukturyzacyjnych oraz dane rejestrowe
podmiotów, których dotyczą ogłoszenia.