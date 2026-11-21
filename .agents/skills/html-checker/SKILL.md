---
name: html-checker
description: Sprawdza plik HTML pod kątem podstawowych problemów dostępności i SEO — obrazków bez atrybutu alt, pustych linków (brak href, href="" lub href="#"), brakującego <title>, brakującego <meta name="description">, oraz nieprawidłowej kolejności nagłówków (kilka <h1>, przeskoki poziomów jak h2 -> h4). Wypisuje tylko listę znalezionych problemów z numerami linii — nic nie naprawia i nie modyfikuje pliku. Użyj tego skilla zawsze, gdy użytkownik prosi o sprawdzenie, zaudytowanie, zweryfikowanie lub "code review" strony HTML/landing page pod kątem dostępności, SEO albo podstawowej jakości, także gdy pyta ogólnie "czy z tą stroną wszystko ok", "sprawdź mój html", "czy mam gdzieś brakujące alt teksty", albo przed opublikowaniem/wysłaniem strony klientowi.
---

# HTML Checker

Lekki, deterministyczny audytor plików HTML. Sprawdza pięć konkretnych,
obiektywnie weryfikowalnych rzeczy i **tylko je wypisuje** — nigdy nie
edytuje, nie naprawia i nie sugeruje konkretnych poprawek w kodzie. Decyzję
co i jak naprawić zostawia użytkownikowi (albo osobnej, świadomej prośbie).

To rozróżnienie ma znaczenie: ten skill służy do szybkiej diagnozy "co jest
nie tak", nie do automatycznych poprawek. Jeśli użytkownik chce też naprawić
znalezione problemy, zapytaj go o to wprost i wtedy wykonaj zmiany osobno —
nie rób tego przy okazji uruchamiania tego skilla.

## Jak używać

Uruchom skrypt na wskazanym pliku HTML:

```bash
python3 scripts/check_html.py sciezka/do/pliku.html
```

Skrypt nie ma żadnych zależności poza standardową biblioteką Pythona
(używa `html.parser`), więc działa od razu na dowolnym systemie z Pythonem 3.

Pokaż użytkownikowi wynik działania skryptu (stdout) w takiej formie, w jakiej
go wypisuje — jest już czytelnie pogrupowany po kategoriach z numerami linii
i podsumowaniem na końcu. Nie przepisuj go własnymi słowami i nie skracaj
listy problemów — to zafałszowuje audyt.

## Co dokładnie jest sprawdzane

1. **Obrazki bez `alt`** — każdy `<img>`, w którym atrybut `alt` w ogóle nie
   występuje. (Puste `alt=""` jest celowo pomijane — to poprawny sposób
   oznaczenia obrazka czysto dekoracyjnego, więc nie jest to błąd).
2. **Puste linki** — każdy `<a>`, który nie ma atrybutu `href`, ma
   `href=""`, albo `href="#"` (czyli nigdzie nie prowadzi).
3. **Tytuł strony** — brak znacznika `<title>` albo `<title>` bez treści.
4. **Meta description** — brak `<meta name="description" content="...">`
   albo `content` jest puste.
5. **Kolejność nagłówków** — więcej niż jeden `<h1>` na stronie, oraz
   przeskoki poziomów w kolejności występowania nagłówków (np. `<h2>` od
   razu do `<h4>`, z pominięciem `<h3>`).

Te reguły celowo nie próbują ocenić jakości treści ani stylu — to twarde,
mechaniczne sprawdzenia, które albo się zgadzają, albo nie. Dzięki temu
wynik jest powtarzalny i nie wymaga oceny "na oko".

## Jeśli plik nie jest podany

Jeśli użytkownik poprosi o sprawdzenie strony, ale nie poda ścieżki do
pliku, poszukaj w bieżącym katalogu roboczym pliku `.html` (najczęściej
`index.html`) zamiast pytać od razu — zapytaj tylko, jeśli jest ich kilka
i nie da się jednoznacznie zgadnąć, o który chodzi.
