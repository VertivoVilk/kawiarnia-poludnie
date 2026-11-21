#!/usr/bin/env python3
"""Sprawdza plik HTML pod kątem podstawowych problemów dostępności i SEO.

Tylko raportuje znalezione problemy - nic nie naprawia ani nie modyfikuje.

Wykrywane problemy:
  - obrazki (<img>) bez atrybutu alt
  - puste linki (<a> bez href, z href="" lub href="#")
  - brak znacznika <title> lub pusty <title>
  - brak <meta name="description"> lub pusta wartość content
  - nieprawidłowa kolejność nagłówków (więcej niż jeden <h1>,
    przeskoki poziomów np. h2 -> h4)

Użycie:
  python3 check_html.py sciezka/do/pliku.html
"""

import argparse
import sys
from html.parser import HTMLParser


HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


def attrs_to_dict(attrs):
    return {name: (value if value is not None else "") for name, value in attrs}


def describe_tag(tag, attrs_dict, max_len=70):
    """Krótki, czytelny podgląd znacznika do raportu (bez pełnej treści)."""
    parts = [f"<{tag}"]
    for key in ("src", "href", "class", "id"):
        if key in attrs_dict:
            parts.append(f' {key}="{attrs_dict[key]}"')
    snippet = "".join(parts) + ">"
    if len(snippet) > max_len:
        snippet = snippet[: max_len - 1] + "…"
    return snippet


class HtmlAuditor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images_without_alt = []
        self.empty_links = []
        self.headings = []  # (line, level, snippet)
        self.title_found = False
        self.title_text = ""
        self.title_line = None
        self._in_title = False
        self.meta_description_found = False
        self.meta_description_empty = False

    def handle_starttag(self, tag, attrs):
        line, _col = self.getpos()
        attrs_dict = attrs_to_dict(attrs)

        if tag == "img":
            if "alt" not in attrs_dict:
                self.images_without_alt.append((line, describe_tag(tag, attrs_dict)))

        elif tag == "a":
            href = attrs_dict.get("href")
            if href is None:
                self.empty_links.append((line, "brak atrybutu href", describe_tag(tag, attrs_dict)))
            elif href.strip() == "":
                self.empty_links.append((line, 'pusty href=""', describe_tag(tag, attrs_dict)))
            elif href.strip() == "#":
                self.empty_links.append((line, 'href="#" (nie prowadzi nigdzie)', describe_tag(tag, attrs_dict)))

        elif tag == "title":
            self.title_found = True
            self.title_line = line
            self._in_title = True

        elif tag == "meta":
            name = (attrs_dict.get("name") or "").strip().lower()
            if name == "description":
                content = (attrs_dict.get("content") or "").strip()
                self.meta_description_found = True
                if not content:
                    self.meta_description_empty = True

        elif tag in HEADING_TAGS:
            level = int(tag[1])
            self.headings.append((line, level, describe_tag(tag, attrs_dict)))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title_text += data


def check_headings(headings):
    """Zwraca listę problemów z kolejnością nagłówków."""
    problems = []

    h1_lines = [line for line, level, _snippet in headings if level == 1]
    if len(h1_lines) > 1:
        lines_str = ", ".join(str(l) for l in h1_lines)
        problems.append(
            f"Więcej niż jeden <h1> na stronie (linie: {lines_str}) - "
            "strona powinna mieć dokładnie jeden główny nagłówek h1."
        )

    previous_level = None
    for line, level, snippet in headings:
        if previous_level is not None and level - previous_level > 1:
            problems.append(
                f"Linia {line}: przeskok z <h{previous_level}> do <h{level}> "
                f"(pominięto poziom pośredni) - {snippet}"
            )
        previous_level = level

    return problems


def run_audit(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        print(f"Nie udało się otworzyć pliku: {e}", file=sys.stderr)
        sys.exit(1)

    auditor = HtmlAuditor()
    auditor.feed(content)
    auditor.close()

    sections = []

    if auditor.images_without_alt:
        lines = [f'  - Linia {line}: {snippet} - brak atrybutu alt' for line, snippet in auditor.images_without_alt]
        sections.append(("Obrazki bez atrybutu alt", lines))

    if auditor.empty_links:
        lines = [f"  - Linia {line}: {reason} - {snippet}" for line, reason, snippet in auditor.empty_links]
        sections.append(("Puste linki", lines))

    title_problems = []
    if not auditor.title_found:
        title_problems.append("  - Brak znacznika <title> w <head>.")
    elif not auditor.title_text.strip():
        title_problems.append(f"  - Linia {auditor.title_line}: <title> jest puste.")
    if title_problems:
        sections.append(("Tytuł strony", title_problems))

    meta_problems = []
    if not auditor.meta_description_found:
        meta_problems.append('  - Brak znacznika <meta name="description" content="...">.')
    elif auditor.meta_description_empty:
        meta_problems.append('  - <meta name="description"> istnieje, ale content jest puste.')
    if meta_problems:
        sections.append(("Meta description", meta_problems))

    heading_problems = check_headings(auditor.headings)
    if heading_problems:
        sections.append(("Kolejność nagłówków", [f"  - {p}" for p in heading_problems]))

    print(f"Sprawdzanie: {path}\n")

    if not sections:
        print("Brak problemów - strona wygląda dobrze pod kątem sprawdzanych reguł.")
        return

    total = 0
    for title, lines in sections:
        print(f"[{title}]")
        for line in lines:
            print(line)
            total += 1
        print()

    print(f"Podsumowanie: znaleziono {total} problem(ów) w {len(sections)} kategoriach.")
    print("Ten skrypt tylko raportuje - żadne pliki nie zostały zmienione.")


def main():
    parser = argparse.ArgumentParser(description="Sprawdza plik HTML pod kątem podstawowych problemów dostępności/SEO.")
    parser.add_argument("path", help="Ścieżka do pliku HTML do sprawdzenia")
    args = parser.parse_args()
    run_audit(args.path)


if __name__ == "__main__":
    main()
