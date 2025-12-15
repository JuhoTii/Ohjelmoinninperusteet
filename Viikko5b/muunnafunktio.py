
"""Muuntaa CSV-rivit päiväsummiksi ja muotoilee raporttirivit."""
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

FI_WEEKDAYS = [
    "maanantai", "tiistai", "keskiviikko",
    "torstai", "perjantai", "lauantai", "sunnuntai"
]

def _paiva_avain(aika_str: str) -> Tuple[str, str]:
    """Palauttaa avaimen (viikonpäivä, pvm) annetusta ISO-aikaleimasta."""
    dt = datetime.fromisoformat(aika_str)
    paiva = FI_WEEKDAYS[dt.weekday()]
    pvm_str = dt.strftime("%d.%m.%Y")
    return (paiva, pvm_str)

def muunna_data(rivit: List[Dict[str, str]]) -> Dict[Tuple[str, str], List[float]]:
    """Ryhmittelee datan päivittäin ja laskee summat (Wh -> kWh, 2 desimaalia)."""
    paivat: Dict[Tuple[str, str], List[float]] = defaultdict(lambda: [0, 0, 0, 0, 0, 0])

    def _to_int(val) -> int:
        try:
            return int(val)
        except (TypeError, ValueError):
            return 0

    for r in rivit:
        # Jos rivistä puuttuu Aika, ohitetaan
        if "Aika" not in r or not r["Aika"]:
            continue
        key = _paiva_avain(r["Aika"])
        paivat[key][0] += _to_int(r.get("Kulutus vaihe 1 Wh", 0))
        paivat[key][1] += _to_int(r.get("Kulutus vaihe 2 Wh", 0))
        paivat[key][2] += _to_int(r.get("Kulutus vaihe 3 Wh", 0))
        paivat[key][3] += _to_int(r.get("Tuotanto vaihe 1 Wh", 0))
        paivat[key][4] += _to_int(r.get("Tuotanto vaihe 2 Wh", 0))
        paivat[key][5] += _to_int(r.get("Tuotanto vaihe 3 Wh", 0))

    # Muunna Wh -> kWh ja pyöristä kahteen desimaaliin
    for key in list(paivat.keys()):
        paivat[key] = [round(x / 1000, 2) for x in paivat[key]]

    return dict(paivat)

def muodosta_raporttirivit(paivat: Dict[Tuple[str, str], List[float]]) -> List[str]:
    """Muotoilee tekstirivit raporttiin (ilman ANSI-värejä)."""
    otsikko = "Viikot 41–43: sähkönkulutus ja -tuotanto (kWh, vaiheittain)"
    header = (
        f"{otsikko}\n\n"
        f"{'Päivä':<12} {'Pvm':<12}  {'Kulutus [kWh]':<28} {'Tuotanto [kWh]':<22}\n"
        f"{'':<12} {'':<12}  {'v1':>8} {'v2':>8} {'v3':>8}    {'v1':>8} {'v2':>8} {'v3':>8}\n"
        + "-" * 90
    )
    rivit: List[str] = [header]

    def _parse_pvm(pvm: str):
        return datetime.strptime(pvm, "%d.%m.%Y")

    for (paiva, pvm) in sorted(paivat.keys(), key=lambda k: _parse_pvm(k[1])):
        arvot = paivat[(paiva, pvm)]
        kulutus = [f"{x:.2f}".replace(".", ",") for x in arvot[:3]]
        tuotanto = [f"{x:.2f}".replace(".", ",") for x in arvot[3:]]
        rivi = (
            f"{paiva:<12} {pvm:<12}  "
            f"{kulutus[0]:>8} {kulutus[1]:>8} {kulutus[2]:>8}    "
            f"{tuotanto[0]:>8} {tuotanto[1]:>8} {tuotanto[2]:>8}"
        )
        rivit.append(rivi)

    # Loppuun kokonaissummat
    if paivat:
        total = [0, 0, 0, 0, 0, 0]
        for arvot in paivat.values():
            for i in range(6):
                total[i] += arvot[i]
        total = [f"{x:.2f}".replace(".", ",") for x in total]
        rivit.append("")
        rivit.append("Yhteensä:")
        rivit.append(
            f"{'':<12} {'':<12}  {total[0]:>8} {total[1]:>8} {total[2]:>8}    "
            f"{total[3]:>8} {total[4]:>8} {total[5]:>8}"
        )

    return rivit

