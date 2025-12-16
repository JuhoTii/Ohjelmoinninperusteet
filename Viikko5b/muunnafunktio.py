"""Muuntaa CSV-rivit päivä- ja viikkosummiksi, sekä muodostaa raporttirivit."""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

FI_WEEKDAYS = [
    "maanantai", "tiistai", "keskiviikko",
    "torstai", "perjantai", "lauantai", "sunnuntai"
]


def muunna_data(rivit: List[Dict[str, str]]) -> Dict[str, List[float]]:
    """Ryhmittelee datan päivittäin ja laskee summat (Wh -> kWh, 2 desimaalia).

    Palauttaa:
        dict: { 'dd.mm.YYYY': [kul_v1, kul_v2, kul_v3, tuo_v1, tuo_v2, tuo_v3] }
              arvot kWh-yksikössä kahden desimaalin tarkkuudella.
    """
    paivat: Dict[str, List[float]] = defaultdict(lambda: [0, 0, 0, 0, 0, 0])

    for r in rivit:
        aika = r.get("Aika")
        if not aika:
            continue
        # Päivä avaimena muodossa dd.mm.YYYY
        pvm = datetime.fromisoformat(aika).strftime("%d.%m.%Y")

        sarakkeet = [
            "Kulutus vaihe 1 Wh", "Kulutus vaihe 2 Wh", "Kulutus vaihe 3 Wh",
            "Tuotanto vaihe 1 Wh", "Tuotanto vaihe 2 Wh", "Tuotanto vaihe 3 Wh",
        ]
        for i, s in enumerate(sarakkeet):
            try:
                paivat[pvm][i] += int(r.get(s, 0))
            except (TypeError, ValueError):
                # Jos puuttuu tai ei numeroa -> ohitetaan (käsitellään nollana)
                pass

    # Wh -> kWh ja pyöristys 2 desimaaliin
    for pvm in paivat:
        paivat[pvm] = [round(x / 1000, 2) for x in paivat[pvm]]

    return dict(paivat)


def _fmt(x: float) -> str:
    """Kahden desimaalin muoto + pilkku desimaalina."""
    return f"{x:.2f}".replace(".", ",")


def _parse_pvm(pvm_str: str) -> datetime:
    """Jäsentää 'dd.mm.YYYY' -> datetime."""
    return datetime.strptime(pvm_str, "%d.%m.%Y")


def muodosta_viikkoraporttirivit(paivat: Dict[str, List[float]]) -> List[str]:
    """Muotoilee raporttirivit viikkokohtaisilla otsikoilla ja taulukolla (41–43)."""
    # Ryhmittele viikoiksi
    weeks: Dict[int, Dict[Tuple[str, str], List[float]]] = defaultdict(dict)
    for pvm_str, vals in paivat.items():
        dt = _parse_pvm(pvm_str)
        week = dt.isocalendar()[1]
        weekday = FI_WEEKDAYS[dt.weekday()]
        weeks[week][(weekday, pvm_str)] = vals

    rivit: List[str] = []

    for week in sorted(weeks.keys()):
        # Tulostetaan vain viikot 41–43 (tehtävänanto)
        if week not in (41, 42, 43):
            continue

        rivit.append(
            f"Viikon {week} sähkönkulutus ja -tuotanto (kWh, vaiheittain)")
        rivit.append(
            "Päivä        Pvm           Kulutus [kWh]                   Tuotanto [kWh]")
        rivit.append(
            "                               v1      v2      v3         v1      v2      v3")
        rivit.append("-" * 77)

        items = list(weeks[week].items())
        items.sort(key=lambda kv: _parse_pvm(kv[0][1]))

        for (weekday, pvm_str), vals in items:
            v1, v2, v3, t1, t2, t3 = vals
            kul = f"{_fmt(v1):>7} {_fmt(v2):>7} {_fmt(v3):>7}"
            tuo = f"{_fmt(t1):>7} {_fmt(t2):>7} {_fmt(t3):>7}"
            rivit.append(f"{weekday:<12} {pvm_str:<12}  {kul:<25} {tuo}")

        rivit.append("")  # tyhjä rivi viikkojen väliin

    # (Valinnainen) Kokonaissummat viikoista 41–43
    total = [0.0]*6
    for week, data in weeks.items():
        if week not in (41, 42, 43):
            continue
        for vals in data.values():
            for i in range(6):
                total[i] += vals[i]

    if any(total):
        v1, v2, v3, t1, t2, t3 = total
        rivit.append("Yhteensä (viikot 41–43):")
        rivit.append(
            f"{'':<12} {'':<12}  "
            f"{_fmt(v1):>7} {_fmt(v2):>7} {_fmt(v3):>7}    "
            f"{_fmt(t1):>7} {_fmt(t2):>7} {_fmt(t3):>7}"
        )

    return rivit

# Yhteensopivuus: jos main.py käyttää vanhaa nimeä


def muodosta_raporttirivit(paivat: Dict[str, List[float]]) -> List[str]:
    """Alias vanhalle nimelle: palauttaa viikkoraporttirivit."""
    return muodosta_viikkoraporttirivit(paivat)
