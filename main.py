import os
import requests
from dotenv import load_dotenv
from gofile import uploadFile
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv()

Bot = Client(
    "GoFile-Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

INSTRUCTIONS = """
I am a gofile uploader telegram bot. \
You can upload files to gofile.io with command.

With media:
    Normal:
        `/upload`
    With token:
        `/upload token`
    With folder id:
        `/upload token folderid`

Using Link:
    Normal:
        `/upload url`
    With token:
        `/upload url token`
    With folder id:
        `/upload url token folderid`
"""


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text=f"Hello {update.from_user.mention}," + INSTRUCTIONS,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.command("upload"))
async def filter(bot, update):

    message = await update.reply_text(
        text="`Processing...`",
        quote=True,
        disable_web_page_preview=True
    )

    text = update.text.replace("\n", " ")
    url = None
    token = None
    folderId = None

    if " " in text:
        text = text.split(" ", 1)[1]
        if update.reply_to_message:
            if " " in text:
                token, folderId = text.split(" ", 1)
            else:
                token = text
        else:
            if " " in text:
                if len(text.split()) > 2:
                    url, token, folderId = text.split(" ", 2)
                else:
                    url, token = text.split()
            else:
                url = text
            if not (url.startswith("http://") or url.startswith("https://")):
                await message.edit_text("Error :- `url is wrong`")
                return
    elif not update.reply_to_message:
        await message.edit_text("Error :- `downloadable media or url not found`")
        return

    try:

        await message.edit_text("`Downloading...`")
        if url:
            response = requests.get(url)
            media = response.url.split("/", -1)[-1]
            with open(media, "wb") as file:
                file.write(response.content)
        else:
            media = await update.reply_to_message.download()
        await message.edit_text("`Downloaded Successfully`")

        await message.edit_text("`Uploading...`")
        response = uploadFile(file=media, token=token, folderId=folderId)
        await message.edit_text("`Uploading Successfully`")

        try:
            os.remove(media)
        except Exception as error:
            print(error)

    except Exception as error:
        await message.edit_text(f"Error :- `{error}`")
        return

    text = f"**File Name:** `{response['fileName']}`" + "\n"
    text += f"**Download Page:** `{response['downloadPage']}`" + "\n"
    text += f"**Direct Download Link:** `{response['directLink']}`" + "\n"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Open Link", url=response['directLink']),
                InlineKeyboardButton(
                    text="Share Link", url=f"https://telegram.me/share/url?url={response['directLink']}")
            ],
            [
                InlineKeyboardButton(
                    text="Feedback", url="https://telegram.me/FayasNoushad")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Bot.run()
