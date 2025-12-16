
# Copyright (c) 2025 Juho Tiihonen
# License: MIT

"""Raporttien muotoilu (Viikko6).

Muodostaa raporttirivit päivä-, kuukausi- ja vuositasolle.
"""

from datetime import date
from typing import Dict, List, Tuple

FI_WEEKDAYS = [
    "maanantai", "tiistai", "keskiviikko",
    "torstai", "perjantai", "lauantai", "sunnuntai"
]


def _fmt(x: float) -> str:
    """Kahden desimaalin muoto + pilkku desimaalina."""
    return f"{x:.2f}".replace(".", ",")


def _pvm(d: date) -> str:
    """Muodostaa muodon dd.mm.yyyy."""
    return f"{d.day}.{d.month}.{d.year}"


def raportti_paivavalilta(paivat: Dict[date, Dict[str, float]],
                          alku: date, loppu: date) -> List[str]:
    """Muodostaa raportin päiväyhteenvetona annetulta aikaväliltä."""
    if alku > loppu:
        alku, loppu = loppu, alku
    valitut = {d: v for d, v in paivat.items() if alku <= d <= loppu}
    total_kul = sum(v["kulutus"] for v in valitut.values())
    total_tuo = sum(v["tuotanto"] for v in valitut.values())
    avg_temp = (sum(v["lampotila"] for v in valitut.values()) / max(len(valitut), 1)) if valitut else 0.0
    netto = total_kul - total_tuo

    ots = f"Päiväkohtainen yhteenveto: {_pvm(alku)}–{_pvm(loppu)}"
    rivit: List[str] = [
        ots,
        "-" * len(ots),
        "Päivä        Pvm           Kulutus [kWh]  Tuotanto [kWh]  Lämpötila [°C]",
    ]
    for d in sorted(valitut.keys()):
        v = valitut[d]
        wd = FI_WEEKDAYS[d.weekday()]
        rivit.append(
            f"{wd:<12} {_pvm(d):<12}  "
            f"{_fmt(v['kulutus']):>13} {_fmt(v['tuotanto']):>15} {_fmt(v['lampotila']):>14}"
        )
    rivit += [
        "",
        f"Yhteensä kulutus:  {_fmt(total_kul)} kWh",
        f"Yhteensä tuotanto: {_fmt(total_tuo)} kWh",
        f"Nettokuorma:       {_fmt(netto)} kWh",
        f"Keskilämpötila:    {_fmt(avg_temp)} °C",
    ]
    return rivit


def raportti_kuukausi(kkdata: Dict[Tuple[int, int], Dict[str, float]], kuukausi: int) -> List[str]:
    """Muodostaa kuukauden yhteenvedon annetulle kuukaudelle (1–12)."""
    key = (2025, kuukausi)
    v = kkdata.get(key, {"kulutus": 0.0, "tuotanto": 0.0, "lampotila": 0.0})
    netto = v["kulutus"] - v["tuotanto"]
    ots = f"Kuukausiyhteenveto: {kuukausi}/2025"
    return [
        ots,
        "-" * len(ots),
        f"Kokonaiskulutus:   {_fmt(v['kulutus'])} kWh",
        f"Kokonaistuotanto:  {_fmt(v['tuotanto'])} kWh",
        f"Nettokuorma:       {_fmt(netto)} kWh",
        f"Keskilämpötila:    {_fmt(v['lampotila'])} °C",
    ]


def raportti_vuosi(vuosi: Dict[str, float]) -> List[str]:
    """Muodostaa vuoden kokonaisyhteenvedon (2025)."""
    netto = vuosi["kulutus"] - vuosi["tuotanto"]
    ots = "Vuoden 2025 kokonaisyhteenveto"
    return [
        ots,
        "-" * len(ots),
        f"Kokonaiskulutus:   {_fmt(vuosi['kulutus'])} kWh",
        f"Kokonaistuotanto:  {_fmt(vuosi['tuotanto'])} kWh",
        f"Nettokuorma:       {_fmt(netto)} kWh",
        f"Keskilämpötila:    {_fmt(vuosi['lampotila'])} °C",
    ]
