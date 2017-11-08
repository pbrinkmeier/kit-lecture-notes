# Mitmachen

Mitarbeit ist natürlich willkommen, aber bitte bleibt mit dem Rest der Mitschriebe konsistent.

## Inhalt

- [Styleguide für Markdown](#styleguide-für-markdown)
    - [Vorlage](#vorlage)
    - [Überschriften](#überschriften)
    - [Absätze](#absätze)
    - [Listen](#listen)
    - [Wichtige Begriffe](#wichtige-begriffe)
    - [Betonung](#betonung)
    - [Korrekte Zeichen](#korrekte-zeichen)
        - [Anführungszeichen](#anführungszeichen)
        - [Apostroph](#apostroph)
        - [Gedankenstrich/Dash](#gedankenstrichdash)

## Styleguide für Markdown

### Vorlage

```
[zurück](README.md)

# [VL-Nummer]:[Titel]

> [Datum DD.MM.YYYY]

## Table of Contents

[Inhaltsverzeichnis]

## Thema 1

## Thema 2

…
```

- **[VL-Nummer]**: Laufende Nummer der VL (mit führender Null)
- **[Inhaltsverzeichnis]**: Von `toc_generator.py [deine Datei]` generiertes Inhaltsverzeichnis

### Überschriften

```
# Dokumenttitel (Überschrift erster Ordnung)
## Überschrift zweiter Ordnung
### Überschrift dritter Ordnung
#### Überschrift vierter Ordnung
```

- Keine Überschriften vierter oder fünfter Ordnung
    - Dann lieber umstrukturieren
- Keine „Fake-Überschriften“ in Form von fettem Text

### Absätze

Jeder Satz kommt in seine eigene Zeile.
Dadurch sind die Diffs schöner und man kann sie besser bearbeiten.
Mehrere Leerzeichen/Zeilenumbrüche fallen in HTML zu einem Leerzeichen zusammen.

```
Jeder Satz kommt in seine eigene Zeile.
Dadurch sind die Diffs schöner und man kann sie besser bearbeiten.
Mehrere Leerzeichen/Zeilenumbrüche fallen in HTML zu einem Leerzeichen zusammen.
```

- Will man einen Zeilenumbruch durch Markdown erzwingen, beendet man die vorhergehende Zeile mit zwei Leerzeichen

### Listen

- Mein
- kleiner
    - eingerückter
- Kaktus

```
- Mein
- kleiner
    - eingerückter
- Kaktus
```

- Führendes Zeichen: immer `-`

### Wichtige Begriffe

Wichtige Begriffe werden mit **Fettschrift** markiert.

```
Wichtige Begriffe werden mit **Fettschrift** markiert.
```

- Nicht `__Unterstriche__`, sondern `**Sternchen**`
- Satzzeichen gehören nicht zum Begriff
    - **Beispiel**: `**Beispiel**:`
- Nein, kursiver Text ist für Betonung reserviert
    - Beispiel: Der **Stack** wächst unter x86 *nach unten*

### Betonung

Betonung wird durch *Kursivschrift* erreicht.

```
Betonung wird durch *Kursivschrift* erreicht.
```

- Nicht `_Unterstriche_`, sondern `*Sternchen*`
- Satzzeichen werden nicht betont
- Nein, fetter Text ist für wichtige Begriffe reserviert
    - Beispiel: Der **Stack** wächst unter x86 *nach unten*

### Korrekte Zeichen

Zum rauskopieren:

# `„ “ ” — ’ …`

# ≠ ≤ ≥

#### Anführungszeichen

Falsch:

```"Lorem ipsum dolor sit amet"```

Richtig (englische Texte):

```“Lorem ipsum dolor sit amet”```

Richtig (deutsche Texte):

```„Lorem ipsum dolor sit amet”```

#### Apostroph

Falsch:

```It's certain.```

Richtig:

```It’s certain.```

#### Gedankenstrich/Dash

Falsch:

```Der Stack - nach unten wachsend - ist nicht unendlich groß.```

Richtig:

```Der Stack — nach unten wachsend — ist nicht unendlich groß.```
