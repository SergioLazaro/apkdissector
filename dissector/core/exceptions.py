__author__ = 'sergio'

import traceback
from logger import Logger

class ZIPException:

    def __init__(self,errorfilepath,apkname):
        self.errorfilepath = errorfilepath
        self.logger = Logger(errorfilepath)
        self.apkname = apkname
        self.write_errorlog()

    def write_errorlog(self):
        self.logger.write("[!!] Error appeared analyzing " + self.errorfilepath)
        err = traceback.format_exc()
        self.logger.write(str(err))
        self.logger.close()