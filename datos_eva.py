"""DANE EVA (Evaluaciones Agropecuarias Municipales) dataset — embedded.

Three Colombian agricultural products with national production data
from datos.gov.co resources 2pnw-mmge (2007-2018) and uejq-wxrr (2019-2025).
Combined series: 19 years per product with consistent metrics.
"""

DATA_SOURCE = {
    "dataset": "Evaluaciones Agropecuarias Municipales (EVA)",
    "entity": "DANE — Departamento Administrativo Nacional de Estadística",
    "url": "https://www.datos.gov.co",
    "resource_ids": ["2pnw-mmge", "uejq-wxrr"],
    "date_range": "2007–2025",
}

PRODUCT_NAMES = ["Café", "Arroz", "Plátano"]

_RAW = {
    "Café": {
        "years":          [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
                           2019, 2020, 2021, 2022, 2023, 2024, 2025],
        "production":     [828904, 828602, 708904, 779257, 640451, 626798, 652054, 728384, 850503, 853913, 851641, 855836,
                           876134, 791957, 754936, 669858, 681169, 833038, 820825],
        "area_sown":      [860244, 866719, 873376, 884505, 922512, 956784, 974100, 948487, 940876, 931750, 903951, 884285,
                           859612, 850191, 841753, 844073, 839549, 838961, 836079],
        "area_harvested": [766481, 758317, 754655, 744333, 712391, 710472, 771794, 795574, 801085, 777711, 753304, 742378,
                           697030, 716693, 695782, 699036, 697815, 671193, 652635],
    },
    "Arroz": {
        "years":          [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
                           2019, 2020, 2021, 2022, 2023, 2024, 2025],
        "production":     [2539719, 2831154, 2840704, 2363902, 2430074, 2570093, 2529986, 2177749, 2598599, 3267216, 3249045, 1980800,
                           3450968, 3945779, 3710346, 3639396, 3630138, 3722845, 3774140],
        "area_sown":      [457023, 518768, 566276, 523167, 541939, 542256, 558908, 458664, 552258, 661654, 685138, 397970,
                           642616, 703661, 688868, 671851, 678980, 711375, 699133],
        "area_harvested": [443568, 506818, 551974, 471615, 527014, 533822, 547267, 443264, 529661, 638685, 667606, 397970,
                           633121, 693845, 640909, 641061, 648181, 679091, 692208],
    },
    "Plátano": {
        "years":          [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
                           2019, 2020, 2021, 2022, 2023, 2024, 2025],
        "production":     [2968116, 2726564, 2744224, 2976687, 3001195, 3218822, 3353156, 3477897, 3542371, 3909044, 4111721, 4430175,
                           4094459, 4310256, 4387886, 4647793, 4835609, 5012254, 5360673],
        "area_sown":      [413030, 398163, 420398, 424464, 422636, 447333, 447548, 448904, 448969, 475079, 474632, 511698,
                           447913, 466922, 470708, 475507, 484837, 490021, 494624],
        "area_harvested": [375685, 357779, 351462, 370641, 375649, 397258, 398453, 401747, 405923, 416072, 415964, 434098,
                           409382, 431668, 441615, 445415, 454434, 459536, 476527],
    },
}


def get_product_data(product_name: str) -> dict:
    """Return data dict for one product.

    Keys: name, years, production, area_sown, area_harvested, yield_per_ha.
    """
    if product_name not in _RAW:
        raise ValueError(
            f"Unknown product '{product_name}'. Choose from: {PRODUCT_NAMES}"
        )
    raw = _RAW[product_name]
    yield_per_ha = [
        p / a for p, a in zip(raw["production"], raw["area_harvested"])
    ]
    return {
        "name": product_name,
        "years": list(raw["years"]),
        "production": list(raw["production"]),
        "area_sown": list(raw["area_sown"]),
        "area_harvested": list(raw["area_harvested"]),
        "yield_per_ha": yield_per_ha,
    }
