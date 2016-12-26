__author__ = 'sergio'

class frida_writer:
    def __init__(self, filepath, classname):
        self.filepath = filepath
        self.classname = classname
        self.python_path = self.filepath + ".py"
        self.javascript_path = self.filepath + ".js"
        self.file = open(self.javascript_path,"a")

    def close_file(self):
        self.file.close()

    def write_frida_header(self):
        self.file.write("Java.perform(function() {\n")
        self.file.write("\t// Class to hook\n")
        self.file.write("\tvar ThisActivity = Java.use('" + self.classname + "');\n")

    def write_frida_hook(self,method):
        if method is not None:
            self.file.write("\tThisActivity." + method.methodname + ".implementation = function() {\n")
            self.file.write("\t\tsend('hook - " + method.methodname + "')\n")
            self.file.write("\t};\n")

    def write_frida_python(self,package_name):
        self.close_file()
        self.file = open(self.python_path,"w")
        #Write header
        self.file.write('import frida, sys\n')
        self.file.write('package_name = "' + package_name + '"\n')
        #Write function get_messages_from_js
        self.file.write('def get_messages_from_js(message, data):\n')
        self.file.write('\tprint(message)\n')
        self.file.write("\tprint(message['payload'])\n")
        #Write function instrument_load_url
        self.file.write("def instrument_load_url():\n")
        self.file.write("\twith open('" + self.classname + ".js', 'r') as myfile:\n")
        self.file.write("\t\thook_code = myfile.read()\n")
        self.file.write("\treturn hook_code\n")
        #Write bottom
        self.file.write("process = frida.get_usb_device().attach(package_name)\n")
        self.file.write("script = process.create_script(instrument_load_url())\n")
        self.file.write("script.on('message',get_messages_from_js)\n")
        self.file.write("script.load()\n")
        self.file.write("sys.stdin.read()\n")