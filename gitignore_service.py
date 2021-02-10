base_gitignore = """
*

!WTF
!WTF/*

"""


def include_addons():
    base_gitignore += "!Interface/Addons/**\n"


def include_general_settings():
    base_gitignore += "!WTF/Config.wtf\n"

def include
