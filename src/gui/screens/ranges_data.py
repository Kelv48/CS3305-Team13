preflop_data = {
        # vs raise (villains: seats before hero)
        # ALL HJ combos
        ("vs raise", "HJ", "LJ"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A5s", "A4s",
                      "KQs", "KJs", "KTs",
                      "QJs",
                      "AKo", "AQo",
                      "KQo"
                      },
            "call": set()},

        # ALL CO combos
        ("vs raise", "CO", "LJ"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A5s", "A4s",
                      "KQs", "KJs", "KTs",
                      "QJs",
                      "AKo", "AQo",
                      "KQo"
                      },
            "call": set()},

        ("vs raise", "CO", "HJ"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A5s", "A4s",
                      "KQs", "KJs", "KTs",
                      "QJs",
                      "AKo", "AQo", "AJo",
                      "KQo"
                      },
            "call": set()},

        # ALL BTN combos
        ("vs raise", "BTN", "LJ"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A5s", "A4s",
                      "KQs", "KJs", "KTs",
                      "QJs",
                      "AKo", "AQo",
                      "KQo"
                      },
            "call": {"99", "88", "77", "66", "55", "44",
                     "98s", 
                     "87s",
                     "76s", 
                     "65s", 
                     "54s"
                     }},

        ("vs raise", "BTN", "HJ"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A5s", "A4s",
                      "KQs", "KJs", "KTs",
                      "QJs",
                      "AKo", "AQo", "AJo",
                      "KQo"
                      },
            "call": {"99", "88", "77", "66", "55",
                     "98s", 
                     "87s",
                     "76s"
                     }},
        ("vs raise", "BTN", "CO"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A5s", "A4s",
                      "KQs", "KJs", "KTs", "K9s",
                      "QJs", "QTs",
                      "JTs",
                      "AKo", "AQo", "AJo", "ATo",
                      "KQo", "KJo",
                      "QJo"
                      },
            "call": {"99", "88", "77",
                     "98s", 
                     "87s",
                     "76s"
                     }},

        # ALL SB combos
        ("vs raise", "SB", "LJ"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A5s", "A4s",
                      "KQs", "KJs", "KTs",
                      "QJs",
                      "AKo", "AQo",
                      },
            "call": set()},
        ("vs raise", "SB", "HJ"):
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A5s", "A4s",
                      "KQs", "KJs", "KTs",
                      "QJs",
                      "AKo", "AQo", "AJo",
                      "KQo"
                      },
            "call": set()},
        ("vs raise", "SB", "CO"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A5s", "A4s", "A3s",
                      "KQs", "KJs", "KTs",
                      "QJs", "QTs",
                      "JTs"
                      "AKo", "AQo", "AJo",
                      "KQo", "KJo"
                      },
            "call": set()},
        ("vs raise", "SB", "BTN"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
                      "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s",
                      "KQs", "KJs", "KTs", "K9s",
                      "QJs", "QTs", "Q9s",
                      "JTs",
                      "T9s", 
                      "AKo", "AQo", "AJo", "ATo",
                      "KQo", "KJo"
                      },
            "call": set()},
        
        # ALL BB combos
        ("vs raise", "BB", "LJ"): 
            {"raise": {"AA", "KK", "QQ",
                      "AKs", "AQs", "AJs", "ATs", "A5s", "A4s",
                      "KQs", "KJs",
                      "AKo",
                      "KQo"
                      },
            "call": {"JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                     "A9s", "A8s", "A7s", "A6s", "A3s", "A2s",
                     "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s",
                     "QJs", "QTs", "Q9s", "Q8s", "Q7s",
                     "JTs", "J9s", "J8s",
                     "T9s", "T8s", "T7s",
                     "98s", "97s", "96s",
                     "87s", "86s",
                     "76s", "75s",
                     "65s", "64s",
                     "54s", "53s",
                     "43s",

                     "AQo", "AJo", "ATo",
                     }},

        ("vs raise", "BB", "HJ"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "AQs", "ATs", "A6s", "A5s", "A4s", "A3s", "A2s",
                      "K6s", "K5s", "K4s", "K3s", "K2s",
                      "AKo",
                      "KQo"
                      },
            "call": {"TT", "99", "88", "77", "66", "55", "44", "33", "22",
                     "AJs", "ATs", "A9s", "A8s", "A7s",
                     "KQs", "KJs", "KTs", "K9s", "K8s", "K7s",
                     "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s",
                     "JTs", "J9s", "J8s",
                     "T9s", "T8s", "T7s",
                     "98s", "97s", "96s",
                     "87s", "86s", "85s", 
                     "76s", "75s", 
                     "65s", "64s",
                     "54s", "53s",
                     "43s",

                     "AQo", "AJo", "ATo",
                     "KJo", 
                     "QJo"
                     }},
        ("vs raise", "BB", "CO"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "AQs", "ATs", "A6s", "A5s", "A4s", "A3s", "A2s",
                      "K6s", "K5s", "K4s", "K3s", "K2s",
                      "AKo", "AQo", "AJo",
                      "KQo"
                      },
            "call": {"TT", "99", "88", "77", "66", "55", "44", "33", "22",
                     "AJs", "ATs", "A9s", "A8s", "A7s",
                     "KQs", "KJs", "KTs", "K9s", "K8s", "K7s",
                     "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s",
                     "JTs", "J9s", "J8s", "J7s", "J6s",
                     "T9s", "T8s", "T7s",
                     "98s", "97s", "96s",
                     "87s", "86s", 
                     "76s", "75s", 
                     "65s", "64s",
                     "54s", "53s",
                     "43s",

                     "ATo", "A9o",
                     "KJo", "KTo",
                     "QJo", "QTo",
                     "JTo"
                     }},
        ("vs raise", "BB", "BTN"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "AQs", "ATs", "A5s", "A4s",
                      "KQs", "KJs", "KTs", "K9s",
                      "QJs", "QTs", "Q9s",
                      "JTs", "J9s", "J8s",
                      "T9s", "T8s",
                      "98s",
                      "AKo", "AQo", "AJo", "ATo",
                      "KQo", "KJo"
                      },
            "call": {"88", "77", "66", "55", "44", "33", "22",
                     "A9s", "A8s", "A7s", "A6s", "A3s", "A2s",
                     "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                     "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                     "J7s", "J6s", "J5s", "J4s",
                     "T7s", "T6s",
                     "97s", "96s",
                     "87s", "86s", "85s",
                     "76s", "75s", "74s",
                     "65s", "64s",
                     "54s", "53s",
                     "43s",

                     "A9o", "A8o", "A7o", "A6o", "A5o",
                     "KTo", "K9o",
                     "QJo", "QTo",
                     "JTo", "J9o",
                     "T9o"
                     }},

        ("vs raise", "BB", "SB"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "ATs", "A5s", "A4s",
                      "KQs", "KJs", "KTs", 
                      "QJs",
                      "T5s", "T4s", "T3s", "T2s",
                      "AKo", "AQo", "A7o", "A6o", "A5o", "A4o", "A3o", "A2o"
                      },
            "call": {"99", "88", "77", "66", "55", "44", "33", "22",
                     "A9s", "A8s", "A7s", "A6s", "A3s", "A2s",
                     "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                     "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                     "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s",
                     "T9s", "T8s", "T7s", "T6s",
                     "98s", "97s", "96s", "95s",
                     "87s", "86s", "85s", "84s",
                     "76s", "75s", "74s",
                     "65s", "64s", "63s",
                     "54s", "53s", "52s",
                     "43s", "42s",
                     "32s",

                     "AJo", "ATo", "A9o", "A8o",
                     "KQo", "KJo", "KTo", "K9o", "K8o",
                     "QJo", "QTo", "Q9o",
                     "JTo", "J9o",
                     "T9o", "T8o"
                     }},
        


    
  


        # vs 3bet (villains: seats after hero)
        ("vs 3bet", "LJ", "HJ"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "A5s", "A4s",
                      "AKo",
                      "KQs", "KJs"
                      },
            "call": {"TT", "99", "88",
                     "AQs", "AJs", "ATs"
                     }},

        ("vs 3bet", "LJ", "CO"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "A5s", "A4s",
                      "AKo",
                      "KQs", "KJs", "KTs"
                      },
            "call": {"TT", "99", "88",
                     "AQs", "AJs", "ATs"
                     }},

        ("vs 3bet", "LJ", "BTN"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "A5s", "A4s",
                      "AKo",
                      "KQs", "KJs", "KTs"
                      },
            "call": {"TT", "99", "88", "77",
                     "AQs", "AJs", "ATs"
                     }},

        ("vs 3bet", "LJ", "SB"): 
            {"raise": {"AA", "KK",
                      "AKs", "A5s", "A4s",
                      "AKo",
                      "KQs"
                      },
            "call": {"QQ","JJ", "TT", "99", "88",
                     "AQs", "AJs", "ATs"
                     }},

        ("vs 3bet", "LJ", "BB"): 
            {"raise": {"AA", "KK",
                      "AKs", "A5s", "A4s",
                      "AKo"
                      },
            "call": {"QQ","JJ", "TT", "99", 
                     "AQs", "AJs", "ATs",
                     "KQs", "KJs",
                     "QJs"
                     }},



        ("vs 3bet", "HJ", "CO"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "A5s",
                      "KQs", "KJs", "KTs",
                      "AKo", "AQo"
                      },
            "call": {"TT", "99", "88",
                     "AQs", "AJs", "ATs"
                     }},

        ("vs 3bet", "HJ", "BTN"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "A5s",
                      "KQs", "KJs", "KTs",
                      "AKo", "AQo"
                      },
            "call": {"TT", "99", "88", "77",
                     "AQs", "AJs", "ATs"
                     }},

        ("vs 3bet", "HJ", "SB"):
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "A5s",
                      "KQs", "KJs", "KTs",
                      "AKo", "AQo"
                      },
            "call": {"TT", "99", "88", "77",
                     "AQs", "AJs", "ATs"
                     }},

        ("vs 3bet", "HJ", "BB"): 
            {"raise": {"AA", "KK",
                      "AKs", "A5s",
                      "AKo", "AQo"
                      },
            "call": {"QQ","JJ", "TT", "99", "88", "77",
                     "AQs", "AJs", "ATs",
                     "KQs"
                     }},



        ("vs 3bet", "CO", "BTN"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "A5s",
                      "JTs",
                      "AKo", "AQo", "AJo", "ATo"
                      },
            "call": {"TT", "99", "88", "77",
                     "AQs", "AJs", "ATs",
                     "KQs", "KJs", "KTs"
                     }},

        ("vs 3bet", "CO", "SB"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "ATs", "A5s",
                      "KTs",
                      "AKo", "AQo"
                      },
            "call": {"99", "88", "77",
                     "AQs", "AJs",
                     "KQs", "KJs",
                     "JTs"
                     }},
        
        ("vs 3bet", "CO", "BB"): 
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs", "A5s",
                      "AKo", "AQo"
                      },
            "call": {"TT", "99", "88", "77",
                     "AQs", "AJs", "ATs", "A9s",
                     "KQs", "KJs", "KTs",
                     "QJs",
                     "JTs"
                     }},



        ("vs 3bet", "BTN", "SB"):
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "A9s", "A8s", "A5s",
                      "AKo", "AQo"
                      },
            "call": {"99", "88", "77",
                     "AJs", "ATs",
                     "KQs", "KJs", "KTs",
                     "QJs", "QTs",
                     "JTs",
                     "T9s", 
                     "98s"
                     }},

        ("vs 3bet", "BTN", "BB"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "A5s",
                      "AKo", "AQo"
                      },
            "call": {"99", "88", "77", "66", "55",
                     "AJs", "ATs", "A9s", "A8s",
                     "KQs", "KJs", "KTs", "K9s",
                     "QJs", "QTs",
                     "JTs",
                     "T9s", 
                     "98s", 
                     "87s", 
                     "76s", 
                     "65s"
                     }},


        ("vs 3bet", "SB", "BB"): 
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "A7s", "A6s", "A5s", "A4s",
                      "AKo", "AQo", "AJo", "ATo"
                      },
            "call": {"99", "88", "77",
                     "AJs", "ATs", "A9s", "A8s",
                     "KQs", "KJs", "KTs", "K9s",
                     "QJs", "QTs", "Q9s",
                     "JTs", "J9s",
                     "T9s"
                     }},
        


   
        # vs 4bet (villains: seats before hero)
        ("vs 4bet", "HJ", "LJ"): 
            {"raise": {"AA", "KK",
                      "AKs",
                      "AKo"
                      },
            "call": {"QQ","JJ",
                     "AQs", "AJs",
                     "KQs"
                     }},


        ("vs 4bet", "CO", "LJ"): 
            {"raise": {"AA", "KK",
                      "AKs",
                      "AKo"
                      },
            "call": {"QQ","JJ",
                     "AQs", "AJs",
                     "KQs"
                     }},

        ("vs 4bet", "CO", "HJ"): 
            {"raise": {"AA", "KK",
                      "AKs",
                      "AKo"
                      },
            "call": {"QQ", "JJ", "TT",
                     "AQs", "AJs",
                     "KQs", "KJs",
                     }},

        ("vs 4bet", "BTN", "LJ"): 
            {"raise": {"AA", "KK",
                      "AKs",
                      "AKo"
                      },
            "call": {"QQ","JJ",
                     "AQs", "AJs",
                     "KQs"
                     }},

        ("vs 4bet", "BTN", "HJ"):
            {"raise": {"AA", "KK", "QQ",
                      "AKs",
                      "AKo"
                      },
            "call": {"JJ", "TT",
                     "AQs", "AJs",
                     "KQs", "KJs"
                     }},

        ("vs 4bet", "BTN", "CO"):
            {"raise": {"KK", "QQ", "JJ",
                      "AKs", "A5s",
                      "AKo"
                      },
            "call": {"AA", "TT",
                     "AQs", "AJs", "ATs",
                     "KQs", "KJs", "KTs"    
                     }},

        ("vs 4bet", "SB", "LJ"): 
            {"raise": {"AA", "KK",
                      "AKs",
                      "AKo"
                      },
            "call": {"QQ","JJ",
                     "AQs", "AJs",
                     "KQs"
                     }},

        ("vs 4bet", "SB", "HJ"):
            {"raise": {"AA", "KK", "QQ",
                      "AKs", "A5s",
                      "AKo"
                      },
            "call": {"QQ","JJ",
                     "AQs", "AJs",
                     "KQs"
                     }},

        ("vs 4bet", "SB", "CO"):
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "A5s",
                      "AKo"
                      },
            "call": {"99",
                     "AQs", "AJs",
                     "KQs"
                     }},
        ("vs 4bet", "SB", "BTN"):
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "A5s",
                      "AKo", "AQo"
                      },
            "call": {"99", "88",
                     "AJs", "ATs",
                     "KQs"
                     }},

        ("vs 4bet", "BB", "LJ"): 
            {"raise": {"AA", "KK",
                      "AKs",
                      "AKo"
                      },
            "call": {"QQ",
                     "AQs"
                     }},
        ("vs 4bet", "BB", "HJ"):
            {"raise": {"AA", "KK", "QQ",
                      "AKs",
                      "AKo"
                      },
            "call": {"JJ",
                     "AQs"
                     }},
        ("vs 4bet", "BB", "CO"):
            {"raise": {"AA", "KK", "QQ", "JJ",
                      "AKs",
                      "AKo"
                      },
            "call": {"AQs"
                     }},
        ("vs 4bet", "BB", "BTN"):
            {"raise": {"AA", "KK", "QQ", "JJ", "TT",
                      "AKs", "AQs", "A5s", "A4s",
                      "AKo"
                      },
            "call": {"99",
                     "AJs",
                     "KQs",
                     "AQo"
                     }},
        ("vs 4bet", "BB", "SB"):
            {"raise": {"KK", "QQ", "JJ", "TT",
                      "AKs", "A5s", "A4s",
                      "AKo", "AQo"
                      },
            "call": {"AA",
                     "AQs", "AJs", "ATs",
                     "KQs", "KJs", "KTs",
                     "QJs"
                     }},
        


        # vs 5bet (villains: seats after hero)
        ("vs 5bet", "LJ", "HJ"):
            {"raise": set(),
            "call": {"AA", "KK",
                     "AKs",
                     "AKo"
                     }},

        ("vs 5bet", "LJ", "CO"):
            {"raise": set(),
            "call": {"AA", "KK",
                     "AKs",
                     "AKo"
                     }},

        ("vs 5bet", "LJ", "BTN"):
            {"raise": set(),
            "call": {"AA", "KK",
                     "AKs",
                     "AKo"
                     }},

        ("vs 5bet", "LJ", "SB"):
            {"raise": set(),
            "call": {"AA", "KK",
                     "AKs",
                     "AKo"
                     }},

        ("vs 5bet", "LJ", "BB"):
            {"raise": set(),
            "call": {"AA", "KK",
                     "AKs",
                     "AKo"
                     }},


        ("vs 5bet", "HJ", "CO"):
            {"raise": set(),
            "call": {"AA", "KK", "QQ",
                     "AKs",
                     "AKo"
                     }},
        ("vs 5bet", "HJ", "BTN"):
            {"raise": set(),
            "call": {"AA", "KK", "QQ",
                     "AKs",
                     "AKo"
                     }},
        ("vs 5bet", "HJ", "SB"):
            {"raise": set(),
            "call": {"AA", "KK", "QQ",
                     "AKs",
                     "AKo"
                     }},
        ("vs 5bet", "HJ", "BB"): 
            {"raise": set(),
            "call": {"AA", "KK",
                     "AKs",
                     "AKo"
                     }},


        ("vs 5bet", "CO", "BTN"):
            {"raise": set(),
            "call": {"AA", "KK", "QQ", "JJ",
                     "AKs",
                     "AKo"
                     }},
        ("vs 5bet", "CO", "SB"):
            {"raise": set(),
            "call": {"AA", "KK", "QQ", "JJ", "TT",
                     "AKs",
                     "AKo"
                     }},
        ("vs 5bet", "CO", "BB"): 
            {"raise": set(),
            "call": {"AA", "KK", "QQ", "JJ",
                     "AKs",
                     "AKo"
                     }},


        ("vs 5bet", "BTN", "SB"):
            {"raise": set(),
            "call": {"AA", "KK", "QQ", "JJ",
                     "AKs", "AQs",
                     "AKo"
                     }},
        ("vs 5bet", "BTN", "BB"): 
            {"raise": set(),
            "call": {"AA", "KK", "QQ", "JJ",
                     "AKs",
                     "AKo"
                     }},
        

        ("vs 5bet", "SB", "BB"):
            {"raise": set(),
            "call": {"AA", "KK", "QQ", "JJ", "TT",
                     "AKs", "AQs",
                     "AKo"
                     }}
    }




    
    # For the "Open" scenario, define ranges for each hero position.
open_ranges = {
        "LJ": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
                         "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                         "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s",
                         "QJs", "QTs", "Q9s",
                         "JTs",
                         "AKo", "AQo", "AJo", "ATo",
                         "KQo", "KJo", "QJo"},
                 "call": set()},
        "HJ": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66",
                         "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                         "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s",
                         "QJs", "QTs", "Q9s", "Q8s",
                         "JTs",
                         "AKo", "AQo", "AJo", "ATo", "A9o",
                         "KQo", "KJo", "KTo", "QJo", "QTo"},
                 "call": set()},
        "CO": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                         "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                         "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s",
                         "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s",
                         "JTs", "J9s", "J8s", "J7s",
                         "T9s", "T8s",
                         "98s",
                         "AKo", "AQo", "AJo", "ATo", "A9o", "A8o",
                         "KQo", "KJo", "KTo", "K9o",
                         "QJo", "QTo", "JTo"},
                 "call": set()},
        "BTN": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                          "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                          "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                          "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                          "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s",
                          "T9s", "T8s", "T7s", "T6s",
                          "98s", "97s", "96s",
                          "87s", "86s",
                          "76s", "75s",
                          "65s",
                          "54s",
                          "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7s", "A6s", "A5s", "A4s", "A3s",
                          "KQo", "KJo", "KTo", "K9o", "K8o",
                          "QJo", "QTo", "Q9o",
                          "JTo", "J9o",
                          "T9o"},
                 "call": set()},
        "SB": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                         "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                         "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                         "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                         "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s",
                         "T9s", "T8s", "T7s", "T6s",
                         "98s", "97s", "96s",
                         "87s", "86s",
                         "76s", "75s",
                         "65s",
                         "54s"},
                 "call": set()}
    }