import io
import requests

from django.core.files.images import ImageFile


class RemoteImageFieldMixin:
    def get_remote_banner(self):
        if self.banner_url:
            result = requests.get(self.banner_url)
            if result.status_code == 200:
                content_type = result.headers.get("Content-Type")
                if content_type and content_type.startswith("image/"):
                    ext = content_type.split("/")[-1]
                    self.banner_file.delete(save=False)
                    image = ImageFile(
                        io.BytesIO(result.content),
                        name=self.banner_file_name(ext=ext),
                    )
                    self.banner_file = image
                else:
                    self.banner_url = ""
        else:
            if self.banner_file:
                self.banner_file.delete(save=False)

    def get_remote_poster(self):
        if self.poster_url:
            result = requests.get(self.poster_url)
            if result.status_code == 200:
                content_type = result.headers.get("Content-Type")
                if content_type and content_type.startswith("image/"):
                    ext = content_type.split("/")[-1]
                    self.poster_file.delete(save=False)
                    image = ImageFile(
                        io.BytesIO(result.content),
                        name=self.poster_file_name(ext=ext),
                    )
                    self.poster_file = image
                else:
                    self.banner_url = ""
        else:
            if self.poster_file:
                self.poster_file.delete(save=False)

    def banner_file_name(self, ext):
        raise NotImplementedError()

    def poster_file_name(self, ext):
        raise NotImplementedError()
