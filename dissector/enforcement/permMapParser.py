__author__ = 'sergio'

import json

from permissionStack import StackElement, PermissionStack

class AndroidJsonParser:

    def __init__(self,jsonpath):
        self.jsonpath = jsonpath
        self.permissionStackElementList = list()
        self.getPermissionStackArray()

    '''
        This method read the JSON file inserted as a parameter in the main.
        It iterates over the JSON array to create objects that are appended
        in [permissionStackElementList] list of the current AndroidJsonParser
        object.
    '''
    def getPermissionStackArray(self):

        with open(self.jsonpath) as file:
            data = json.load(file)

            data = data['mapping']      #Getting the interesting information from the JSON file
            i = 0
            while i < len(data):

                permission = data[i]['permission']
                methodName = data[i]['methodName']
                uid = data[i]['uid']
                pid = data[i]['pid']
                stack = self.getStackElementsArray(data[i]['stack'])
                #Creating stackElement object array
                permissionStackElement = PermissionStack(permission,uid,pid,methodName,stack)
                self.appendNewPermissionStack(permissionStackElement)   #Append this object into the list
                i += 1

    '''
        Method that appends a new permissionStackElement in the
        list created by the constructor (self.permissionStackElementList)
    '''
    def appendNewPermissionStack(self,permissionStackElement):
        print "[*] New element appended. Permission: " + permissionStackElement.permission
        self.permissionStackElementList.append(permissionStackElement)

    '''
        Method that parse the json_stack element and return a list of
        StackElement (permissionStack.py object)
    '''
    def getStackElementsArray(self,json_stack):
        stack = list()
        for elem in json_stack:
            className = elem['className']
            fileName = elem['fileName']
            methodName = elem['methodName']
            #Creating new StackElement object
            stackElement = StackElement(fileName,className,methodName)
            #Appending new StackElement object to the stack list
            stack.append(stackElement)

        return stack