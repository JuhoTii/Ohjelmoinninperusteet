
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

def muunna_data(rivit: List[Dict[str, str]]) -> Dict[str, List[float]]:
    paivat = defaultdict(lambda: [0, 0, 0, 0, 0, 0])
    for r in rivit:
        if not r.get("Aika"):
            continue
        pvm = datetime.fromisoformat(r["Aika"]).strftime("%d.%m.%Y")
        for i, sarake in enumerate([
            "Kulutus vaihe 1 Wh", "Kulutus vaihe 2 Wh", "Kulutus vaihe 3 Wh",
            "Tuotanto vaihe 1 Wh", "Tuotanto vaihe 2 Wh", "Tuotanto vaihe 3 Wh"
        ]):
            try:
                paivat[pvm][i] += int(r.get(sarake, 0))
            except ValueError:
                pass
    # Muunna Wh -> kWh
    for pvm in paivat:
        paivat[pvm] = [round(x / 1000, 2) for x in paivat[pvm]]
    return dict(paivat)

def muodosta_raporttirivit(paivat: Dict[str, List[float]]) -> List[str]:
    rivit = ["Pvm           Kulutus (v1,v2,v3)       Tuotanto (v1,v2,v3)", "-"*60]
    for pvm in sorted(paivat.keys(), key=lambda d: datetime.strptime(d, "%d.%m.%Y")):
        arvot = paivat[pvm]
        kulutus = " ".join(f"{x:.2f}" for x in arvot[:3])
        tuotanto = " ".join(f"{x:.2f}" for x in arvot[3:])
        rivit.append(f"{pvm:<12} {kulutus:<24} {tuotanto}")
    # Yhteensä
    total = [0]*6
    for arvot in paivat.values():
        for i in range(6):
            total[i] += arvot[i]
    rivit.append("\nYhteensä:")
    rivit.append(" ".join(f"{x:.2f}" for x in total))
    return rivit


