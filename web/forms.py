from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from api.models import Manga, Volume, Edition, Genre


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Enter a valid email address")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class MangaForm(forms.ModelForm):
    # start_date = forms.DateField(help_text='Format: YYYY-MM-DD')
    start_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    tags = forms.CharField(
        label="Tags", help_text="Comma seperated list of tags.", required=False
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    poster_url = forms.CharField(
        label="Poster URL",
        help_text="URL to an image file.",
        required=False,
    )
    banner_url = forms.CharField(
        label="Banner URL",
        help_text="URL to an image file.",
        required=False,
    )
    anilist_id = forms.IntegerField(label="AniList ID", required=False)
    mal_id = forms.IntegerField(label="MyAnimeList ID", required=False)
    mangaupdates_id = forms.IntegerField(label="MangaUpdates ID", required=False)
    anime_planet_slug = forms.CharField(
        label="Anime Planet Slug",
        help_text="You can find the Anime Planet slug at the end of the Anime Planet url. Example: https://www.anime-planet.com/manga/anime-planet-slug",
        required=False,
    )
    kitsu_id = forms.IntegerField(label="Kitsu ID", required=False)

    class Meta:
        model = Manga
        fields = (
            "name",
            "romaji",
            "description",
            "status",
            "start_date",
            "tags",
            "genres",
            "poster_url",
            "banner_url",
            "anilist_id",
            "mal_id",
            "mangaupdates_id",
            "anime_planet_slug",
            "kitsu_id",
            "fandom",
            "magazine",
        )


class VolumeEditForm(forms.ModelForm):
    chapters = forms.CharField(
        widget=forms.Textarea(),
        help_text="Make sure that each chapter is listed on a separate line. If the chapter has a known name, include it here. To add an arc starting point use the format '|Story Arc Name'.",
    )
    poster_url = forms.CharField(
        label="Poster URL", help_text="URL to an image file.", required=False
    )

    class Meta:
        model = Volume
        fields = ("poster_url", "chapters")


class VolumeNewForm(forms.ModelForm):
    absolute_number = forms.IntegerField(
        label="Volume Number",
        help_text="Volume number -1 is reserved for chapters that are not in tankobon format yet.",
    )
    chapters = forms.CharField(
        widget=forms.Textarea(),
        help_text="Make sure that each chapter is listed on a separate line. If the chapter has a known name, include it here.. To add an arc starting point use the format '|Story Arc Name'.",
    )
    poster_url = forms.CharField(
        label="Poster URL", help_text="URL to an image file.", required=False
    )
    manga = None

    class Meta:
        model = Volume
        fields = ("absolute_number", "poster_url", "edition", "chapters")

    def __init__(self, manga, *args, **kwargs):
        super(VolumeNewForm, self).__init__(*args, **kwargs)
        self.manga = manga
        self.fields["edition"].queryset = Edition.objects.filter(manga=manga)
        self.fields["edition"].required = True

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            Volume.objects.get(
                absolute_number=cleaned_data["absolute_number"],
                edition=cleaned_data["edition"],
                manga=self.manga,
            )
        except KeyError as exception:
            self.add_error(str(exception).replace("'", ""), "This field is required")
        except Volume.DoesNotExist:
            # The volume does not exist with the given absolute_number, it can be added. Yay!
            pass
        else:
            self.add_error(
                "absolute_number",
                "Volume with this absolute_number already exists for this manga edition",
            )

        return cleaned_data


class EditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = ("manga", "name")
