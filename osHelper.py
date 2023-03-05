import os
import logging
import stat

def appendPermisson(path:str, appendMode):
    
    if os.path.exists(path) is False:
        logging.warn(f'폴더가 없어 권한을 추가하지 않아요. {path}')
        return;

    mode = getPermission(path)
    
    if (mode & appendMode) == appendMode:
        logging.info(f'폴더에 이미 권한이 있어요. [{path}] {stat.filemode(appendMode)}')
        return;

    os.chmod(path, mode|appendMode)
    logging.info(f'폴더에 권한을 추가했습니다. [{path}] {stat.filemode(appendMode)}')

def removePermission(path:str, removeMode):
    if os.path.exists(path) is False:
        logging.warn(f'폴더가 없어 권한을 삭제하지 않아요. {path}')
        return;
    mode = getPermission(path)
    if ((mode & removeMode) == removeMode) is False:
        logging.info(f'폴더에 권한이 이미 없어 권한을 삭제하지 않아요. [{path}] {stat.filemode(removeMode)}')
        return;
    logging.info(f'폴더에 권한을 삭제합니다. [{path}] 폴더권한: {stat.filemode(mode)} 삭제권한: {stat.filemode(removeMode)}')
    os.chmod(path, mode & ~removeMode)

def getPermission(path:str):
    if os.path.exists(path) is False:
        logging.warn(f'폴더가 없네요. {path}')
        return;
    stat = os.lstat(path)
    logging.debug(f'[{path}]의 소유자 PUID: {stat.st_uid}, PGID: {stat.st_gid}]')
    return stat.st_mode

def isPermission(path:str, mode):
    currentMode = getPermission(path)
    if currentMode is None:
        return False;
    logging.debug(f'폴더에 권한을 체크합니다. [{path}] 폴더권한: {stat.filemode(currentMode)}, 체크권한: {stat.filemode(mode)}')
    return (currentMode & mode)==mode

def addXToUser(path: str):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)