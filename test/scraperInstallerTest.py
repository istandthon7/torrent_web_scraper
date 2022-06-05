import unittest
import os
import scraperInstaller
import setting

class ScraperInstallerTest(unittest.TestCase): 

    def test_copyConfigIfNotExist_파일이_없을때(self):
        # arrange
        mySetting = setting.Setting()
        if os.path.isfile(mySetting.settingPath):
            os.remove(mySetting.settingPath)
        # action
        installer = scraperInstaller.ScraperInstaller()
        
        # assert
        self.assertTrue(installer.copyConfigIfNotExist(mySetting.settingPath))

    def test_copyConfigIfNotExist_파일이_있을때(self):
        # arrange
        mySetting = setting.Setting()
        if os.path.isfile(mySetting.settingPath) is False:
            with open(mySetting.settingPath, 'w') as f:
                f.close()
        # action
        installer = scraperInstaller.ScraperInstaller()
        
        # assert
        self.assertFalse(installer.copyConfigIfNotExist(mySetting.settingPath))

if __name__ == '__main__':  
    unittest.main()