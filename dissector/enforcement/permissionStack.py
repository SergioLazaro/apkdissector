__author__ = 'sergio'

import hashlib

class StackElement:

    def __init__(self, filename, classname, methodname):
        self.filename = filename
        self.classname = classname
        self.methodname = methodname

    def toString(self):
        return self.filename + "," + self.classname + "," + self.methodname

class PermissionStack:

    def __init__(self, permission, uid, pid, methodname,stack):
        self.permission = permission
        self.uid = uid
        self.pid = pid
        self.methodname = methodname
        self.stack = stack
        self.hash = self.generateHash()

    '''
        This method generates the hash(sha1) of the string which contains
        the concatenation of [permission] and [stack-elements-string]
        The hash is returned.
    '''
    def generateHash(self):
        concatenation = self.permission + "," + str(self.stackToString())
        return hashlib.sha1(concatenation).hexdigest()

    '''
        Iterates over the stack elements list to concatenate all of them
        in a string. This method returns this string.
    '''
    def stackToString(self):
        string = ''
        for elem in self.stack:
            string += str(elem.toString()) + ','

        return string