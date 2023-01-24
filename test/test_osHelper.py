import os
import unittest
import osHelper
import stat
import setting
from pathlib import Path

class OsHelperTest(unittest.TestCase):
    """리눅스에서만 가능"""

    def test_폴더_퍼미션이_None이_아닌지_구하기(self):
        dir = "dirtest"
        os.mkdir(dir)
        print(Path(dir).resolve())
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertIsNotNone(mode)
        os.rmdir(dir)

    def test_폴더_퍼미션이_소유자_읽기쓰기_권한이_있는지_구하기(self):
        dir = "dirtest"
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        else:
            os.rmdir(dir)
            os.mkdir(dir)
        print(Path(dir).resolve())
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IRUSR))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IWUSR))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IRUSR | stat.S_IWUSR))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IRWXU))
        os.rmdir(dir)

    def test_폴더_퍼미션이_그룹_읽기쓰기_권한이_있는지_구하기(self):
        dir = "dirtest"
        os.mkdir(dir)
        print(Path(dir).resolve())
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IRGRP))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IWGRP))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IRGRP | stat.S_IWGRP))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IRWXG))
        os.rmdir(dir)

    def test_폴더_퍼미션이_other_읽기실행_권한이_있는지_구하기(self):
        dir = "dirtest"
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        print(Path(dir).resolve())
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IROTH))
        #self.assertTrue(osHelper.isPermission(dir, stat.S_IWOTH))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IROTH | stat.S_IXOTH))
        self.assertFalse(osHelper.isPermission(dir, stat.S_IWOTH))
        os.rmdir(dir)

    def test_폴더_퍼미션이_전체권한이_없는지(self):
        mySetting = setting.Setting()
        dir = "dirtest"
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        else:
            os.rmdir(dir)
            os.mkdir(dir)
        print(Path(dir).resolve())
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(dir, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG))
        os.rmdir(dir)

    def test_폴더_퍼미션이_other에_전체권한이_없는지(self):
        mySetting = setting.Setting()
        dir = "dirtest"
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        else:
            os.rmdir(dir)
            os.mkdir(dir)
        print(Path(dir).resolve())
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(dir, stat.S_IRWXO))
        os.rmdir(dir)

    def test_폴더_퍼미션이_group에_전체권한이_없는지(self):
        mySetting = setting.Setting()
        dir = "dirtest"
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        else:
            os.rmdir(dir)
            os.mkdir(dir)
        print(Path(dir).resolve())
        osHelper.removePermission(dir, stat.S_IWGRP)
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(dir, stat.S_IRWXG))
        os.rmdir(dir)

    def test_폴더_퍼미션이_other에_쓰기권한이_없는지(self):
        mySetting = setting.Setting()
        dir = "dirtest"
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        else:
            os.rmdir(dir)
            os.mkdir(dir)
        print(Path(dir).resolve())
        osHelper.removePermission(dir, stat.S_IWOTH)
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(dir, stat.S_IWOTH))
        os.rmdir(dir)

    def test_폴더_퍼미션이_user에_쓰기권한이_없는지(self):
        mySetting = setting.Setting()
        dir = "dirtest"
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        else:
            os.rmdir(dir)
            os.mkdir(dir)
        print(Path(dir).resolve())
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        osHelper.removePermission(dir,stat.S_IWUSR)
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(dir, stat.S_IWUSR))
        os.rmdir(dir)

    def test_폴더_퍼미션이_group에_쓰기권한이_없는지(self):
        mySetting = setting.Setting()
        dir = "dirtest"
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        print(Path(dir).resolve())
        osHelper.removePermission(dir,stat.S_IWGRP)
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(dir, stat.S_IWGRP))
        os.rmdir(dir)

    def test_현재폴더_appendPermission(self):
        
        dir = "dirtest"
        os.mkdir(dir)
        mySetting = setting.Setting()
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        if osHelper.isPermission(dir, stat.S_IWOTH) is False:
            osHelper.appendPermisson(dir, stat.S_IWOTH)
        else:
            osHelper.removePermission(dir, stat.S_IWOTH)
            osHelper.appendPermisson(dir, stat.S_IWOTH)
        self.assertTrue(osHelper.isPermission(dir, stat.S_IWOTH))
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        osHelper.removePermission(dir, stat.S_IWOTH)
        os.rmdir(dir)

if __name__ == '__main__':  
    unittest.main()