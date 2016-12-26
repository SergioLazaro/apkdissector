__author__ = 'sergio'

from androguard.core.analysis import analysis
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm

class AndroApp:
	def __init__(self, apkpath):
		self.a = apk.APK(apkpath)
		self.d = dvm.DalvikVMFormat(self.a.get_dex())
		self.vmx = analysis.newVMAnalysis(self.d)

class AndroClass:
	def __init__(self,classname, methods):
		self.classname = classname
		self.methods = methods

	def print_info(self):
		print "CLASSNAME = " + self.classname
		print "METHODS"
		for method in self.methods:
			print method.toString()


class AndroMethod:

	def __init__(self,classname,methodname,signature):
		self.classname = classname
		self.methodname = methodname
		self.signature = signature

	def toString(self):
		return self.classname + " - " + self.methodname + " - " + self.signature
