# arimr2traces
Pobiera dane o zwierzętach ze strony ARiMRu w celu przygotowania świadectw zdrowia w TRACES.

Lekarze weterynarii pracujący w PIW muszą wpisywać świadectwa zdrowia do systemu TRACES,
pobierając dane o zwierzętach, ręcznie wpisując każdy nr kolczyka do systemu Agencji 
Modernizacji i Restrukturyzacji Rolnictwa, i przekopiowując dane z okienka do okienka.

Ten program to upraszcza. Wystarczy wczytać listę nr identyfikacyjnych zwierząt (zwyczajny plik 
tekstowy gdzie każdy z nr zwierząt jest w osobnej linii).
Jeśli dysponuje się loginem i hasłem do systemu ARiMR, program sam pobierze potrzebne
 dane i zapisze je w formacie do wczytania do TRACES, oraz jako arkusz z danymi do wczytania do
 Excela.

