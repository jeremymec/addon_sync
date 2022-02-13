base_gitignore = """
*

!Interface
!Interface/AddOns/

!WTF
!WTF/*
!WTF/Account
!WTF/Account/*/
!WTF/Account/*/SavedVariables
!WTF/Account/*/*/
!WTF/Account/*/*/*/
!WTF/Account/*/*/*/SavedVariables


"""

def create_gitignore_including(including):
    for group in including:
        if group == "Addons":
            include_addons()
        elif group == "AddonSettings":
            include_addon_settings()
        elif group == "GeneralSettings":
            include_general_settings()
        elif group == "InterfaceSettings":
            include_interface_settings()
        elif group == "AddonsEnabled":
            include_addons_enable_disable()

    return base_gitignore
        
def include_addons():
    global base_gitignore
    base_gitignore += "!Interface/AddOns/**\n"

def include_addon_settings():
    global base_gitignore
    base_gitignore += "!WTF/Account/*/SavedVariables/**\n"
    base_gitignore += "!WTF/Account/*/*/*/SavedVariables/**\n"

def include_general_settings():
    global base_gitignore
    base_gitignore += "!WTF/Config.wtf\n"

def include_keybindings():
    global base_gitignore
    base_gitignore += "!WTF/Account/*/bindings-cache.wtf\n"

def include_addons_enable_disable():
    global base_gitignore
    base_gitignore += "!WTF/Account/*/*/*/AddOns.txt\n"

def include_interface_settings():
    global base_gitignore
    base_gitignore += "!WTF/Account/*/*/*/chat-cache.txt\n"
    base_gitignore += "!WTF/Account/*/*/*/config-cache.wtf\n"
    base_gitignore += "!WTF/Account/*/*/*/config-cache.old\n"

