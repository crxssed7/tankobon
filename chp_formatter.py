# This file formats a list of chapters ready to be added to Tankobon
custom_name = "Chapter"

chapter_in = """
17. Destroyer
18. At the Back of the Treasury
19. Memories of You
20. Instant
21. Collapse and Relief
22. Assembly at the Royal Capital
23. War Merits Conferment Ceremony
24. Royal Capital Riot
25. Marching Corpses
"""

chapters = chapter_in.split('\n')
output = ""
for c in chapters:
    if c:
        print(custom_name + " " + c)
