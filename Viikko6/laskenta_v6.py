
# Copyright (c) 2025 Juho Tiihonen
# License: MIT

"""Aggregointi- ja laskentafunktiot (Viikko6).

Muodostaa päivä-, kuukausi- ja vuosiyhteenvedot.
"""

from datetime import datetime, date
from typing import Dict, List, Tuple

FI_WEEKDAYS = [
    "maanantai", "tiistai", "keskiviikko",
    "torstai", "perjantai", "lauantai", "sunnuntai"
]


def _parse_iso(aika_str: str) -> datetime:
    """Muuntaa ISO-aikaleiman datetime-olioksi (esim. '2025-10-06T13:00:00')."""
    return datetime.fromisoformat(aika_str)


def _to_float(s: str) -> float:
    """Muuntaa merkkijonon liukuluvuksi (tukee pilkku/piste)."""
    if s is None:
        return 0.0
    s = s.strip().replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def muodosta_paivat(rivit: List[Dict[str, str]]) -> Dict[date, Dict[str, float]]:
    """Laskee päiväkohtaiset summat.

    Palauttaa: {date: {"kulutus": kWh, "tuotanto": kWh, "lampotila": °C}}
    """
    paivat: Dict[date, Dict[str, float]] = {}
    tuntia_per_paiva: Dict[date, int] = {}

    for r in rivit:
        if not r.get("aika"):
            continue
        dt = _parse_iso(r["aika"])
        d = dt.date()
        kul = _to_float(r.get("kulutus", "0"))
        tuo = _to_float(r.get("tuotanto", "0"))
        lam = _to_float(r.get("keskilämpötila", "0"))
        if d not in paivat:
            paivat[d] = {"kulutus": 0.0, "tuotanto": 0.0, "_lam_sum": 0.0}
            tuntia_per_paiva[d] = 0
        paivat[d]["kulutus"] += kul
        paivat[d]["tuotanto"] += tuo
        paivat[d]["_lam_sum"] += lam
        tuntia_per_paiva[d] += 1

    for d in paivat:
        n = max(tuntia_per_paiva.get(d, 0), 1)
        paivat[d]["lampotila"] = paivat[d].pop("_lam_sum") / n
    return paivat


def muodosta_kuukaudet(paivat: Dict[date, Dict[str, float]]) -> Dict[Tuple[int, int], Dict[str, float]]:
    """Aggregoi päivädatasta kuukaudet: (vuosi, kk) -> kulutus, tuotanto, lampotila."""
    kk: Dict[Tuple[int, int], Dict[str, float]] = {}
    paivia: Dict[Tuple[int, int], int] = {}
    for d, v in paivat.items():
        key = (d.year, d.month)
        if key not in kk:
            kk[key] = {"kulutus": 0.0, "tuotanto": 0.0, "_lam_sum": 0.0}
            paivia[key] = 0
        kk[key]["kulutus"] += v["kulutus"]
        kk[key]["tuotanto"] += v["tuotanto"]
        kk[key]["_lam_sum"] += v["lampotila"]
        paivia[key] += 1
    for key in kk:
        n = max(paivia[key], 1)
        kk[key]["lampotila"] = kk[key].pop("_lam_sum") / n
    return kk


def muodosta_vuosi(paivat: Dict[date, Dict[str, float]]) -> Dict[str, float]:
    """Aggregoi koko vuoden: kulutus, tuotanto, lampotila (päiväkeskiarvon keskiarvo)."""
    days = max(len(paivat), 1)
    total_kul = sum(v["kulutus"] for v in paivat.values())
    total_tuo = sum(v["tuotanto"] for v in paivat.values())
    avg_temp = sum(v["lampotila"] for v in paivat.values()) / days

    return {
        "kulutus": total_kul,
        "tuotanto": total_tuo,
        "lampotila": avg_temp,
    }


