import requests

def uploadFile(file: str):
    server = requests.get("https://api.gofile.io/getServer").json()["server"]
    uploadFile_response = requests.post(
        url=f"https://{server}.gofile.io/uploadFile",
        data={
            "token": None,
            "folderId": None,
            "description": None,
            "password": None,
            "tags": None,
            "expire": None
        },
        files={"upload_file": open(file, "rb")}
    ).json()
    return response_handler(uploadFile_response)
