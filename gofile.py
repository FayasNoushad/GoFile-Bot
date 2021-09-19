import requests

def uploadFile(
    file: str,
    token: str = None,
    folderId: str = None,
    description: str = None,
    password: str = None,
    tags: str = None,
    expire: int = None,
    server: str = getServer()["server"]
):
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
