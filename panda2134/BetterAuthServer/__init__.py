from flask import Flask,request
import json,uuid,hashlib
from panda2134.BetterAuthServer.UserInfoStorage import UserInfoStorage

app=Flask(__name__)
storage=UserInfoStorage()

@app.route('/')
def rootPage():
    #TODO:finish this
    return "Hello World"

@app.route('/authenticate',methods=['POST'])
def auth():
    payload=request.get_json();
    resp={}
    if(payload['clientToken']==''):
        payload['clientToken']=str(uuid.uuid4())
    if storage.haveUser(payload['username']):
        u=storage.getUser(payload['username'])
    else:
        return ("Not Found",404)
    
    if not u.verifyPassword(payload['password']):
        return ("Forbidden",403)
    
    u.setToken(payload['clientToken'],str(uuid.uuid4()))
    resp['accessToken']=u.accessToken
    resp['clientToken']=u.clientToken
    if 'agent' in payload.keys():
        resp['availableProfiles']=u.availableProfiles
        resp['selectedProfile']=u.availableProfiles[0]
    return json.dumps(resp)

@app.route('/refresh',methods=['POST'])
def refresh():
    payload=request.get_json()
    if storage.haveUser(payload['username']):
        u=storage.getUser(payload['username'])
    else:
        return ("Not Found",404)
    #TODO:finish this
    
    
if __name__=='__main__':
    app.debug=True
    app.run()
