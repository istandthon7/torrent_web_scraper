import unittest
import shutil
import os
import scraperInstaller


class ScraperInstallerTest(unittest.TestCase): 

    # def setUp(self):
    #     self.mySetting = setting.Setting(configDir="config_test")
    #     if not os.path.exists(self.mySetting.configDirPath):
    #         os.makedirs(self.mySetting.configDirPath)
    #     self.installer = scraperInstaller.ScraperInstaller()

    # def tearDown(self):
    #     if os.path.exists(self.mySetting.configDirPath):
    #         shutil.rmtree(self.mySetting.configDirPath)

    def test_copyConfigIfNotExist_파일이_없을때(self):
        # arrange
        currentPath = os.path.realpath(os.path.dirname(__file__))
        testPath = os.path.join(currentPath, "config_test", "setting.json")
        # action
        if os.path.isfile(testPath):
            os.remove(testPath)
        # assert
        installer = scraperInstaller.ScraperInstaller()
        self.assertTrue(installer.copyFileIfNotExist(testPath))
        dirPath = os.path.dirname(testPath)
        if os.path.exists(dirPath):
            shutil.rmtree(dirPath)

    def test_copyConfigIfNotExist_파일이_있을때(self):
        # arrange
        currentPath = os.path.realpath(os.path.dirname(__file__))
        testPath = os.path.join(currentPath, "config_test", "setting.json")
        dirPath = os.path.dirname(testPath)
        # action
        if os.path.isfile(testPath) is False:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            with open(testPath, 'w') as f:
                f.close()
        # assert
        installer = scraperInstaller.ScraperInstaller()
        self.assertFalse(installer.copyFileIfNotExist(testPath))
        if os.path.exists(dirPath):
            shutil.rmtree(dirPath)

    def test_installConfig_폴더가_없으면_생성되나(self):
        # arrange
        installer = scraperInstaller.ScraperInstaller(configDir="config_test")
        if os.path.isdir(installer.mySetting.configDirPath):
            shutil.rmtree(installer.mySetting.configDirPath)
        # action 
        installer.installConfig()
        #assert
        self.assertTrue(os.path.isdir(installer.mySetting.configDirPath))
        if os.path.exists(installer.mySetting.configDirPath):
            shutil.rmtree(installer.mySetting.configDirPath)

    def test_installTransmissionScript_폴더가_없으면_생성되나(self):
        # arrange
        installer = scraperInstaller.ScraperInstaller(configDir="config_test")
        if os.path.isdir(installer.mySetting.transmissionScriptDirPath):
            shutil.rmtree(installer.mySetting.transmissionScriptDirPath)
        # action 
        installer.installTransmissionScript()
        #assert
        self.assertTrue(os.path.isdir(installer.mySetting.transmissionScriptDirPath))

if __name__ == '__main__':  
    unittest.main()
