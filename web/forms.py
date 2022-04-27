from django import forms
from api.models import Manga, Volume
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Sign Up Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2', 
            ]

class MangaForm(forms.ModelForm):
    start_date = forms.DateField(help_text='Format: YYYY-MM-DD')
    poster = forms.CharField(label='Poster URL', help_text='URL to an image file. Try to use an image from AniList or MAL.', required=False)
    banner = forms.CharField(label='Banner URL', help_text='URL to an image file. Try to use an image from AniList or MAL.', required=False)
    anilist_id = forms.IntegerField(label='AniList ID', required=False)
    mal_id = forms.IntegerField(label='MyAnimeList ID', required=False)
    mangaupdates_id = forms.IntegerField(label='MangaUpdates ID', required=False)
    anime_planet_slug = forms.CharField(label='Anime Planet Slug', help_text='You can find the Anime Planet slug at the end of the Anime Planet url. Example: https://www.anime-planet.com/manga/anime-planet-slug', required=False)
    kitsu_id = forms.IntegerField(label='Kitsu ID', required=False)

    class Meta:
        model = Manga
        fields = ('name', 'romaji', 'description', 'status', 'start_date', 'poster', 'banner', 'anilist_id', 'mal_id', 'mangaupdates_id', 'anime_planet_slug', 'kitsu_id', 'fandom', 'magazine', 'volume_count')

class VolumeEditForm(forms.ModelForm):
    chapters = forms.CharField(widget=forms.Textarea(), help_text='Make sure that each chapter is listed on a separate line. If the chapter has a known name, include it here. To add an arc starting point use the format \'|Story Arc Name\'.')
    poster = forms.CharField(label='Poster URL', help_text='URL to an image file.', required=False)

    class Meta:
        model = Volume
        fields = ('poster', 'chapters')

class VolumeNewForm(forms.ModelForm):
    absolute_number = forms.IntegerField(label='Volume Number', help_text='Volume number -1 is reserved for chapters that are not in tankobon format yet.')
    chapters = forms.CharField(widget=forms.Textarea(), help_text='Make sure that each chapter is listed on a separate line. If the chapter has a known name, include it here.. To add an arc starting point use the format \'|Story Arc Name\'.')
    poster = forms.CharField(label='Poster URL', help_text='URL to an image file.', required=False)

    class Meta:
        model = Volume
        fields = ('absolute_number', 'poster', 'chapters')

    def clean(self):
        cleaned_data = self.cleaned_data

        try:
            Volume.objects.get(absolute_number=cleaned_data['absolute_number'], manga=self.data['manga'])
        except Volume.DoesNotExist:
            pass
        else:
            raise ValidationError('Volume with this absolute_number already exists for this manga')

        if cleaned_data['absolute_number'] < -1:
            raise ValidationError('Volume Number cannot be less than -1')

        # Always return cleaned_data
        return cleaned_data