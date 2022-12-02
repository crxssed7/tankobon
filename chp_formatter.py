# This file formats a list of chapters ready to be added to Tankobon
custom_name = "Chapter"

chapter_in = """
54. A Meeting of the Magic Knight Captains
55. The Captains and the Peasant Boy
56. Three-Leaf Salute
57. A Black Beach Story
58. The Story of the Growing Water Child
59. Seabed Temple
60. The High Priest's Game
61. Temple Battle Royale
62. The Strong Reign
"""

chapters = chapter_in.split("\n")
output = ""
for c in chapters:
    if c:
        print(custom_name + " " + c)
