from libgravatar import Gravatar

from tankobon.settings import TANKOBON_LOGS


def get_user_image(email) -> str:
    gravatar = Gravatar(email)
    image = gravatar.get_image(default="retro")
    return image