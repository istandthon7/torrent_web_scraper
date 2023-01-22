import os
import logging
import stat

def setPermisson(path:str, newMode):
    if os.path.exists(path) is False:
        logging.info(f'폴더에 권한을 추가하려고 했으나 폴더가 없네요. {path}')
        return;
    stat = os.lstat(path)
    mode = stat.st_mode

    logging.info(f'[{path}]의 소유자 PUID: {stat.st_uid}, PGID: {stat.st_gid}, mode: [{mode}]')
    
    #if (mode & newMode) != newMode:
    os.chmod(path, mode|newMode)
    logging.info(f'폴더에 권한을 추가했습니다. {newMode}')

def addXToUser(path: str):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)