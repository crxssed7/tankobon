function importKitsu(modal, toast) {
    kitsuId = document.getElementById("kitsuId").value;
    if (kitsuId) {
        $.ajax({
            url: "https://kitsu.io/api/edge/manga/" + kitsuId,
            type: "GET",
            success: function (response) {
                const data = response.data
                var name = document.getElementById("id_name")
                var romaji = document.getElementById("id_romaji")
                var description = document.getElementById("id_description")
                var status = document.getElementById("id_status")
                var startDate = document.getElementById("id_start_date")
                var poster = document.getElementById("id_poster")
                var banner = document.getElementById("id_banner")
                var anilistId = document.getElementById("id_anilist_id")
                var malId = document.getElementById("id_mal_id")
                var mangaupdatesId = document.getElementById("id_mangaupdates_id")
                var animeplanetSlug = document.getElementById("id_anime_planet_slug")
                var idKitsu = document.getElementById("id_kitsu_id")
                var magazine = document.getElementById("id_magazine")
                var volumeCount = document.getElementById("id_volume_count")

                name.value = data.attributes.canonicalTitle
                romaji.value = data.attributes.titles.en_jp
                description.value = data.attributes.description
                if (data.attributes.status === "current") {
                    status.selectedIndex = 1
                } else if (data.attributes.status === "finished") {
                    status.selectedIndex = 2
                }
                startDate.value = data.attributes.startDate
                if (data.attributes.posterImage) {
                    poster.value = data.attributes.posterImage.medium
                }
                if (data.attributes.coverImage) {
                    banner.value = data.attributes.coverImage.original
                }
                idKitsu.value = data.id
                magazine.value = data.attributes.serialization
                volumeCount.value = data.attributes.volumeCount

                modal.hide()
            },
            error: function (err) {
                console.log(err);
                modal.hide();
                toast.show();
            },
        })
    } else {
        console.log("No kitsu id entered")
    }
}

function importAnilist(modal) {
    anilistId = document.getElementById("anilistId").value;
    if (anilistId) {
        var query = `
        {
            Media(id: ${anilistId}, type: MANGA) {
              title {
                romaji
                english
                native
                userPreferred
              },
              description,
              status,
              startDate {
                year
                month
                day
              },
              coverImage {
                extraLarge
                large
                medium
                color
              },
              bannerImage,
              id,
              idMal,
              volumes
            }
          }
        `

        $.ajax({
            url: "https://graphql.anilist.co",
            method: "POST",
            data: {
                "query": query
            },
            success: function (response) {
                const data = response.data
                var name = document.getElementById("id_name")
                var romaji = document.getElementById("id_romaji")
                var description = document.getElementById("id_description")
                var status = document.getElementById("id_status")
                var startDate = document.getElementById("id_start_date")
                var poster = document.getElementById("id_poster")
                var banner = document.getElementById("id_banner")
                var idAnilist = document.getElementById("id_anilist_id")
                var malId = document.getElementById("id_mal_id")
                var mangaupdatesId = document.getElementById("id_mangaupdates_id")
                var animeplanetSlug = document.getElementById("id_anime_planet_slug")
                var idKitsu = document.getElementById("id_kitsu_id")
                var magazine = document.getElementById("id_magazine")
                var volumeCount = document.getElementById("id_volume_count")

                name.value = data.Media.title.english
                romaji.value = data.Media.title.romaji
                description.value = data.Media.description
                if (data.Media.status === "RELEASING") {
                    status.selectedIndex = 1
                } else if (data.Media.status === "FINISHED") {
                    status.selectedIndex = 2
                }
                var MM = ""
                if (data.Media.startDate.month < 10) {
                    MM = "0" + data.Media.startDate.month
                } else {
                    MM = data.Media.startDate.month.toString()
                }
                var dd = ""
                if (data.Media.startDate.day < 10) {
                    dd = "0" + data.Media.startDate.day
                } else {
                    dd = data.Media.startDate.day.toString()
                }
                startDate.value = data.Media.startDate.year + "-" + MM + "-" + dd
                if (data.Media.coverImage) {
                    poster.value = data.Media.coverImage.large
                }
                if (data.Media.bannerImage) {
                    banner.value = data.Media.bannerImage
                }
                idAnilist.value = data.Media.id
                malId.value = data.Media.idMal
                volumeCount.value = data.Media.volumes

                modal.hide()
            },
            error: function (err) {
                console.log(err);
                modal.hide();
                toast.show();
            },
        })
    } else {
        console.log("No anilist id entered")
    }
}