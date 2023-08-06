'''
Custom Crowdstrike library
--------------------------
Methods for API calls about Host
https://assets.falcon.us-2.crowdstrike.com/support/api/swagger-us2.html#/hosts
'''
import json

def DevicesQueriesDevices(self, query):
    '''/devices/queries/devices/v1'''
    return json.loads(self.GetAPI("devices/queries/devices/v1?"+query))

def DevicesEntitiesDevices(self, ids):
    '''/devices/entities/devices/v1'''
    Param = ""
    for ids in ids:
        Param += "ids="+ids+"&"    
    return json.loads(self.GetAPI("devices/entities/devices/v1?"+Param))

def SensorsQueriesInstallersCcid(self):
    '''sensors/queries/installers/ccid/v1'''
    return json.loads(self.GetAPI("sensors/queries/installers/ccid/v1"))

def DevicesCombinedDevicesLoginhistory(self, DeviceList):
    '''/devices/combined/devices/login-history/v1'''
    return json.loads(self.PostAPI("devices/combined/devices/login-history/v1", ({"ids": DeviceList}) ))

def DevicesCombinedDevicesNetworkAddressHistory(self, DeviceList):
    '''/devices/combined/devices/network-address-history/v1'''
    return json.loads(self.PostAPI("devices/combined/devices/network-address-history/v1", ({"ids": DeviceList}) ))

# Ioc
def IndicatorsQueriesDevices(self, payload):
    '''/indicators/queries/devices/v1'''
    return json.loads(self.GetAPI("indicators/queries/devices/v1?"+payload))

# Intel
def MalqueryEntitiesMetadata(self, ids):
    '''/malquery/entities/metadata/v1'''
    Param = ""
    for ids in ids:
        Param += "ids="+ids+"&"    
    return json.loads(self.GetAPI("devices/entities/devices/v1?"+Param))
