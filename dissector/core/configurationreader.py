__author__ = 'sergio'
import ConfigParser, os


class ConfigurationReader:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        self.outputdir = self.config.options("Configuration")[0]
        self.version = self.config.options("Configuration")[1]
        self.errorlog = self.config.options("Configuration")[2]
        self.threads = self.config.options("Configuration")[3]