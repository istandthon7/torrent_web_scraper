import os
import shutil
import tempfile
import unittest
import osHelper
import stat
from pathlib import Path

class OsHelperTest(unittest.TestCase):
    """윈도우에서 테스트하지 않음"""
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        
    def test_폴더_퍼미션이_None이_아닌지_구하기(self):
        print(Path(self.test_dir).resolve())
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        self.assertIsNotNone(mode)

    def test_폴더_퍼미션이_소유자_읽기쓰기_권한이_있는지_구하기(self):
        print(Path(self.test_dir).resolve())
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        self.assertTrue(osHelper.isPermission(self.test_dir, stat.S_IRUSR))
        self.assertTrue(osHelper.isPermission(self.test_dir, stat.S_IWUSR))
        self.assertTrue(osHelper.isPermission(self.test_dir, stat.S_IRUSR | stat.S_IWUSR))
        self.assertTrue(osHelper.isPermission(self.test_dir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR))
        self.assertTrue(osHelper.isPermission(self.test_dir, stat.S_IRWXU))

    def test_폴더_퍼미션이_그룹_읽기쓰기_권한이_있는지_구하기(self):
        if os.name == 'nt':  # Windows
            return
        else:
            # 폴더를 만들면 기본 755
            dir = "dirtest2"
            os.mkdir(dir)
            print(Path(dir).resolve())
            mode = osHelper.getPermission(dir)
            print(stat.filemode(mode))
            self.assertTrue(osHelper.isPermission(dir, stat.S_IRGRP))
            self.assertFalse(osHelper.isPermission(dir, stat.S_IWGRP))
            self.assertFalse(osHelper.isPermission(dir, stat.S_IRGRP | stat.S_IWGRP))
            self.assertFalse(osHelper.isPermission(dir, stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP))
            self.assertFalse(osHelper.isPermission(dir, stat.S_IRWXG))

    def test_폴더_퍼미션이_other_읽기실행_권한이_있는지_구하기(self):
        if os.name == 'nt':  # Windows
            return
        dir = "dirtest"
        os.mkdir(dir)
        print(Path(dir).resolve())
        mode = osHelper.getPermission(dir)
        print(stat.filemode(mode))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IROTH))
        #self.assertTrue(osHelper.isPermission(dir, stat.S_IWOTH))
        self.assertTrue(osHelper.isPermission(dir, stat.S_IROTH | stat.S_IXOTH))
        self.assertFalse(osHelper.isPermission(dir, stat.S_IWOTH))
        shutil.rmtree(dir)

    def test_폴더_퍼미션이_전체권한이_없는지(self):
        if os.name == 'nt':  # Windows
            return
        print(Path(self.test_dir).resolve())
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(self.test_dir, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG))

    def test_폴더_퍼미션이_other에_전체권한이_없는지(self):        
        if os.name == 'nt':  # Windows
            return
        print(Path(self.test_dir).resolve())
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(self.test_dir, stat.S_IRWXO))

    def test_폴더_퍼미션이_group에_전체권한이_없는지(self):
        if os.name == 'nt':  # Windows
            return
        print(Path(self.test_dir).resolve())
        osHelper.removePermission(self.test_dir, stat.S_IWGRP)
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(self.test_dir, stat.S_IRWXG))

    def test_폴더_퍼미션이_other에_쓰기권한이_없는지(self):
        if os.name == 'nt':  # Windows
            return
        print(Path(self.test_dir).resolve())
        osHelper.removePermission(self.test_dir, stat.S_IWOTH)
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(self.test_dir, stat.S_IWOTH))

    def test_폴더_퍼미션이_user에_쓰기권한이_없는지(self):
        if os.name == 'nt':  # Windows
            return
        print(Path(self.test_dir).resolve())
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        osHelper.removePermission(self.test_dir,stat.S_IWUSR)
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(self.test_dir, stat.S_IWUSR))

    def test_폴더_퍼미션이_group에_쓰기권한이_없는지(self):
        if os.name == 'nt':  # Windows
            return
        print(Path(self.test_dir).resolve())
        osHelper.removePermission(self.test_dir,stat.S_IWGRP)
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        self.assertFalse(osHelper.isPermission(self.test_dir, stat.S_IWGRP))

    def test_현재폴더_appendPermission(self):
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        if osHelper.isPermission(self.test_dir, stat.S_IWOTH) is False:
            osHelper.appendPermisson(self.test_dir, stat.S_IWOTH)
        else:
            osHelper.removePermission(self.test_dir, stat.S_IWOTH)
            osHelper.appendPermisson(self.test_dir, stat.S_IWOTH)
        self.assertTrue(osHelper.isPermission(self.test_dir, stat.S_IWOTH))
        mode = osHelper.getPermission(self.test_dir)
        print(stat.filemode(mode))
        osHelper.removePermission(self.test_dir, stat.S_IWOTH)

if __name__ == '__main__':  
    unittest.main()