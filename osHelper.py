import argparse
import os
import logging
import stat
import setting

def appendPermisson(path:str, appendMode):
    '''appendMode(oct): stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG'''
    if os.path.exists(path) is False:
        logging.warning(f'폴더가 없어 권한을 추가하지 않아요. {path}')
        return;

    mode = getPermission(path)
    
    if (mode & appendMode) == appendMode:
        logging.debug(f'폴더에 이미 권한이 있어요. [{path}] {stat.filemode(appendMode)}')
        return;

    os.chmod(path, mode|appendMode)
    logging.info(f'폴더에 권한을 추가했습니다. [{path}] {stat.filemode(appendMode)}')

def removePermission(path:str, removeMode):
    if os.path.exists(path) is False:
        logging.warning(f'폴더가 없어 권한을 삭제하지 않아요. {path}')
        return;
    mode = getPermission(path)
    if ((mode & removeMode) == removeMode) is False:
        logging.debug(f'폴더에 권한이 이미 없어 권한을 삭제하지 않아요. [{path}] {stat.filemode(removeMode)}')
        return;
    logging.info(f'폴더에 권한을 삭제합니다. [{path}] 폴더권한: {stat.filemode(mode)} 삭제권한: {stat.filemode(removeMode)}')
    os.chmod(path, mode & ~removeMode)

def getPermission(path:str):
    if os.path.exists(path) is False:
        logging.warning(f'폴더가 없네요. {path}')
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

def changeOwner(path: str, uid: int, gid: int):
    os.chown(path, uid, gid)
    logging.info(f'폴더 소유자를 변경했어요. {path}, puid: {uid}, pgid: {gid}')

def getUid(path: str) -> int:
    return os.stat(path).st_uid

def getGid(path: str) -> int:
    return os.stat(path).st_gid

def isOwner(path: str, uid: int, gid: int) -> bool:
    if os.path.exists(path) is False:
        logging.warning(f'폴더가 없네요. {path}')
        return;
    if uid == getUid(path) and gid == getGid(path):
        return True
    return False

def setOwnerRwxPermission(path: str, puid: int , pgid: int, permissions: str):
    if puid is not None and pgid is not None:
        logging.debug('폴더 소유자를 설정합니다.')
        if isOwner(path, puid, pgid) is False:
            changeOwner(path, puid, pgid)
            logging.info(f'폴더 소유자를 설정했어요. [{path}], puid: [{puid}], pgid: [{pgid}]')
    if permissions is not None:
        permission = stat.S_IRUSR
        if permissions[0] == '-':
            removePermission(path, permission)
        else:
            appendPermisson(path, permission)
        permission = stat.S_IWUSR
        if permissions[1] == '-':
            removePermission(path, permission)
        else:
            appendPermisson(path, permission)
        permission = stat.S_IXUSR
        if permissions[2] == '-':
            removePermission(path, permission)
        else:
            appendPermisson(path, permission)
        permission = stat.S_IRGRP
        if permissions[3] == '-':
            removePermission(path, permission)
        else:
            appendPermisson(path, permission)
        permission = stat.S_IWGRP
        if permissions[4] == '-':
            removePermission(path, permission)
        else:
            appendPermisson(path, permission)
        permission = stat.S_IXGRP
        if permissions[5] == '-':
            removePermission(path, permission)
        else:
            appendPermisson(path, permission)
        permission = stat.S_IROTH
        if permissions[6] == '-':
            removePermission(path, permission)
        else:
            appendPermisson(path, permission)
        permission = stat.S_IWOTH
        if permissions[7] == '-':
            removePermission(path, permission)
        else:
            appendPermisson(path, permission)
        permission = stat.S_IXOTH
        if permissions[8] == '-':
            removePermission(path, permission)
        else:
            appendPermisson(path, permission)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="설정할 경로")
    parser.add_argument("--puid", help="puid", type=int)
    parser.add_argument("--pgid", help="pgid", type=int)
    parser.add_argument("--permission", help="permission(ex: rwxr-xr-x)")
    args = parser.parse_args()
    # 로그 초기화
    mySetting = setting.Setting()
    setOwnerRwxPermission(args.path, args.puid, args.pgid, args.permission)

    