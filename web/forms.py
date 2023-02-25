from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from api.models import Manga, Volume, Edition

ATTRS = {"class": "w-full rounded focus:border-hint focus:ring-hint bg-blay border-whay hover:border-hint transition duration-300 ease-in-out"}


class SignUpForm(UserCreationForm):
    template_name = "web/form_snippet.html"

    email = forms.EmailField(max_length=254, help_text="Enter a valid email address")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(ATTRS)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    template_name = "web/form_snippet.html"

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(ATTRS)

    class Meta:
        model = User
        fields = ["username", "password"]


class MangaForm(forms.ModelForm):
    template_name = "web/form_snippet.html"

    # start_date = forms.DateField(help_text='Format: YYYY-MM-DD')
    start_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    tags = forms.CharField(
        label="Tags", help_text="Comma seperated list of tags.", required=False
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

    def __init__(self, *args, **kwargs):
        super(MangaForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(ATTRS)

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
    template_name = "web/form_snippet.html"

    release_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}), required=False)
    chapters = forms.CharField(
        widget=forms.Textarea(),
        help_text="Make sure that each chapter is listed on a separate line. If the chapter has a known name, include it here. To add an arc starting point use the format '|Story Arc Name'.",
    )
    poster_url = forms.CharField(
        label="Poster URL", help_text="URL to an image file.", required=False
    )

    def __init__(self, *args, **kwargs):
        super(VolumeEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(ATTRS)

    class Meta:
        model = Volume
        fields = ("poster_url", "chapters", "isbn", "page_count", "release_date")


class VolumeNewForm(forms.ModelForm):
    template_name = "web/form_snippet.html"

    release_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}), required=False)
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
        fields = ("absolute_number", "poster_url", "edition", "chapters", "isbn", "page_count", "release_date")

    def __init__(self, manga, *args, **kwargs):
        super(VolumeNewForm, self).__init__(*args, **kwargs)
        self.manga = manga
        self.fields["edition"].queryset = Edition.objects.filter(manga=manga)
        self.fields["edition"].required = True
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(ATTRS)

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
    template_name = "web/form_snippet.html"

    class Meta:
        model = Edition
        fields = ("manga", "language", "name")

    def __init__(self, *args, **kwargs):
        super(EditionForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(ATTRS)
