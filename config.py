from os import getenv
from dotenv import load_dotenv

admins = {}
load_dotenv()

# client vars
API_ID = int(getenv("API_ID", "26128734"))
API_HASH = getenv("API_HASH", "ff991e0856938ede932dc88fa2f15b61")
BOT_TOKEN = getenv("BOT_TOKEN", "5990830200:AAGlQbppgRb5J9xIh2MrKJOrGW7IP768yRs")
SESSION_NAME = getenv("SESSION_NAME", "Kyi - SESSION_SECRET")
SESSION_STRING = getenv("SESSION_STRING", "AgB86r0AbmBFb_yYuNajuG8X1_UDH0L5ckcuA7bImX1KMs-BMGYYBvHdLuUL4k9WTaPvXGmRBKzI2bs1P3Iwon457TY7QogcJRJEwVsXp3CaD8COHqYRjcDt840BkCdwlkVbsYoqlUIqz8EhE0pAmwiTQ4QjPm3ybJlTQttyNlgzToGNS0F0DpLQtS3RuxmgNim-2VvisxQ5VMyf-s0ug1xJ84FPE5qUYKo5mNRWa5O2VHLUmWvXfyF8alzYHWIdyseQblSZjkYC20KCZeUGOG2kMvcgf9fcSiWNpnnncFHSf3NUbizLiS5tjCNZLRoPAcoZWFHinO-4_1i6CJpwXNBkcrtoQwAAAAE-EYqSAA")

# mandatory vars
OWNER_USERNAME = getenv("OWNER_USERNAME", "rda")
ALIVE_NAME = getenv("ALIVE_NAME", "Music")
BOT_USERNAME = getenv("BOT_USERNAME", "MusicBot")
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/X02lx/")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "Hirosi_hr")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "Hirosi_hr")

# database, decorators, handlers mandatory vars
MONGODB_URL = getenv("MONGODB_URL", "mongodb+srv://veez:mega@cluster0.heqnd.mongodb.net/veez?retryWrites=true&w=majority")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "شغل تشغيل ش").split())
OWNER_ID = list(map(int, getenv("OWNER_ID", "6878196064").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6878196064").split()))

# image resources vars
IMG_1 = getenv("IMG_1", "https://te.legra.ph/file/2a726c634dbc3b9e8f451.png")
IMG_2 = getenv("IMG_2", "https://te.legra.ph/file/90e3b3aeb77e3e598d66d.png")
IMG_3 = getenv("IMG_3", "https://te.legra.ph/file/d70bb6fa92728763c671f.png")
IMG_4 = getenv("IMG_4", "https://te.legra.ph/file/430dcf25456f2bb38109f.png")
IMG_5 = getenv("IMG_5", "https://te.legra.ph/file/cd5c96a3c7e8ae1913ef3.png")
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/c83b000f004f01897fe18.png")
