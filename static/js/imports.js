class Importer {
  static async searchKitsu(query) {
    const url = `https://kitsu.io/api/edge/manga?filter[text]=${query}`;
    const options = {};

    const result = await fetch(url, options).then(this.handleResponse)
      .then(this.handleData)
      .catch(this.handleError);
    return result;
  }

  static async searchAniList(query) {
    const graphql = `
    {
      Page(page: 1, perPage: 50) {
        media(type: MANGA, search: "${query}") {
          title {
            romaji
            english
            native
            userPreferred
          }
          description
          status
          startDate {
            year
            month
            day
          }
          coverImage {
            extraLarge
            large
            medium
            color
          }
          bannerImage
          id
          idMal
          volumes
        }
      }
    }
    `;

    const url = 'https://graphql.anilist.co';
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({
        query: graphql,
      }),
    };

    const result = await fetch(url, options).then(this.handleResponse)
      .then(this.handleData)
      .catch(this.handleError);
    return result;
  }

  static handleResponse(response) {
    return response.json().then((json) => (response.ok ? json : Promise.reject(json)));
  }

  static handleData(data) {
    return data;
  }

  static handleError(error) {
    console.error(error);
  }
}

// Importer.searchKitsu('demon slayer').then((daq) => { console.log(daq); });

function importKitsu(modal, toast) {
  const kitsuId = document.getElementById('kitsuId').value;
  if (kitsuId) {
    $.ajax({
      url: `https://kitsu.io/api/edge/manga/${kitsuId}`,
      type: 'GET',
      success(response) {
        const { data } = response;
        const name = document.getElementById('id_name');
        const romaji = document.getElementById('id_romaji');
        const description = document.getElementById('id_description');
        const status = document.getElementById('id_status');
        const startDate = document.getElementById('id_start_date');
        const poster = document.getElementById('id_poster');
        const banner = document.getElementById('id_banner');
        const idKitsu = document.getElementById('id_kitsu_id');
        const magazine = document.getElementById('id_magazine');
        const volumeCount = document.getElementById('id_volume_count');

        name.value = data.attributes.canonicalTitle;
        romaji.value = data.attributes.titles.en_jp;
        description.value = data.attributes.description;
        if (data.attributes.status === 'current') {
          status.selectedIndex = 1;
        } else if (data.attributes.status === 'finished') {
          status.selectedIndex = 2;
        }
        startDate.value = data.attributes.startDate;
        if (data.attributes.posterImage) {
          poster.value = data.attributes.posterImage.medium;
        }
        if (data.attributes.coverImage) {
          banner.value = data.attributes.coverImage.original;
        }
        idKitsu.value = data.id;
        magazine.value = data.attributes.serialization;
        volumeCount.value = data.attributes.volumeCount;

        modal.hide();
      },
      error() {
        modal.hide();
        toast.show();
      },
    });
  }
}

function importAnilist(modal, toast) {
  const anilistId = document.getElementById('anilistId').value;
  if (anilistId) {
    const query = `
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
        `;

    $.ajax({
      url: 'https://graphql.anilist.co',
      method: 'POST',
      data: {
        query,
      },
      success(response) {
        const { data } = response;
        const name = document.getElementById('id_name');
        const romaji = document.getElementById('id_romaji');
        const description = document.getElementById('id_description');
        const status = document.getElementById('id_status');
        const startDate = document.getElementById('id_start_date');
        const poster = document.getElementById('id_poster');
        const banner = document.getElementById('id_banner');
        const idAnilist = document.getElementById('id_anilist_id');
        const malId = document.getElementById('id_mal_id');
        const volumeCount = document.getElementById('id_volume_count');

        name.value = data.Media.title.english;
        romaji.value = data.Media.title.romaji;
        description.value = data.Media.description;
        if (data.Media.status === 'RELEASING') {
          status.selectedIndex = 1;
        } else if (data.Media.status === 'FINISHED') {
          status.selectedIndex = 2;
        }
        let MM = '';
        if (data.Media.startDate.month < 10) {
          MM = `0${data.Media.startDate.month}`;
        } else {
          MM = data.Media.startDate.month.toString();
        }
        let dd = '';
        if (data.Media.startDate.day < 10) {
          dd = `0${data.Media.startDate.day}`;
        } else {
          dd = data.Media.startDate.day.toString();
        }
        startDate.value = `${data.Media.startDate.year}-${MM}-${dd}`;
        if (data.Media.coverImage) {
          poster.value = data.Media.coverImage.large;
        }
        if (data.Media.bannerImage) {
          banner.value = data.Media.bannerImage;
        }
        idAnilist.value = data.Media.id;
        malId.value = data.Media.idMal;
        volumeCount.value = data.Media.volumes;

        modal.hide();
      },
      error() {
        modal.hide();
        toast.show();
      },
    });
  }
}
