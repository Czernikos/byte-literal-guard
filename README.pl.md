# byte-literal-guard 🐿️

[English](README.md) | **Polski**

Mały, pozbawiony zewnętrznych zależności **eksperymentalny sprawdzian wstępny**, który wykrywa bezpośrednio zapisane znaki nie-ASCII w bajtowych literałach Pythona.

Autorka: **Kartografka**, asystentka AI współpracująca z **Czernikosem** w Planeta Gaja.

Nie usuwa polskich znaków ze zwykłych napisów i nie poprawia kodu za Ciebie.

## Co sprawdza

```python
# Zgłaszane:
payload = b"żółw"

# Akceptowane przez ten wąski sprawdzian:
payload = "żółw".encode("utf-8")
payload = b"\xc5\xbc\xc3\xb3\xc5\x82w"
text = "żółw"
```

Skaner korzysta z modułu `tokenize` Pythona i sprawdza tokeny napisów z prefiksem bajtowym. Czyta kod źródłowy bez importowania go ani wykonywania. Zgłasza ścieżki plików i numery początkowych wierszy tokenów, liczone od 1; diagnostyka nie zawiera tekstu źródłowego.

## Uruchomienie

Bez instalacji i zewnętrznych zależności:

```sh
python3 -B byte_literal_guard.py path/to/project another_file.py
python3 -B -m unittest discover -s tests -v
```

Katalogi są przeszukiwane rekurencyjnie w poszukiwaniu `*.py`; przy takim przeszukiwaniu pomijane są `.git`, `.venv` i `__pycache__`. Jawnie wskazane pliki `.py` są sprawdzane także wewnątrz tych katalogów. Deklaracje kodowania Pythona i znacznik UTF-8 BOM są odczytywane przez `tokenize.open`.

Kody zakończenia:

- **0:** sprawdzono przynajmniej jeden plik Pythona i nie znaleziono pasującego literału.
- **1:** znaleziono pasujący literał.
- **2:** błąd użycia, wejścia, dekodowania lub tokenizacji albo brak wybranych plików Pythona.

Zgłaszany jest początkowy wiersz tokenu, nawet jeśli niedozwolony znak znajduje się dalej w wielowierszowym literale. Błędy zatrzymują skanowanie; narzędzie nie zbiera wyczerpującej listy wszystkich błędów.

## Ważne ograniczenia

**To nie jest walidator składni Pythona, skaner bezpieczeństwa ani ogólny linter.** Kod zakończenia 0 nie oznacza, że program się kompiluje lub jest bezpieczny. Osobno uruchom kompilator swojego interpretera i zwykłe testy.

Dokumentacja Pythona określa tokenizację kodu niepoprawnego składniowo jako zachowanie niezdefiniowane. Literały, które to narzędzie ma wykrywać, same są niepoprawną składnią Pythona: wykrywanie jest zatem **udogodnieniem sprawdzonym na interpreterze wskazanym poniżej, a nie przenośną gwarancją parsera**. Uszkodzona lub nowsza składnia, w tym zagnieżdżone wyrażenia w nowszych f-stringach, pozostaje poza sprawdzonym zakresem. Nie używaj tego jako jedynego warunku przejścia CI.

Lokalne testy wykonano na **CPythonie 3.9.6, macOS**: 14 metod unittest, w tym 18 podprzypadków literałów. Obejmują prefiksy, literały wielowierszowe, sekwencje ucieczki, tekst i komentarze Unicode, rekurencję i wykluczenia, brakujące wejścia, brak wybranych plików, dekodowanie, deklarację Latin-1, UTF-8 BOM oraz przypadek niewykonywania kodu. Innych wersji Pythona i systemów operacyjnych nie przetestowano dla tego wydania. Pewne niepoprawne konstrukcje celowo przechodzą ten wąski sprawdzian; test utrwala tę granicę.

Narzędzie nie zmienia plików, nie korzysta z sieci, niczego nie instaluje i nie zbiera telemetrii.

## Pochodzenie i wydanie

Wersja **0.1.0**. Wyodrębniona z małego lokalnego narzędzia z września 2026. W publicznej wersji dodałam jawną obsługę błędów wejścia, odczyt uwzględniający kodowanie, testy i dokumentację. Oryginalne lokalne narzędzie pozostaje niezmienione. Publikacja nie zawiera prywatnych rozmów, lokalnych logów, danych uwierzytelniających ani danych badawczych.

Zobacz [CHANGELOG.md](CHANGELOG.md) i [LICENSE](LICENSE). O naszej współpracy: [Kartografka · Planeta Gaja](https://github.com/Czernikos/kartografka-gaja).

### Źródło

[Dokumentacja `tokenize` Pythona](https://docs.python.org/3/library/tokenize.html) — szczególnie ostrzeżenie dotyczące niepoprawnego kodu i opis `tokenize.open`.
