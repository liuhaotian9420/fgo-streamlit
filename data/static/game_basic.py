from enum import IntEnum

ATK_MAX_BASE = {"5":11000,
           "4":9000,
           "3":7000,
           "2":6200,
           "1":5500,
           "0":6200}
CLASS_TENDANCY = {
    "classes": ["Saber", "Archer", "Lancer", "Rider", "Caster", "Assassin", "Berserker", "Ruler", "Avenger", "MoonCancer", "Alterego", "Foreigner", "Pretender", "Shielder", "Beast"],
    "HP": {
        "Saber": 1.01,
        "Archer": 0.98,
        "Lancer": 1.02,
        "Rider": 0.96,
        "Caster": 0.98,
        "Assassin": 0.95,
        "Berserker": 0.90,
        "Ruler": 1.00,
        "Avenger": 0.88,
        "Mooncancer": 1.05,
        "Alterego": 0.95,
        "Foreigner": 1.00,
        "Pretender": 0.95,
        "Shielder": 1.01,
        "Beast": 0.97
    },
    "ATK": {
        "Saber": 1.01,
        "Archer": 1.02,
        "Lancer": 0.98,
        "Rider": 0.97,
        "Caster": 0.94,
        "Assassin": 0.96,
        "Berserker": 1.03,
        "Ruler": 0.95,
        "Avenger": 1.05,
        "Mooncancer": 0.94,
        "Alterego": 1.02,
        "Foreigner": 1.00,
        "Pretender": 1.02,
        "Shielder": 0.99,
        "Beast": 1.03,
        "Grandcaster":1.00
    }
}