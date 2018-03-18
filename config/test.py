import json
a = {
    "1":  {
        "(5, 5)":3, 
        "(3, 4)":3,
        "(2, 2)":5,
        "(7, 7)":5,
        "(6, 9)":1,
        "(2, 4)":2
    },
    "2": {
        "(0, 2)":2
    },
    "3": {
        "(5, 8)":1
    },
    "4": {
        "(4, 5)":1
    },
    "5": {
        "(5, 3)":5,
        "(6, 3)":4
    },
    "6": {
        "(4, 2)":1,
        "(1, 4)":1
    },
    "7": {
        "(3, 2)":5
    },
    "8": {
        "(1, 0)":1,
        "(2, 1)":1,
        "(5, 6)":1
    },
    "9": {
        "(7, 5)":1,
        "(8, 8)":1,
        "(0, 3)":4
    },
    "10": {
        "(3, 5)":1,
        "(7, 4)":1,
        "(7, 6)":1,
        "(5, 7)":1
    }
}

logs = {
    "log": [
        {},
        {
            "0": {
                "response": a["1"]
            }
        },
        {},
        {
            "0": {
                "response": a["2"]
            }
        },
        {},
        {
            "0": {
                "response": a["3"]
            }
        },
        {},
        {
            "0": {
                "response": a["4"]
            }
        },
        {},
        {
            "0": {
                "response": a["5"]
            }
        },
        {},
        {
            "0": {
                "response": a["6"]
            }
        },
        {},
        {
            "0": {
                "response": a["7"]
            }
        },
        {},
        {
            "0": {
                "response": a["8"]
            }
        },
        {},
        {
            "0": {
                "response": a["9"]
            }
        }
    ]
}
# print(json.dumps(logs))
# for k in a.keys():
#   print(json.dumps(a[k]))

data = {
			"TowerTypeNum": 5,
			"EnemyWave": {
				"1": [
					2,
					1,
					0
				],
				"2": [
					1,
					3,
					0
				],
				"3": [
					2,
					2,
					1
				],
				"4": [
					2,
					3,
					1
				],
				"5": [
					0,
					3,
					0
				],
				"6": [
					0,
					3,
					2
				],
				"7": [
					0,
					4,
					3
				],
				"8": [
					0,
					4,
					5
				],
				"9": [
					2,
					3,
					7
				],
				"10": [
					2,
					5,
					10
				]
			},
			"Map": {
				"mapWidth": 10,
				"mapEnd": [
					9,
					9
				],
				"mapHeight": 10,
				"mapStart": [
					0,
					0
				]
			},
			"EnemyTypeNum": 3,
			"Road": [
				[
					0,
					0
				],
				[
					0,
					1
				],
				[
					1,
					1
				],
				[
					1,
					2
				],
				[
					1,
					3
				],
				[
					2,
					3
				],
				[
					3,
					3
				],
				[
					4,
					3
				],
				[
					4,
					4
				],
				[
					5,
					4
				],
				[
					6,
					4
				],
				[
					6,
					5
				],
				[
					6,
					6
				],
				[
					6,
					7
				],
				[
					6,
					8
				],
				[
					7,
					8
				],
				[
					7,
					9
				],
				[
					8,
					9
				],
				[
					9,
					9
				]
			],
			"Enemy": {
				"1": {
					"eHP": 30,
					"eReward": 28,
					"eSpeed": 1
				},
				"2": {
					"eHP": 20,
					"eReward": 56,
					"eSpeed": 2
				},
				"3": {
					"eHP": 800,
					"eReward": 98,
					"eSpeed": 0.5
				}
			},
			"Tower": {
				"1": {
					"tFreq": 1,
					"tType": "single",
					"tAttack": 24,
					"tPrice": 160,
					"tRange": 2,
					"tSlowRate": 1
				},
				"2": {
					"tFreq": 1,
					"tType": "single",
					"tAttack": 10,
					"tPrice": 100,
					"tRange": 2,
					"tSlowRate": 1
				},
				"3": {
					"tFreq": 1,
					"tType": "pack-round",
					"tAttack": 17,
					"tPrice": 180,
					"tRange": 2,
					"tSlowRate": 1
				},
				"4": {
					"tFreq": 1,
					"tType": "pack-line",
					"tAttack": 12,
					"tPrice": 160,
					"tRange": 3,
					"tSlowRate": 1
				},
				"5": {
					"tFreq": 0.25,
					"tType": "pack-round",
					"tAttack": 5,
					"tPrice": 180,
					"tRange": 3,
					"tSlowRate": 0
				}
			},
			"UserInitialWealth": 1000
		}
tt = {
	"requests": [
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, data
	],
	"responses": [
        {"(3, 4)": 3},
        {"(0, 2)": 3},
		{"(6, 9)": 3, "(7, 7)": 3, "(2, 2)": 5, "(5, 3)": 1},
		{"(6, 3)": 4},
		{"(8, 8)": 2},
		{"(5, 5)": 3},
		{"(4, 5)": 5},
		{"(7, 6)": 1},
		{"(7, 3)": 4},
		{"(2, 1)": 2}
    ]
}

print(json.dumps(tt))





# print(json.dumps(tt))


# {"response": {"(3, 4)": 3}}
