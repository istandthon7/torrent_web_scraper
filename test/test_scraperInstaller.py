import unittest
import shutil
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

    def test_installConfig_폴더가_없으면_생성되나(self):
        # arrange
        mySetting = setting.Setting()
        installer = scraperInstaller.ScraperInstaller()
        if os.path.isdir(mySetting.configDirPath):
            shutil.rmtree(mySetting.configDirPath)
        # action 
        installer.installConfig()
        #assert
        self.assertTrue(os.path.isdir(mySetting.configDirPath))

    def test_installTransmissionScript_폴더가_없으면_생성되나(self):
        # arrange
        mySetting = setting.Setting()
        installer = scraperInstaller.ScraperInstaller()
        if os.path.isdir(mySetting.transmissionScriptDirPath):
            shutil.rmtree(mySetting.transmissionScriptDirPath)
        # action 
        installer.installTransmissionScript()
        #assert
        self.assertTrue(os.path.isdir(mySetting.transmissionScriptDirPath))
if __name__ == '__main__':  
    unittest.main()