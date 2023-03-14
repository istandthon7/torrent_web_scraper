import unittest
import rpc
import setting

# 51413 -> 41413 isp등에 의해 막힌 경우
# docker run -d --name=transmission -e TZ=Asia/Seoul -p 9091:9091 -p 41413:41413 -p 41413:41413/udp -e PUID=1000 -e PGID=1000 -e USER=transmission -e PASS=transmission lscr.io/linuxserver/transmission

class RpcTest(unittest.TestCase):
    def test_sessionID(self):
        mySetting = setting.Setting()
        # 더미 호스트
        mySetting.json["transmission"]["host"] = "555.168.0.1"
        mySetting.json["transmission"]["port"] = 9091
        mySetting.json["transmission"]["id"] = "transmission"
        mySetting.json["transmission"]["pw"] = "transmission"
        sessionId = rpc.getSessionIdTransRpc(mySetting.getRpcUrl())
        self.assertIsNone(sessionId)

    # def test_sessionIDOfConfigFile(self):
    #     ''' 수정해야 '''
    #     mySetting = setting.Setting()
    #     sessionId = rpc.getSessionIdTransRpc(mySetting.getRpcUrl())
    #     self.assertIsNotNone(sessionId)
    
    def test_패스워드가_다르면(self):
        mySetting = setting.Setting()
        mySetting.json["transmission"]["pw"] = "5555"
        url = mySetting.getRpcUrl()
        sessionId = rpc.getSessionIdTransRpc(url)
        self.assertIsNone(sessionId)

if __name__ == '__main__':  
    unittest.main()