import os
import json
import shlex
import requests
import subprocess


def uploadFile(file_path: str, token=None, folderId=None) -> dict:
    response = requests.get("https://api.gofile.io/servers/").json()
    servers = response["data"]["servers"]
    server = servers[0]["name"]
    cmd = "curl "
    cmd += f'-F "file=@{file_path}" '
    if token:
        cmd += f'-F "token={token}" '
    if folderId:
        cmd += f'-F "folderId={folderId}" '
    cmd += f"'https://{server}.gofile.io/uploadFile'"
    upload_cmd = shlex.split(cmd)
    try:
        out = subprocess.check_output(upload_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise Exception(e)
    try:
        os.remove(file_path)
    except:
        pass
    out = out.decode("UTF-8").strip()
    # print(out)
    if out:
        out = out.split("\n")[-1]
        try:
            response = json.loads(out)
        except:
            raise Exception("API Error (Not Vaild JSON Data Received)")
        if not response:
            raise Exception("API Error (No JSON Data Received)")
    else:
        raise Exception("API Error (No Data Received)")

    if response["status"] == "ok":
        data = response["data"]
        # data["directLink"] = (
        #     f"https://{server}.gofile.io/download/{data['id']}/{data['name']}"
        # )
        return data
    elif "error-" in response["status"]:
        error = response["status"].split("-")[1]
        raise Exception(error)
