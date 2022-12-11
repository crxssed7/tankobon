from libgravatar import Gravatar


def get_user_image(email) -> str:
    gravatar = Gravatar(email)
    image = gravatar.get_image(default="retro")
    return image
