import shutil
import os
from pathlib import Path

def copy_addons(wow_path):

    source_addons = Path(wow_path).joinpath('Interface/AddOns')
    source_config = Path(wow_path).joinpath('WTF')
    dst_addons = Path(__file__).parent.absolute().joinpath('wow-addons/AddOns')
    dst_config = Path(__file__).parent.absolute().joinpath('wow-addons/WTF')

    if os.path.exists(dst_addons):
        shutil.rmtree(dst_addons)

    if os.path.exists(dst_config):
        shutil.rmtree(dst_config)

    shutil.copytree(source_addons, dst_addons)  
    shutil.copytree(source_config, dst_config)