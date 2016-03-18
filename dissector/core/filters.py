__author__ = 'vaioco'

from json import JSONEncoder

class TargetVirtualMethod(JSONEncoder):
    def __init__(self, m, p, ret):
        self.name = m.get_name()
        self.method = m
        self.proto = p
        self.ret = ret



class VirtualMethodsFilter:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        ## dict of TargetClass object
        self.classes = {}

    def filtering(self):
        vmethods_list = []
        classes_list = self.analyzer.get_cls_list()
        for c in classes_list:
            for m in c.get_methods():
                if m.get_access_flags_string() == "public":
                    print "Target: " + m.get_class_name() +  m.get_name() + '->' + m.get_descriptor()
                    (proto, return_type)  = self._parseProto(m.proto)
                    virtual_method = TargetVirtualMethod(m, proto, return_type)
                    #print m.proto, m.return_type
                    #self.methods.append(m)
                    real_name = c.get_name().replace('/','.').replace(';','')
                    real_name = real_name[1:]
                    #target_class = TargetClass(real_name)
                    #target_class.virtual_methods.append(virtual_method)
                    vmethods_list.append(virtual_method)
            self.classes[real_name] = vmethods_list
            vmethods_list = []

        for k,v in self.classes.iteritems():
            print k,v

    def get_data(self):
        return  (self.classes)

    def _parseProto(self, proto):
        args = ""
        ret_type = ""
        ## trasformo da formato dalvik a formato Java e tolgo gli spazi
        ret = proto.replace('/', '.').replace(" ","")
        ## splitto la stringa in due: argomenti e valore di ritorno
        l = ret.split(')')
        ## elimino il carattere di parentesi chiusa
        l = [tmp.replace('(','') for tmp in l]
        ## rimuovo eventuali elementi nulli rimanenti
        l = filter(None,l)
        counter = 0
        for item in l[:1]:
            args_list = item.split(';')
            args_list = filter(None, args_list)
            if len(args_list) == 0:
                continue
            print 'args list: ' + str(args_list)
            nargs = 0
            for arg in args_list:
                if arg[:1] == 'L':
                    nargs += 1
                    args += ", " + arg[1:] + " arg%d " % (nargs)
                else:
                    arg = arg.replace(" ","")
                    for c in arg:
                        if c == 'I':
                            nargs += 1
                            args += ",int arg%d " % (nargs)
        ## item is the return type
        if l[-1] is not None:
            item = l[-1]
            item = item.replace(";",'')
            #print 'return type founded!' + str(l[-1])
            if item[:1] == 'L':
                ret_type = item[1:]
            else:
                if item[:1] == 'V':
                    ret_type = 'void'
                if item[:1] == 'I':
                    ret_type = 'int'
                #TODO: continuare gli if
        return (args, ret_type)