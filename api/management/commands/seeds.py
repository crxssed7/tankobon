# pylint: skip-file

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import datetime

from api.models import Manga, Volume, Collection, Edition, Genre, Language

from tankobon.settings import DEBUG


class Command(BaseCommand):
    help = "Seeds the database with test data"

    def handle(self, *args, **options):
        if DEBUG:
            print("Dropping existing data")
            Manga.objects.all().delete()
            Volume.objects.all().delete()
            Collection.objects.all().delete()
            Edition.objects.all().delete()
            Genre.objects.all().delete()
            Language.objects.all().delete()

            # ===================================================================================================

            print("Creating Genres")
            shounen = Genre.objects.create(
                name="Shounen",
            )
            shoujo = Genre.objects.create(
                name="Shoujo",
            )
            seinen = Genre.objects.create(
                name="Seinen",
            )
            josei = Genre.objects.create(
                name="Josei",
            )
            drama = Genre.objects.create(
                name="Drama"
            )
            action = Genre.objects.create(
                name="Action"
            )
            adventure = Genre.objects.create(
                name="Adventure"
            )
            supernatural = Genre.objects.create(
                name="Supernatural"
            )
            comedy = Genre.objects.create(
                name="Comedy"
            )
            slice_of_life = Genre.objects.create(
                name="Slice of Life"
            )
            mystery = Genre.objects.create(
                name="Mystery"
            )
            romance = Genre.objects.create(
                name="Romance"
            )
            music = Genre.objects.create(
                name="Music"
            )
            science_fiction = Genre.objects.create(
                name="Science Fiction"
            )
            fantasy = Genre.objects.create(
                name="Fantasy"
            )
            horror = Genre.objects.create(
                name="Horror"
            )
            psychological = Genre.objects.create(
                name="Psychological"
            )

            # ===================================================================================================

            print("Creating Languages")
            english = Language.objects.create(
                name="English",
                code="US"
            )
            japanese = Language.objects.create(
                name="Japanese",
                code="JP"
            )

            # ===================================================================================================

            print("Creating Manga")
            demon_slayer = Manga.objects.create(
                name="Demon Slayer",
                romaji="Kimetsu no Yaiba",
                description="The setting is Taisho era Japan. Tanjirou is a kindhearted young boy who lived peacefully with his family as a coal seller. Their normal life changes completely when his family is slaughtered by demons. The only other survivor, Tanjirou's younger sister Nezuko, has become a ferocious demon. In order to return Nezuko to normal and get revenge on the demon that killed their family, the two of them depart on a journey. From a young talent, an adventure tale of blood and swords begins!",
                status="FINISHED",
                start_date="2016-02-15",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx87216-c9bSNVD10UuD.png",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/87216-TVKEGfSxAqKs.jpg",
                anilist_id=87216,
                mal_id=96792,
                mangaupdates_id=130757,
                anime_planet_slug="demon-slayer-kimetsu-no-yaiba",
                kitsu_id=37280,
                fandom="https://kimetsu-no-yaiba.fandom.com/f",
                magazine="Shounen Jump",
                locked=True,
                tags="demons, swords, old era"
            )
            demon_slayer.genres.set([action, adventure, supernatural, shounen])
            demon_slayer_edition = demon_slayer.edition_set.first()
            demon_slayer_edition.language = japanese
            demon_slayer_edition.save()

            spy_family = Manga.objects.create(
                name="SPY x FAMILY",
                romaji="SPY×FAMILY",
                description="The master spy codenamed Twilight has spent his days on undercover missions, all for the dream of a better world. But one day, he receives a particularly difficult new order from command. For his mission, he must form a temporary family and start a new life?! A Spy/Action/Comedy about a one-of-a-kind family!",
                status="RELEASING",
                start_date="2019-03-25",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx108556-NHjkz0BNJhLx.jpg",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/108556-iCiPfU0GU4OM.jpg",
                anilist_id=108556,
                mal_id=119161,
                mangaupdates_id=153402,
                anime_planet_slug="spy-x-family",
                kitsu_id=54448,
                fandom="https://spy-x-family.fandom.com/f",
                magazine="Shounen Jump+",
                locked=False,
                tags="spy, war, esper"
            )
            spy_family.genres.set([action, supernatural, shounen, comedy, slice_of_life])
            spy_family_edition = spy_family.edition_set.first()
            spy_family_edition.language = japanese
            spy_family_edition.save()

            ruri_dragon = Manga.objects.create(
                name="Ruri Dragon",
                romaji="Ruri Dragon",
                description="Ruri faces the usual issues: pushy classmates, annoying teachers and... waking up with dragon horns?!",
                status="RELEASING",
                start_date="2022-06-13",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx150440-ZgOHRsvdwsVo.jpg",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/150440-xvrwegI0XlIR.jpg",
                anilist_id=150440,
                mal_id=148054,
                anime_planet_slug="ruri-dragon",
                kitsu_id=63638,
                fandom="https://ruridragon.fandom.com/wiki/RuriDragon_Wiki",
                magazine="Shounen Jump",
                locked=False,
                tags="dragons"
            )
            ruri_dragon.genres.set([supernatural, shounen, comedy, slice_of_life])

            hells_paradise = Manga.objects.create(
                name="Hell's Paradise: Jigokuraku",
                romaji="Jigokuraku",
                description="Gabimaru the Hollow is one of the most vicious assassins ever to come out of the ninja village of Iwagakure. He’s ruthlessly efficient, but a betrayal results in him being handed a death sentence. He has only one hope—in order to earn his freedom, he must travel to a long-hidden island and recover an elixir that will make the shogun immortal. Failure is not an option. On this island, heaven and hell are just a hair’s breadth away.\n\n(Source: Viz Media)",
                status="FINISHED",
                start_date="2018-01-23",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx100994-f6CMjiQQNVeS.png",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/100994-mEIqjSzFKysR.jpg",
                anilist_id=100994,
                mal_id=112318,
                mangaupdates_id=146739,
                anime_planet_slug="hells-paradise-jigokuraku",
                kitsu_id=40546,
                fandom="https://jigokuraku.fandom.com/wiki/Jigokuraku_Wiki",
                magazine="Shounen Jump+",
                locked=True,
                tags="hells paradise"
            )
            hells_paradise.genres.set([supernatural, shounen, action, adventure, mystery])

            banana_fish = Manga.objects.create(
                name="Banana Fish",
                romaji="Banana Fish",
                description="Nature made Ash Lynx beautiful; nurture made him a cold ruthless killer. A runaway brought up as the adopted heir and sex toy of \"Papa\" Dino Golzine, Ash, now at the rebellious age of seventeen, forsakes the kingdom held out by the devil who raised him. But the hideous secret that drove Ash's older brother mad in Vietnam has suddenly fallen into Papa's insatiably ambitious hands--and it's exactly the wrong time for Eiji Okamura, a pure-hearted young photographer from Japan, to make Ash Lynx's acquaintance...\n\n(Source: Viz Media)",
                status="FINISHED",
                start_date="1985-05-01",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx30756-rlxjQWBAizHX.jpg",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/30756-raw9tFTKi9cQ.jpg",
                anilist_id=30756,
                mal_id=756,
                mangaupdates_id=5753,
                anime_planet_slug="banana-fish",
                kitsu_id=1654,
                fandom="https://banana-fish.fandom.com/wiki/BANANA_FISH_Wiki",
                magazine="Shōjo Comic",
                locked=True,
                tags="bananas"
            )
            banana_fish.genres.set([drama, action, adventure, shoujo])

            nana = Manga.objects.create(
                name="Nana",
                romaji="NANA",
                description="Nana Komatsu is a young woman who's endured an unending string of boyfriend problems. Moving to Tokyo, she's hoping to take control of her life and put all those messy misadventures behind her. She's looking for love and she's hoping to find it in the big city.\n\nNana Osaki, on the other hand, is cool, confident and focused. She swaggers into town and proceeds to kick down the doors to Tokyo's underground punk scene. She's got a dream and won't give up until she becomes Japan's No. 1 rock'n'roll superstar.\n\nThis is the story of two 20-year-old women who share the same name. Even though they come from completely different backgrounds, they somehow meet and become best friends. The world of Nana is a world exploding with sex, music, fashion, gossip and all-night parties.\n\n(Source: Viz Media)\n\nNote: Winner of the 48th Shogakukan Manga Award in the Shoujo Category in 2002.",
                status="RELEASING",
                start_date="2000-05-15",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx30028-UxaCSA7qg1u3.png",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/30028-42xc4ztbqalW.jpg",
                anilist_id=30028,
                mal_id=28,
                mangaupdates_id=655,
                anime_planet_slug="nana",
                kitsu_id=74,
                fandom="https://nana.fandom.com/wiki/Nana_Wiki",
                magazine="Cookie",
                locked=False
            )
            nana.genres.set([romance, drama, shoujo, slice_of_life, music])

            skull_face = Manga.objects.create(
                name="Skull-face Bookseller Honda-san",
                romaji="Gaikotsu Shotenin Honda-san",
                description="Ever wonder what it's like to sell comics at a Japanese bookstore? Honda provides a hilarious firsthand account from the front lines! Whether it's handling the store, out-of-print books, or enthusiastic manga fans, Honda takes on every challenge!\n\n(Source: Yen Press)",
                status="FINISHED",
                start_date="2015-08-27",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/nx105439-pwKt9SazJKMW.jpg",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/105439-JsyqmoG47Ql1.jpg",
                anilist_id=105439,
                mal_id=104337,
                mangaupdates_id=125127,
                anime_planet_slug="skull-face-bookseller-honda-san",
                kitsu_id=40100,
                fandom="https://skullface-bookseller.fandom.com/wiki/Skull-Face_Bookseller_Honda-san_Wiki",
                magazine="pixiv Comic",
                locked=True,
                tags="skullface bookseller"
            )
            skull_face.genres.set([comedy, slice_of_life, shoujo])

            natsume = Manga.objects.create(
                name="Natsume's Book of Friends",
                romaji="Natsume Yuujinchou",
                description="When Reiko was Takashi's age, she bound the names of demons and spirits in her Book of Friends, enslaving them to her capricious whim. Now Takashi is the owner of the book, and the creatures will do anything to get their names back.\n\n(Source: Viz Media)",
                status="RELEASING",
                start_date="2003-06-10",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx31859-mITgIaJFBzl4.png",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/31859-cldDQH6BHxtF.jpg",
                anilist_id=31859,
                mal_id=1859,
                mangaupdates_id=6781,
                anime_planet_slug="natsumes-book-of-friends",
                kitsu_id=3917,
                fandom="https://natsumeyuujinchou.fandom.com/wiki/Main_Page",
                magazine="LaLa DX",
                locked=False,
                tags="natsumes book of friends"
            )
            natsume.genres.set([shoujo, drama, supernatural])

            girls_last_tour = Manga.objects.create(
                name="Girls' Last Tour",
                romaji="Shoujo Shuumatsu Ryokou",
                description="Civilization is dead, but Chito and Yuuri are still alive. So they hop aboard their beloved Kettenkrad motorbike and aimlessly wander the ruins of the world they once knew. Day after hopeless day, they look for their next meal and fuel for their ride. But as long as the two are together, even an existence as bleak as theirs has a ray or two of sunshine in it, whether they're sucking down their fill of soup or hunting for machine parts to tinker with. For two girls in a world full of nothing, the experiences and feelings the two share give them something to live for…\n\n(Source: Yen Press)\n\nNote: Winner of the Best Comic Award at the Seiun Awards in 2019.",
                status="FINISHED",
                start_date="2014-02-21",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx85412-3kJSfIV9pji2.jpg",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/85412-H9Uo0YNhxd9J.jpg",
                anilist_id=85412,
                mal_id=72467,
                mangaupdates_id=108708,
                anime_planet_slug="girls-last-tour",
                kitsu_id=25931,
                fandom="https://girls-last-tour.fandom.com/wiki/Girls_Last_Tour_Wiki",
                magazine="Kurage Bunch",
                locked=True,
                tags="dystopia"
            )
            girls_last_tour.genres.set([slice_of_life, adventure, science_fiction, seinen])

            househusband = Manga.objects.create(
                name="The Way of the Househusband",
                romaji="Gokushufudou",
                description="He was the fiercest member of the yakuza, a man who left countless underworld legends in his wake. They called him “the Immortal Dragon.” But one day he walked away from it all to travel another path—the path of the househusband! The curtain rises on this cozy yakuza comedy!",
                status="RELEASING",
                start_date="2018-02-26",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/nx101233-ipG2rYitNxyd.jpg",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/101233-4Q41vXLKrjhe.jpg",
                anilist_id=101233,
                mal_id=112922,
                mangaupdates_id=147413,
                anime_planet_slug="the-way-of-the-househusband",
                kitsu_id=40679,
                fandom="https://gokushufudou.fandom.com/f",
                magazine="Kurage Bunch",
                locked=False,
                tags="yakuza"
            )
            househusband.genres.set([comedy, slice_of_life, seinen])

            one_punch = Manga.objects.create(
                name="One-Punch Man",
                romaji="One Punch-Man",
                description="In this new action-comedy, everything about a young man named Saitama screams \"AVERAGE,\" from his lifeless expression, to his bald head, to his unimpressive physique. However, this average-looking fellow doesn't have your average problem... He's actually a superhero that's looking for tough opponents! The problem is, every time he finds a promising candidate he beats the snot out of them in one punch. Can Saitama finally find an evil villain strong enough to challenge him? Follow Saitama through his hilarious romps as he searches for new bad guys to challenge!",
                status="RELEASING",
                start_date="2012-06-14",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx74347-O6KMkECzHPOE.jpg",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/74347-xAQI9BxcpWM3.jpg",
                anilist_id=74347,
                mal_id=44347,
                mangaupdates_id=80345,
                anime_planet_slug="one-punch-man",
                kitsu_id=24147,
                fandom="https://onepunchman.fandom.com/f",
                magazine="Tonari no Young Jump",
                locked=False,
                tags="one punch man"
            )
            one_punch.genres.set([comedy, action, supernatural, science_fiction, seinen])

            hinamatsuri = Manga.objects.create(
                name="Hinamatsuri",
                romaji="Hinamatsuri",
                description="Nitta is an ambitious, young member of the Ashikawa-gumi yakuza syndicate. One day, a mysterious, oval-shaped object falls out of thin air into his apartment, and suddenly changes everything! Inside of the object is an expressionless young girl named Hina. The girl has formidable telekinetic powers that she uses to threaten Nitta, forcing him to allow her to live in his apartment. Dangers abound as the yakuza member and young psychic begin their life together as roommates!",
                status="FINISHED",
                start_date="2010-06-15",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx66413-MHIcMzhhOCjd.jpg",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/n66413-mM3CAMAwfR3J.jpg",
                anilist_id=66413,
                mal_id=36413,
                mangaupdates_id=53417,
                anime_planet_slug="hinamatsuri",
                kitsu_id=14480,
                fandom="https://hinamatsuri.fandom.com/wiki/Hinamatsuri_Wiki",
                magazine="Harta",
                locked=True,
                tags="yakuza"
            )
            hinamatsuri.genres.set([comedy, slice_of_life, supernatural, science_fiction, seinen])

            berserk = Manga.objects.create(
                name="Berserk",
                romaji="Berserk",
                description="His name is Guts, the Black Swordsman, a feared warrior spoken of only in whispers. Bearer of a gigantic sword, an iron hand, and the scars of countless battles and tortures, his flesh is also indelibly marked with The Brand, an unholy symbol that draws the forces of darkness to him and dooms him as their sacrifice. But Guts won't take his fate lying down; he'll cut a crimson swath of carnage through the ranks of the damned—and anyone else foolish enough to oppose him! Accompanied by Puck the Elf, more an annoyance than a companion, Guts relentlessly follows a dark, bloodstained path that leads only to death... or vengeance.",
                status="RELEASING",
                start_date="1989-08-25",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx30002-7EzO7o21jzeF.jpg",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/30002-3TuoSMl20fUX.jpg",
                anilist_id=30002,
                mal_id=2,
                mangaupdates_id=88,
                anime_planet_slug="berserk",
                kitsu_id=8,
                fandom="https://berserk.fandom.com/f",
                magazine="Young Animal",
                locked=False,
                tags="literal pain"
            )
            berserk.genres.set([drama, action, adventure, fantasy, seinen, horror, psychological])
            berserk_edition = berserk.edition_set.first()
            berserk_edition.language = japanese
            berserk_edition.save()
            berserk_deluxe = Edition.objects.create(
                name="Deluxe",
                manga=berserk,
                language=english
            )

            wotakoi = Manga.objects.create(
                name="Wotakoi: Love Is Hard for Otaku",
                romaji="Wotaku ni Koi wa Muzukashii",
                description="Narumi Momose has had it rough: every boyfriend she’s had dumped her once they found out she was an otaku, so she’s gone to great lengths to hide it. When a chance meeting at her new job with childhood friend, fellow otaku, and now coworker Hirotaka Nifuji almost gets her secret outed at work, she comes up with a plan to make sure he never speaks up. But he comes up with a counter-proposal: why doesn’t she just date him instead? In love, there are no save points.\n\n(Source: Kodansha USA)",
                status="FINISHED",
                start_date="2014-04-17",
                poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx86717-S7z7uizfTfEu.png",
                banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/86717-96ElWeIFwPPj.jpg",
                anilist_id=86717,
                mal_id=89087,
                mangaupdates_id=121092,
                anime_planet_slug="wotakoi-love-is-hard-for-otaku",
                kitsu_id=36095,
                fandom="https://wotaku-ni-koi-wa-muzukashii.fandom.com/wiki/Main_Page",
                magazine="Comic Pool",
                locked=True,
                tags="office life"
            )
            wotakoi.genres.set([comedy, romance, josei, slice_of_life])

            # ===================================================================================================

            print("Creating Volumes")
            demon_slayer_vol_1 = Volume.objects.create(
                poster_url="https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/8/83/Kimetsu_no_Yaiba_V1.png/revision/latest?cb=20181206190730",
                locked=True,
                manga=demon_slayer,
                absolute_number=1,
                chapters="|Final Selection\nChapter 1. Cruelty\nChapter 2. The Stranger\nChapter 3. Return by Dawn\nChapter 4. Tanjiro's Journal, Part 1\nChapter 5. Tanjiro's Journal, Part 2\nChapter 6. A Mountain of Hands\nChapter 7. Spirits of the Deceased",
                edition=demon_slayer_edition,
                isbn="978-4-08-880723-2",
                page_count=200,
                release_date="2016-02-15"
            )
            demon_slayer_vol_2 = Volume.objects.create(
                poster_url="https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/a/a3/Kimetsu_no_Yaiba_V2.png/revision/latest?cb=20181206190746",
                locked=True,
                manga=demon_slayer,
                absolute_number=2,
                chapters="|Final Selection\nChapter 1. Cruelty\nChapter 2. The Stranger\nChapter 3. Return by Dawn\nChapter 4. Tanjiro's Journal, Part 1\nChapter 5. Tanjiro's Journal, Part 2\nChapter 6. A Mountain of Hands\nChapter 7. Spirits of the Deceased",
                edition=demon_slayer_edition,
                isbn="978-4-08-880755-3",
                page_count=190,
                release_date="2016-02-15"
            )
            demon_slayer_vol_3 = Volume.objects.create(
                poster_url="https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/a/ae/Kimetsu_no_Yaiba_V3.png/revision/latest?cb=20181206190801",
                locked=True,
                manga=demon_slayer,
                absolute_number=3,
                chapters="|Final Selection\nChapter 1. Cruelty\nChapter 2. The Stranger\nChapter 3. Return by Dawn\nChapter 4. Tanjiro's Journal, Part 1\nChapter 5. Tanjiro's Journal, Part 2\nChapter 6. A Mountain of Hands\nChapter 7. Spirits of the Deceased",
                edition=demon_slayer_edition,
                isbn="978-4-08-880795-9",
                page_count=210,
                release_date="2016-02-15"
            )
            demon_slayer_vol_4 = Volume.objects.create(
                poster_url="https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/0/02/Kimetsu_no_Yaiba_V4.png/revision/latest?cb=20161201151048",
                locked=True,
                manga=demon_slayer,
                absolute_number=4,
                chapters="|Final Selection\nChapter 1. Cruelty\nChapter 2. The Stranger\nChapter 3. Return by Dawn\nChapter 4. Tanjiro's Journal, Part 1\nChapter 5. Tanjiro's Journal, Part 2\nChapter 6. A Mountain of Hands\nChapter 7. Spirits of the Deceased",
                edition=demon_slayer_edition,
                isbn="978-4-08-880826-0",
                page_count=190,
                release_date="2016-02-15"
            )
            demon_slayer_vol_5 = Volume.objects.create(
                poster_url="https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/0/0c/Kimetsu_no_Yaiba_V5.png/revision/latest?cb=20170513022618",
                locked=True,
                manga=demon_slayer,
                absolute_number=5,
                chapters="|Final Selection\nChapter 1. Cruelty\nChapter 2. The Stranger\nChapter 3. Return by Dawn\nChapter 4. Tanjiro's Journal, Part 1\nChapter 5. Tanjiro's Journal, Part 2\nChapter 6. A Mountain of Hands\nChapter 7. Spirits of the Deceased",
                edition=demon_slayer_edition,
                isbn="978-4-08-881026-3",
                page_count=170,
                release_date="2016-02-15"
            )

            spy_family_none = Volume.objects.create(
                locked=False,
                manga=spy_family,
                absolute_number=-1,
                chapters="Mission 67\nMission 68\nMission 69\nMission 70\nMission 71\nMission 72\nMission 73",
                edition=spy_family_edition
            )
            spy_family_vol_1 = Volume.objects.create(
                poster_url="https://static.wikia.nocookie.net/spy-x-family9171/images/0/0e/Volume_1.png/revision/latest/scale-to-width-down/1000?cb=20200508212135",
                locked=True,
                manga=spy_family,
                absolute_number=1,
                chapters="Mission 1\nMission 2\nMission 3\nMission 4\nMission 5\nMission 6\nMission 7",
                edition=spy_family_edition,
                isbn="978-4-08-882011-8",
                page_count=190,
                release_date="2016-02-15"
            )

            berserk_vol_1 = Volume.objects.create(
                poster_url="https://tankobon.s3.amazonaws.com/posters/berserk/volumes/standard-japanese/volume_1_poster.png",
                locked=False,
                manga=berserk,
                absolute_number=1,
                chapters="Chapter 1\nChapter 2\nChapter 3\nChapter 4\nChapter 5\nChapter 6\n",
                edition=berserk_edition,
                isbn="978-4-59-213574-6",
                page_count=200,
                release_date="2016-02-15"
            )
            berserk_vol_2 = Volume.objects.create(
                poster_url="https://tankobon.s3.amazonaws.com/posters/berserk/volumes/standard-japanese/volume_2_poster.png",
                locked=False,
                manga=berserk,
                absolute_number=2,
                chapters="Chapter 1\nChapter 2\nChapter 3\nChapter 4\nChapter 5\nChapter 6\n",
                edition=berserk_edition,
                isbn="978-4-59-213575-3",
                page_count=190,
                release_date="2016-02-15"
            )
            berserk_d_vol_1 = Volume.objects.create(
                poster_url="https://cdn.waterstones.com/bookjackets/large/9781/5067/9781506711980.jpg",
                locked=False,
                manga=berserk,
                absolute_number=1,
                chapters="Chapter 1\nChapter 2\nChapter 3\nChapter 4\nChapter 5\nChapter 6\n",
                edition=berserk_deluxe,
                isbn="9781506711980",
                page_count=190,
                release_date="2016-02-15"
            )

            # ===================================================================================================

            print("Creating Collections")

            user = User.objects.all().first()

            Collection.objects.create(
                user=user,
                volume=demon_slayer_vol_1,
                collected_at="2023-02-15"
            )
            Collection.objects.create(
                user=user,
                volume=demon_slayer_vol_2,
                collected_at="2023-02-15"
            )
            Collection.objects.create(
                user=user,
                volume=demon_slayer_vol_3,
                collected_at="2023-02-15"
            )
            Collection.objects.create(
                user=user,
                volume=demon_slayer_vol_4,
                collected_at="2023-02-15"
            )
            Collection.objects.create(
                user=user,
                volume=demon_slayer_vol_5,
                collected_at="2023-02-15"
            )
            Collection.objects.create(
                user=user,
                volume=spy_family_vol_1,
                collected_at="2023-03-10"
            )
            Collection.objects.create(
                user=user,
                volume=berserk_vol_1,
                collected_at="2023-01-23"
            )
            Collection.objects.create(
                user=user,
                volume=berserk_d_vol_1,
                collected_at="2023-04-12"
            )
        else:
            print("Cannot seed in production")
