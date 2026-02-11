ARC_CHAPTERS = [
    ("Romance Dawn", 1, 7),
    ("Orange Town", 8, 21),
    ("Syrup Village", 22, 41),
    ("Baratie", 42, 68),
    ("Arlong Park", 69, 95),
    ("Loguetown", 96, 100),

    ("Reverse Mountain", 101, 105),
    ("Whiskey Peak", 106, 114),
    ("Little Garden", 115, 129),
    ("Drum Island", 130, 154),
    ("Alabasta", 155, 217),

    ("Jaya", 218, 236),
    ("Skypiea", 237, 302),

    ("Long Ring Long Land", 303, 321),
    ("Water 7", 322, 374),
    ("Enies Lobby", 375, 430),
    ("Post-Enies Lobby", 431, 441),

    ("Thriller Bark", 442, 489),

    ("Sabaody Archipelago", 490, 513),
    ("Amazon Lily", 514, 524),
    ("Impel Down", 525, 549),
    ("Marineford", 550, 580),
    ("Post-War", 581, 597),

    ("Return to Sabaody", 598, 602),
    ("Fish-Man Island", 603, 653),

    ("Punk Hazard", 654, 699),
    ("Dressrosa", 700, 801),

    ("Zou", 802, 824),
    ("Whole Cake Island", 825, 902),

    ("Levely", 903, 908),
    ("Wano Country", 909, 1057),

    ("Egghead", 1058, 9999)  # open-ended
]

ARC_TO_ORDER = {arc: i for i, (arc, _, _) in enumerate(ARC_CHAPTERS)}
ORDER_TO_ARC = {i: arc for i, (arc, _, _) in enumerate(ARC_CHAPTERS)}

def arc_from_chapter(chapter: int) -> str:
    for arc, start, end in ARC_CHAPTERS:
        if start <= chapter <= end:
            return arc
    raise ValueError("Chapter out of range")

def chapter_before(a: int, b: int) -> bool:
    return a < b

def arc_before(arc_a: str, arc_b: str) -> bool:
    index = {arc: i for i, (arc, _, _) in enumerate(ARC_CHAPTERS)}
    return index[arc_a] < index[arc_b]

def chapter_before_arc(chapter: int, arc: str) -> bool:
    for a, start, _ in ARC_CHAPTERS:
        if a == arc:
            return chapter < start
    return False
    
if __name__ == "__main__":
    print(arc_from_chapter(150))  # Should print "Drum Island"
    print(arc_before("Alabasta", "Jaya"))  # Should print True
    print(chapter_before_arc(200, "Jaya"))  # Should print True
    print(ARC_TO_ORDER["Whole Cake Island"])  # Should print (825, 902)