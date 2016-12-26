__author__ = 'sergio'
import optparse, re, os

from androguard_objects import AndroClass, AndroApp, AndroMethod
from frida_writer import frida_writer


class Frida:
	def __init__(self, apkpath):
		self.apkpath = apkpath
		self.start()

	def start(self):
		outputdir = "/tmp/hook_code/"

		createNewDir(outputdir)

		app = AndroApp(self.apkpath)
		package_name = app.a.get_package()
		# activities = app.a.get_activities()

		andro_classes = self.analyze_apk_classes(app, package_name)
		# andro_classes has AndroClasses info
		self.write_frida_hooks(andro_classes, outputdir, package_name)
		print "[*] Frida writer results in " + outputdir

	def analyze_apk_classes(self,app, package_name):
		andro_classes = list()
		for cl in app.d.get_classes():
			modified_class_name = convert_descriptor(cl.get_name())
			if package_name in modified_class_name and "R$" not in modified_class_name and \
							modified_class_name != package_name + ".BuildConfig" and \
							modified_class_name != package_name + ".R":

				andro_methods = list()
				for method in cl.get_methods():
					m = self.method_parser(str(method))
					if m is not None:
						andro_methods.append(m)
				andro_classes.append(AndroClass(modified_class_name, andro_methods))

		for an in andro_classes:
			an.print_info()
		return andro_classes

	def method_parser(self,method):
		class_name = convert_descriptor(re.search("(.*);->", method).group(1))
		method_tmp = re.search("<(.*)>", method)
		andro_method = None
		if method_tmp is None:
			method_name = re.search(";->(.*)\(", method).group(1)
			signature = re.search(method_name + "(.*) \[", method).group(1)
			andro_method = AndroMethod(class_name,method_name,signature)
			#print andro_method.toString()

		return andro_method

	def write_frida_hooks(self, andro_classes, outputdir, package_name):
		createNewDir(outputdir + package_name) #Create directory for this apk

		for cl in andro_classes:
			filepath = outputdir + package_name + "/" + cl.classname
			fw = frida_writer(filepath, cl.classname)
			fw.write_frida_header()
			for method in cl.methods:
				fw.write_frida_hook(method)

			fw.file.write("});")	#Close file structure
			fw.write_frida_python(package_name)


def createNewDir(dirpath):
	if not os.path.exists(dirpath):
		print "[*] Creating new directory in %s ..." % (dirpath)
		os.makedirs(dirpath)

def convert_descriptor(name):
	name = name[1:]
	return name.replace("/",".").replace(";","")