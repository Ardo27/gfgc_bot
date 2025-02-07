from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

# ✅ Replace with your bot token
TOKEN = "8065888962:AAFMgJZM4UGT2ukGOkG6UWmkkMSascxVpnc"

# ✅ College Information Database
COLLEGE_DATA = {
    "name": "Government First Grade College, Mangalore",
    "established": "2007",
    "location": "CarStreet, Mangalore, Karnataka",
    "principal": "Dr. Jayakara Bhandary",
    "history": "The college was established in 2007. Initially based at Balmatta, it moved to CarStreet in 2008.",
    "students_2024": "1,200 students",
    "courses": [
        "B.A (Bachelor of Arts)",
        "B.Sc (Bachelor of Science)",
        "B.Com (Bachelor of Commerce)",
        "B.C.A (Bachelor of Computer Applications)",
        "B.B.A (Bachelor of Business Administration)",
        "B.S.W (Bachelor of Social Work)",
        "M.Com (Master of Commerce)",
        "M.A in Politics (Master of Arts in Politics)",
        "M.S.W (Master of Social Work)"
    ],
    "contact": "+91-9876543210",
    "website": "https://gfgc.edu.in/",
    "facilities": "Library, Sports Complex, Computer Lab, Hostel, Auditorium",
    "admission": "Admissions open in June. Apply online via the website."
}


# ✅ Start Command
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📖 History", callback_data="history"),
         InlineKeyboardButton("📍 Location", callback_data="location")],
        [InlineKeyboardButton("🎓 Courses", callback_data="courses"),
         InlineKeyboardButton("☎ Contact", callback_data="contact")],
        [InlineKeyboardButton("🏫 Facilities", callback_data="facilities"),
         InlineKeyboardButton("📝 Admission", callback_data="admission")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to GFGC College Bot!\nTap a button below to get information:",
        reply_markup=reply_markup
    )


# ✅ Callback Handler for Buttons
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    response = COLLEGE_DATA.get(query.data, "❌ Information not found.")
    if isinstance(response, list):
        response = "\n".join(f"• {item}" for item in response)

    await query.message.reply_text(response)


# ✅ Handle Text Messages
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    response = None

    if "establish" in text or "founded" in text:
        response = f"🏛 The college was established in {COLLEGE_DATA['established']}."
    elif "location" in text:
        response = f"📍 {COLLEGE_DATA['location']}"
    elif "principal" in text:
        response = f"🎓 Principal: {COLLEGE_DATA['principal']}"
    elif "students" in text:
        response = f"👨‍🎓 {COLLEGE_DATA['students_2024']} enrolled."
    elif "course" in text:
        response = "🎓 Courses Offered:\n" + "\n".join(f"• {course}" for course in COLLEGE_DATA["courses"])
    elif "contact" in text:
        response = f"📞 Contact: {COLLEGE_DATA['contact']}\n🌐 Website: {COLLEGE_DATA['website']}"
    elif "facilities" in text:
        response = f"🏫 Facilities Available: {COLLEGE_DATA['facilities']}"
    elif "admission" in text:
        response = f"📅 {COLLEGE_DATA['admission']}"
    else:
        response = "❌ Sorry, I couldn't find that information. Try using a button."

    await update.message.reply_text(response)


# ✅ Main Function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))  # ✅ FIXED: Handling button clicks

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
