
import os
import logging

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InputMediaPhoto,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN


# =========================
# CONFIGURATION
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PNG_DIR = os.path.join(BASE_DIR, "PNG")
VD_DIR = os.path.join(BASE_DIR, "Vd")
APK_DIR = os.path.join(BASE_DIR, "ml_v")

VIDEO_FILE = os.path.join(VD_DIR, "tutorial.mp4")
APK_FILE = os.path.join(APK_DIR, "mlbb.apk")

IMAGE_FILES = [
    os.path.join(PNG_DIR, "1.png"),
    os.path.join(PNG_DIR, "2.png"),
    os.path.join(PNG_DIR, "3.png"),
    os.path.join(PNG_DIR, "4.png"),
]

PROMO_CODE = "Promo - BellaCiao"

CAPTION = (
    "MLBB Promo - BellaCiao\n\n"
    "အကောင့်ဖွင့်နည်းကို အောက်ပါပုံများနှင့် "
    "Video Tutorial မှာ လေ့လာနိုင်ပါတယ်။\n\n"
    "အကောင့်ဖွင့်တိုင်း Bonus 100% အပြည့်ဝရမယ့်အပြင် "
    "အခြားသော Bonus များလည်း ရရှိနိုင်ပါတယ်။"
)

VIDEO_CAPTION = CAPTION


# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================
# KEYBOARD
# =========================

def main_keyboard():

    keyboard = [
        [
            KeyboardButton("MLBB Acc ဖွင့်နည်း"),
        ],
        [
            KeyboardButton("MLBB Apk Downရန်"),
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Welcome to MLBB Bot!\n\n"
        "အောက်ပါ Menu မှာ လိုအပ်တာကို ရွေးချယ်ပါ။",
        reply_markup=main_keyboard(),
    )


# =========================
# MLBB ACCOUNT TUTORIAL
# =========================

async def account_tutorial(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message

    # Check exactly 4 images
    if len(IMAGE_FILES) != 4:
        await message.reply_text(
            "Error: ပုံ ၄ ပုံတိတိ ထည့်ပေးပါ။"
        )
        return

    # Check image files
    missing_images = [
        path for path in IMAGE_FILES
        if not os.path.isfile(path)
    ]

    if missing_images:
        await message.reply_text(
            "PNG Folder ထဲမှာ ပုံဖိုင် မပြည့်စုံပါ။"
        )
        return

    # Send all four photos as ONE album
    try:

        media = []

        for index, image_path in enumerate(IMAGE_FILES):

            if index == 0:
                media.append(
                    InputMediaPhoto(
                        media=open(image_path, "rb"),
                        caption=CAPTION,
                    )
                )
            else:
                media.append(
                    InputMediaPhoto(
                        media=open(image_path, "rb"),
                    )
                )

        try:
            await message.reply_media_group(
                media=media
            )
        finally:
            for item in media:
                item.media.close()

    except Exception as error:

        logger.exception("Album sending failed")

        await message.reply_text(
            f"Album ပို့ရာတွင် Error ဖြစ်နေပါတယ်။"
        )
        return

    # Send video after album
    if not os.path.isfile(VIDEO_FILE):

        await message.reply_text(
            "Video ဖိုင်ကို Vd Folder ထဲမှာ မတွေ့ပါ။"
        )
        return

    try:

        with open(VIDEO_FILE, "rb") as video:

            await message.reply_video(
                video=video,
                caption=VIDEO_CAPTION,
                supports_streaming=True,
            )

        # Separate copyable promo code
        await message.reply_text(
            PROMO_CODE
        )

    except Exception:

        logger.exception("Video sending failed")

        await message.reply_text(
            "Video ပို့ရာတွင် Error ဖြစ်နေပါတယ်။"
        )


# =========================
# MLBB APK DOWNLOAD
# =========================

async def apk_download(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message

    if not os.path.isfile(APK_FILE):

        await message.reply_text(
            "APK ဖိုင်ကို ml_v Folder ထဲမှာ မတွေ့ပါ။"
        )
        return

    try:

        with open(APK_FILE, "rb") as apk:

            await message.reply_document(
                document=apk,
                filename="mlbb.apk",
                caption="MLBB APK Download",
            )

    except Exception:

        logger.exception("APK sending failed")

        await message.reply_text(
            "APK ပို့ရာတွင် Error ဖြစ်နေပါတယ်။"
        )


# =========================
# TEXT HANDLER
# =========================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    if text == "MLBB Acc ဖွင့်နည်း":

        await account_tutorial(update, context)

    elif text == "MLBB Apk Downရန်":

        await apk_download(update, context)

    else:

        await update.message.reply_text(
            "Menu မှာရှိတဲ့ Button ကို ရွေးချယ်ပါ။",
            reply_markup=main_keyboard(),
        )


# =========================
# ERROR HANDLER
# =========================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Update error: %s",
        context.error,
    )


# =========================
# MAIN
# =========================

def main():

    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN":
        raise ValueError("config.py ထဲမှာ BOT_TOKEN ထည့်ပါ။")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    app.add_error_handler(error_handler)

    print("MLBB BOT STARTED")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
