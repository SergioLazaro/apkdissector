import os

__author__ = 'sergio'
import ConfigParser


class ConfigurationReader:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        self.outputdir = self.ConfigSectionMap("Configuration")['outputdirpath']
        self.version = self.ConfigSectionMap("Configuration")['pscoutversion']
        self.errorlogdir = self.ConfigSectionMap("Configuration")['errorlogpath']
        self.threads = self.ConfigSectionMap("Configuration")['threads']
        self.dbpath = self.ConfigSectionMap("Configuration")['dbpath']
        self.checkEnviroment()
        self.printConfiguration()

    def checkEnviroment(self):
        print "Checking current enviroment..."
        if os.path.isdir(self.outputdir) is False:
            print "Creating folder to write the output in " + self.outputdir
            os.mkdir(self.outputdir,0666)
        if os.path.isdir(self.errorlogdir) is False:
            print "Creating folder to report errors in " + self.errorlogdir
            os.mkdir(self.errorlogdir,0666)
        print "Everything is currently OK..."

    def printConfiguration(self):
        print "====================="
        print "Current configuration"
        print "====================="
        print "Output directory: " + self.outputdir
        print "Threads: " + self.threads
        print "PScout Version: " + self.version
        print "Error log dir: " + self.errorlogdir
        print "DB path: " + self.dbpath
        print "====================="


    def ConfigSectionMap(self,section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

