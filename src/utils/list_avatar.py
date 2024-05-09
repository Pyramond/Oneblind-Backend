from os import listdir


def list_avatar():
    files = listdir("./static/avatars")
    avatar = [file for file in files if file.endswith(".png")]
    return avatar
