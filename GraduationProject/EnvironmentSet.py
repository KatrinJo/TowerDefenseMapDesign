data = {
    "Map": {
        "mapHeight": 10,
        "mapWidth": 10,
        "mapStart": [ 0, 0 ],
        "mapEnd": [ 9, 9 ]
    },
    "Road": [
            [ 0, 0 ],
            [ 0, 1 ],
            [ 1, 1 ],
            [ 1, 2 ],
            [ 1, 3 ],
            [ 2, 3 ],
            [ 3, 3 ],
            [ 4, 3 ],
            [ 4, 4 ],
            [ 5, 4 ],
            [ 6, 4 ],
            [ 6, 5 ],
            [ 6, 6 ],
            [ 6, 7 ],
            [ 6, 8 ],
            [ 7, 8 ],
            [ 7, 9 ],
            [ 8, 9 ],
            [ 9, 9 ]
    ],
    "EnemyTypeNum": 3,
    "Enemy": {
        "1": {
            "eHP": 30,
            "eSpeed": 1,
            "eReward": 28
        },
        "2": {
            "eHP": 20,
            "eSpeed": 2,
            "eReward": 56
        },
        "3": {
            "eHP": 800,
            "eSpeed": 0.5,
            "eReward": 98
        }
    },
    "EnemyWave": {
        "1": [ 2, 1, 0 ],
        "2": [ 1, 3, 0 ],
        "3": [ 2, 2, 1 ],
        "4": [ 2, 3, 1 ],
        "5": [ 0, 3, 0 ],
        "6": [ 0, 3, 2 ],
        "7": [ 0, 4, 3 ],
        "8": [ 0, 4, 5 ],
        "9": [ 2, 3, 7 ],
        "10": [ 2, 5, 10 ]
    },
    "TowerTypeNum": 5,
    "Tower": {
        "1": {
            "tType": "single",
            "tAttack": 24,
            "tPrice": 160,
            "tRange": 2,
            "tFreq": 1,
            "tSlowRate": 1
        },
        "2": {
            "tType": "single",
            "tAttack": 10,
            "tPrice": 100,
            "tRange": 2,
            "tFreq": 1,
            "tSlowRate": 1
        },
        "3": {
            "tType": "pack-round",
            "tAttack": 17,
            "tPrice": 180,
            "tRange": 2,
            "tFreq": 1,
            "tSlowRate": 1
        },
        "4": {
            "tType": "pack-line",
            "tAttack": 12,
            "tPrice": 160,
            "tRange": 3,
            "tFreq": 1,
            "tSlowRate": 1
        },
        "5": {
            "tType": "pack-round",
            "tAttack": 5,
            "tPrice": 180,
            "tRange": 3,
            "tFreq": 0.25,
            "tSlowRate": 0
        }
    },
    "UserInitialWealth": 1000
}