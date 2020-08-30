#python3
#encoding: utf-8
#backup.py - cria backup dos arquivos de determinada pasta

import os, shelve, shutil

######################################
#Codigo no cliente
clientName = 'client'
clientFolder = os.path.join(os.getcwd(),clientName)

#Recupera o nome dos arquivos e a ultima modificação no cliente
def getFolderInfo():
    info = {}
    for folderName, subfolders, filenames in os.walk(clientFolder):
            for filename in filenames:
                lastModified = os.path.getmtime(f'{folderName}/{filename}')
                file = {filename:lastModified}
                info.update(file)
    return info

##########################################
#Código do servidor
backupLog = shelve.open('backupLog')
requestToDelete = []
requestToAdd = []

folderName = 'backup'
backupFolder = os.path.join(os.getcwd(),folderName)

def backupActions():
    #Abre arquivos no backup
    #Le nome dos arquivos armazenados no backup
    backupLogFiles = list(backupLog.keys())        
    for filename in backupLogFiles:
        #Checa se arquivo existente no backup tambem existe no cliente
        if(clientFolderBlueprint.get(filename)):
            #Checa se o arquivo no cliente foi modificado
            if(clientFolderBlueprint[filename] != backupLog[filename]):
                requestToDelete.append(filename)
                requestToAdd.append(filename)
                backupLog[filename] = clientFolderBlueprint[filename]
        else:
            requestToDelete.append(filename)
            del backupLog[filename]
    #Checa quais arquivos devem ser adicionadors ao backup
    toBeAdded = clientFolderBlueprint.keys() - backupLogFiles
    requestToAdd.extend(list(toBeAdded))
    print(requestToAdd)
    print(requestToDelete)
#Adiciona os arquivos a pasta de backup -- simulação da ação do servidor ao recever os arquivos atualizados do cliente
def sendToBackupFolder():
    for filesToAdd in requestToAdd:
        shutil.copy2(os.path.join(clientFolder,filesToAdd),os.path.join(backupFolder,filesToAdd))
        backupLog[filesToAdd] = clientFolderBlueprint[filesToAdd]
#Remove arquivos da pasta backup e atualiza historico 
def manageBackupHistory():
    for filesToDelele in requestToDelete:
        os.unlink(os.path.join(backupFolder,filesToDelele))
        del backupLog[filesToDelele]
########################################
#Execução do programa
#Checa se pasta existe
if not os.path.exists(folderName):
    os.makedirs(folderName)
if not os.path.exists(folderName):
    os.makedirs(clientName)
#Execução do programa
clientFolderBlueprint = getFolderInfo()
backupActions()
sendToBackupFolder()
manageBackupHistory()
backupLog.close()

