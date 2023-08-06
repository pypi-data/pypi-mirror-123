#!/usr/bin/python3

from .utillity import *
import os,subprocess
import logging,sys

class filemime:
    def __init__(self):
        self.realPath = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
        self.exec = self.assginExec()
        if self.exec == None:
            logging.error("Not Find Excuteble File")
    
    def assginExec(self):
        fileExec = None
        try:
            if sys.platform == WIN32:
                usrFolder = os.path.join(self.realPath,USR,BIN)
                fileExec = os.path.join(usrFolder,EXEC_FILE)
        except Exception as e:
            logging.error(e)
        return fileExec

    def load_file(self,filePath,mimeType=False):
        try:
            if not os.path.isfile(filePath):
                return None
            if mimeType == False:
                cmd = EXEC_DSC.format(self.exec,filePath)
            elif mimeType == True:
                cmd = EXEC_MIMETYPE.format(self.exec,filePath)
            else:
                return None
            comm = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if comm.stderr == b"":
                out = comm.stdout.decode("utf-8")
                splitColan = out.replace("\n","").split(":",1)
                if len(splitColan) == 2:
                    return splitColan[1].lstrip()
        except Exception as e:
            logging.error(e)