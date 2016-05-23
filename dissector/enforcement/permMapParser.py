__author__ = 'sergio'

import ijson
from permissionStack import StackElement, PermissionStack

class AndroidJsonParser:

    def __init__(self,jsonpath):
        self.jsonpath = jsonpath
        self.permissionStackElementList = list()
        print "[*] Getting elements from JSON file..."
        self.getPermissionStackArray()

    '''
        This method read the JSON file inserted as a parameter in the main.
        It iterates over the JSON array to create objects that are appended
        in [permissionStackElementList] list of the current AndroidJsonParser
        object.
    '''
    def getPermissionStackArray(self):
        fd = open(self.jsonpath,'rb')
        objects = ijson.items(fd,'mapping.item')
        for obj in objects:
            permission = obj['permission']
            methodName = obj['methodName']
            uid = obj['uid']
            pid = obj['pid']
            stack = self.getStackElementsArray(obj['stack'])
            #Creating stackElement object array
            permissionStackElement = PermissionStack(permission,uid,pid,methodName,stack)
            #print "[*] New element appended. Permission: " + permissionStackElement.permission
            self.appendNewPermissionStack(permissionStackElement)   #Append this object into the list

    '''
        Method that appends a new permissionStackElement in the
        list created by the constructor (self.permissionStackElementList)
    '''
    def appendNewPermissionStack(self,permissionStackElement):
        self.permissionStackElementList.append(permissionStackElement)

    '''
        Method that parse the json_stack element and return a list of
        StackElement (permissionStack.py object)
    '''
    def getStackElementsArray(self,json_stack):
        stack = list()
        for elem in json_stack:
            className = elem['className'].replace(".","/")
            fileName = elem['fileName']
            methodName = elem['methodName']
            #Creating new StackElement object
            stackElement = StackElement(fileName,className,methodName)
            #Appending new StackElement object to the stack list
            stack.append(stackElement)
        return stack