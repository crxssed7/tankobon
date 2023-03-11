from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from api.models import Manga, Volume, Edition, Collection

from web.mixins.forms import HiddenFieldsMixin, StyledFieldsMixin


class SignUpForm(StyledFieldsMixin, UserCreationForm):
    template_name = "web/form_snippet.html"

    email = forms.EmailField(max_length=254, help_text="Enter a valid email address")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class LoginForm(StyledFieldsMixin, AuthenticationForm):
    template_name = "web/form_snippet.html"

    class Meta:
        model = User
        fields = ["username", "password"]


class MangaForm(StyledFieldsMixin, forms.ModelForm):
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


class VolumeForm(StyledFieldsMixin, HiddenFieldsMixin, forms.ModelForm):
    template_name = "web/form_snippet.html"

    hidden_fields = ["absolute_number", "edition", "poster_url", "isbn", "page_count", "release_date"]

    release_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    page_count = forms.IntegerField(label="Page Count")
    isbn = forms.CharField(label="ISBN (10/13)")
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
        fields = ["absolute_number", "poster_url", "edition", "chapters", "isbn", "page_count", "release_date"]

    def __init__(self, manga, *args, **kwargs):
        super(VolumeForm, self).__init__(*args, **kwargs)
        self.manga = manga
        if not self.is_editing():
            self.fields["edition"].queryset = Edition.objects.filter(manga=manga)
            self.fields["edition"].required = True
        else:
            self.fields.pop("absolute_number", None)
            self.fields.pop("edition", None)

    def is_editing(self):
        return self.instance.pk is not None

    def conditional(self):
        if self.is_editing():
            return self.instance and self.instance.absolute_number < 0
        return False

    def clean(self):
        cleaned_data = self.cleaned_data
        absolute_number = self.cleaned_data.get("absolute_number")
        edition = self.cleaned_data.get("edition")

        if not self.is_editing() and absolute_number is not None and edition is not None:
            try:
                Volume.objects.get(
                    absolute_number=absolute_number,
                    edition=edition,
                    manga=self.manga,
                )
            except Volume.DoesNotExist:
                # The volume does not exist with the given absolute_number, it can be added. Yay!
                pass
            else:
                self.add_error(
                    "absolute_number",
                    "Volume with this absolute_number already exists for this manga edition",
                )

        return cleaned_data


class EditionForm(StyledFieldsMixin, forms.ModelForm):
    template_name = "web/form_snippet.html"

    class Meta:
        model = Edition
        fields = ("manga", "language", "name")

class CollectionCollectedAtForm(forms.ModelForm):
    template_name = "web/form_snippet.html"

    collected_at = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}), label="You collected this volume on:")

    def __init__(self, *args, **kwargs):
        super(CollectionCollectedAtForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(ATTRS)

    class Meta:
        model = Collection
        fields = ("collected_at",)


class CollectionForm(forms.Form):
    template_name = "web/form_snippet.html"

    isbn = forms.CharField(max_length=20, label="ISBN")
    collected_at = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))

    def __init__(self, user, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.user = user
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(ATTRS)

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn'].replace("-", '')

        try:
            volume = Volume.objects.get(isbn=isbn, absolute_number__gt=-1)
        except Volume.DoesNotExist:
            raise forms.ValidationError('No volume found with ISBN {}'.format(isbn))
        self.volume = volume

        exists = Collection.objects.filter(user=self.user, volume=volume).exists()
        if exists:
            raise forms.ValidationError('You already have this volume in your collection.')

        return isbn

    def save(self):
        return Collection.objects.create(user=self.user, volume=self.volume, collected_at=self.cleaned_data['collected_at'])
