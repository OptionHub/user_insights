import requests, sys, os, json, time
from datetime import datetime, timedelta
import logging
import asyncio
import utilities.util as utilInstance
import utilities.qsAPI as qsAPI
import regex
import socket

log = logging.getLogger('appDeploy')
util = utilInstance.Util(log)

async def deployTask(util, config, qlikPackageDir, clientKey):
    print("Started deployment process for client:", clientKey)
    _proxy = config[clientKey]['proxy']
    _vProxy = config[clientKey]['vProxy']

    uploadAppName = config[clientKey]['templateApp']['name']
    destinationAppID = config[clientKey]['templateApp']['replaceAppID']
    destinationStreamID = config[clientKey]['streamId']
    '''***********Initiate deployment process configure framework*********
    '''
    #******************Qlik QRS GET session request*******************

    # qrs=qsAPI.QRS(proxy=_proxy, vproxy=_vProxy)
    qrs=qsAPI.QRS(proxy=_proxy, vproxy=_vProxy, user={'userDirectory':'PRECIMA', 'userID':'qservicess'})

    ##************Starting the initial upload process with qvf argument ************
    qvfFile = util.readQVF(qlikPackageDir)
    responseUpload = qrs.AppUpload(filename=qvfFile, pName=uploadAppName)
    importedAppId = responseUpload.json()['id']
    print("Upload app{", importedAppId, "} successful for client:", clientKey)
    await asyncio .sleep(0)
    ##************Starting the reload process for the now replaced app *************
    responseReloadApp = qrs.AppReload(importedAppId)
    print("Reload task started for client", clientKey)

    if await qrs.isReloadSuccess(importedAppId, 10): # change wait time for existing app last reload duration as reference input
        print("Successful reload app{", importedAppId, "} finished at UTC", qrs.getAppReloadResult(importedAppId)['stopTime'], "for client:", clientKey) #qrs.getAppLastReloadTime(importedAppId))
    else:
        print("Reload app{", importedAppId, "} failed, status code:", qrs.getAppReloadResult(importedAppId)['status'], "for client:", clientKey)
        responseDeleteLocalApp = qrs.AppDelete(importedAppId)
        print("Delete app{", importedAppId, "} result: ", responseDeleteLocalApp.status_code, ".............Done", "for client:", clientKey)
        importedAppId = None
    ##************Starting the replacement process by fetching id from upload response with appID in config { TO BE CHANGED BASED ON PROJECT }
    await asyncio .sleep(0)
    if importedAppId is not None:
        if not destinationAppID:
            responsePublishApp = qrs.appPublish(importedAppId, destinationAppID).json()
            if responsePublishApp['published']:
                config[clientKey]['templateApp']['replaceAppID'] = responsePublishApp['id']
                print("Publish app {", importedAppId, "} at UTC", responsePublishApp['publishTime'], "..........Done", "for client:", clientKey)
            else:
                responseReloadApp = qrs.AppReplace(importedAppId, destinationAppID)
                responseDeleteLocalApp = qrs.AppDelete(importedAppId)
                print("Delete app {", importedAppId, "} result: ", responseDeleteLocalApp.status_code, "............Done", "for client:", clientKey)
                print("Replace app {", importedAppId, "} result:", responseReplaceApp.status_code, "............Done", "for client", clientKey)
            ##*********************Delete app imported in the personal stream****************




async def main():
    # Directory of the python module
    _pyFileDir = os.path.dirname(os.path.abspah(__file__))
    # Directory of Qlik package
    qlikPackageDir = os.path.dirname(_pyFileDir)
    config = util.getConfigFile(_pyFileDir)
    deployClientList = []
    for key, _clientConfig in config.items():
        if regex.search(socket.gethostname().upper(), _clientConfig['proxy'].upper()):
            print(key, 'deploy config matches with current host name - ', _clientConfig['proxy'])
            deployClientList.append(key)

    print('Deployment client list:', deployClientList)

    tasks = []
    for clientKey in deployClientList:
        tasks.append(deployTask(util, config, qlikPackageDir, clientKey))

    await asyncio.wait(tasks, return_when='ALL_COMPLETED')

    # Update config file with published app id
    util.updateConfigFile(_pyFileDir, config)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
