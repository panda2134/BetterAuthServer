import cPickle as pickle
import hashlib,os
from __builtin__ import file
class UserInfoStorage:
    __userInfo={} #key:email value:UserInfo
    __f=None
    def __init__(self):
        self.__f=open("UserInfo.bin",'w+b')
        if os.path.getsize("UserInfo.bin")>0:
            self.__userInfo=pickle.load(self.__f)
        #debug only
        u=UserInfo("example@example.com","test","test")
        self.addUser(u)
    
    def __del__(self):
        pickle.dump(self.__userInfo, self.__f, protocol=1)
    
    def addUser(self,u):
        self.__userInfo[u.email]=u
    
    def getUser(self,email):
        return self.__userInfo[email]
    
    def haveUser(self,email):
        return email in self.__userInfo.keys()
    
    def setUserName(self,email,name):
        self.__userInfo[email].setProfileName(name)
    
    
class UserInfo:
    clientToken=""
    accessToken=""
    email=""
    passwordHash=None
    availableProfiles=[{'id':0,'name':None}] #currently only one profile per account
    def checkToken(self,clientToken,accessToken):
        return clientToken == self.clientToken and accessToken == self.accessToken

    def setToken(self,clientToken,accessToken):
        self.clientToken=clientToken
        self.accessToken=accessToken
    
    def setEmail(self,email):
        self.email=email
    
    def setPassword(self,password):
        self.passwordHash=hashlib.sha512(password)
    
    def verifyPassword(self,password):
        return hashlib.sha512(password)==self.passwordHash
    
    def changePassword(self,passwordOld,passwordNew):
        if hashlib.sha512(passwordOld)==self.passwordHash:
            self.passwordHash=hashlib.sha512(passwordNew)
        else:
            raise ValueError('Password Incorrect')
    
    def setProfileName(self,name):
        if name!='' and name!=None:
            self.availableProfiles[0]['name']=name;
        else:
            raise ValueError('Name can\'t be null');
            
    def __init__(self,email,password,name):
        self.setEmail(email)
        self.setPassword(password)
        self.setProfileName(name)