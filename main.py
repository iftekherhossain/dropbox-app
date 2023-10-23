import requests
from fastapi import FastAPI, Form,File, UploadFile
import uvicorn
import json
app = FastAPI()

APP_KEY = ""
APP_SECRET = ""

@app.get("/get_auth_url")
async def get_auth_url():
    auth_uri = f"https://www.dropbox.com/oauth2/authorize?response_type=code&client_id={APP_KEY}"
    return f"Browse this url to authenticate: {auth_uri}"

@app.post("/authorize")
async def auth(code: str =Form(...)):
    token_url = "https://api.dropbox.com/oauth2/token"
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": APP_KEY,
        "client_secret": APP_SECRET,
    }

    response = requests.post(token_url, data=data)
    try:
        access_token = response.json()["access_token"]
        return {"Access Token" :access_token}
    except:
        return {"Error" :"Not a valid code"}
    
@app.post("/get_user_info")
async def get_user_info(access_tok: str=Form(...)):

    headers = {"Authorization": f"Bearer {access_tok}"}
    response = requests.post(f"https://api.dropboxapi.com/2/users/get_current_account", headers=headers)
    try:
        return response.json()
    except:
        return {"Error":"Beep"}

@app.post("/upload_file")
def upload_file(access_tok: str=Form(...), file: UploadFile = File(...)):
    
    headers = {"Authorization": f"Bearer {access_tok}", 
               "Content-Type": "application/octet-stream",
               "Dropbox-API-Arg": json.dumps({"path": "/uploaded/" + file.filename, "mode": "add"})}
    response = requests.post(
    f"https://content.dropboxapi.com/2/files/upload",
    headers=headers,
    data=file.file.read())
    
    try:
        return response.json()
    except:
        return {"Error":"Beep"}
    
@app.post("/file_info")
def file_info(access_tok: str=Form(...), file_path: str = Form(...)):
    url_info="https://api.dropboxapi.com/2/files/get_metadata"
    headers = {"Authorization": f"Bearer {access_tok}", 
               "Content-Type": "application/json",
               }
    data={
        "path": file_path,  
    }
    response = requests.post(url=url_info,headers=headers,json=data)
    try:
        return response.json()
    except Exception as e:
        print(e)
        return {"Error":"Beep"}

@app.post("/delete_file")
def delete_file(access_tok: str=Form(...), file_path: str = Form(...)):
    url_delete="https://api.dropboxapi.com/2/files/delete"
    headers = {"Authorization": f"Bearer {access_tok}", 
               "Content-Type": "application/json",
               }
    data={
        "path": file_path,   
    }
    response = requests.post(url=url_delete,headers=headers,json=data)
    try:
        return response.json()
    except:
        return {"Error":"Beep"}

if __name__ == '__main__':
    uvicorn.run(app, port=5000, host="127.0.0.5")