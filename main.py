import os
import urldl
from gofile import uploadFile
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 


Bot = Client(
    "GoFile-Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    
    await update.reply_text(
        text=f"""Hello {update.from_user.mention},
        Please send a media and reply `/upload` for gofile.io stream url.
        You can also send with token and folder id\n
        Normal:-
          `/upload`
        With token:-
          `/upload token`
        With folder id:-
          `/upload token folderid`
        \n
        You can also send as media download url with token and folder id\n
        Normal:-
          `/upload url`
        With token:-
          `/upload url token`
        With folder id:-
          `/upload url token folderid`\n
        Made by @FayasNoushad""",
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.command("upload"))
async def filter(bot, update):
    
    text = update.text.replace("\n", " ")
    url = None
    token = None
    folderId = None
    
    if " " in text:
        text = text.split(" ", 1)[1]
        if not update.reply_to_message.media:
            if text.startswith("http://") or text.startswith("https://"):
                if " " in text:
                    if len(text.split()) > 2:
                        url, token, folderId = text.split(" ", 2)
                    else:
                        url, token = text.split()
                else:
                    url = text
    elif not update.reply_to_message:
        return
    
    message = await update.reply_text(
        text="`Processing...`",
        quote=True,
        disable_web_page_preview=True
    )
    
    try:
        
        try:
            await message.edit_text("`Downloading...`")
        except:
            pass
        if url:
            media = urldl.download(url)
        else:
            media = await update.reply_to_message.download()
        
        try:
            await message.edit_text("`Uploading...`")
        except:
            pass
        response = uploadFile(file=media, token=token, folderId=folderId)
        
        try:
            os.remove(media)
        except:
            pass
    
    except Exception as error:
        await message.edit_text(
            text=f"Error :- `{error}`",
            quote=True,
            disable_web_page_preview=True
        )
        return
    
    text = f"**File Name:** `{response['fileName']}`" + "\n"
    text += f"**Download Page:** `{response['downloadPage']}`" + "\n"
    text += f"**Direct Download Link:** `{response['directLink']}`" + "\n"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Open Link", url=response['directLink']),
                InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={response['directLink']}")
            ],
            [
                InlineKeyboardButton(text="Join Updates Channel", url="https://telegram.me/FayasNoushad")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Bot.run()
