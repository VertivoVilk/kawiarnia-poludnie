# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A single-file static landing page for "Kawiarnia Południe" (a fictional café), written entirely in Polish. There is no build system, no package manager, and no test suite — everything (HTML, CSS, inline SVG icons) lives in `index.html`.

## Commands

There is no build/lint/test tooling. To preview the page, simply open `index.html` in a browser (e.g. `open index.html` on macOS), or serve the directory with any static file server.

## Architecture

- `index.html` — the entire site: a `<style>` block in `<head>` followed by four sections (`hero`/`powitanie`, `about`/`o-nas`, `offer`/`oferta`, footer). Navigation uses in-page anchor links (`#o-nas`, `#oferta`).
- Styling uses CSS custom properties defined on `:root` (`--ink`, `--paper`, `--sun`, `--clay`, `--moss`, plus `--font-display`/`--font-body`/`--font-mono`) — reuse these tokens rather than hardcoding new colors/fonts.
- Fonts are system font stacks (Georgia / system-ui / ui-monospace) defined in `--font-*` tokens — no external font loading.
- Icons and decorative marks are hand-written inline `<svg>` (no icon library/image assets).
- Responsive behavior is handled with two breakpoints (`max-width: 780px`, `max-width: 560px`) and a `prefers-reduced-motion` block that disables animations (`hero-glow` pulse, `steam-wisp` float).

## Design constraints

- Strona trzyma się kremowej palety kolorów — nie wprowadzaj nowych, niepasujących kolorów (np. jaskrawych/neonowych barw).
- Nie używamy żadnych zewnętrznych bibliotek (CSS/JS frameworków, ikon, itp.) — tylko czysty HTML i CSS.

## Skills

This repo has `frontend-design`, `skill-creator`, and `html-checker` skills installed (see `.claude/skills/`, tracked via `skills-lock.json`). Use `html-checker` to audit `index.html` for missing alt text, empty links, missing title/meta description, and heading-order issues before considering edits to the page complete.
