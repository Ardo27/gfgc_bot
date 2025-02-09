import json
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8065888962:AAGDTZWsOkoRmbH44KAJ_1ragl5lP6rP5p8"

# ✅ Replace with your GitHub Web App URL
BOT_WEB_APP_URL = "https://ardo27.github.io/GFGC-web/"

# ✅ JSON File to Store User Data
USER_DATA_FILE = "users.json"

# ✅ Function to Load User Data from JSON
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# ✅ Function to Save User Data to JSON
def save_user_data(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

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

# ✅ Function to Save User Data
def save_user(user_id, name):
    users = load_user_data()
    if str(user_id) not in users:  # ✅ Prevent duplicates
        users[str(user_id)] = {"name": name}
        save_user_data(users)

# ✅ Start Command with Web App Button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name  # ✅ Get the user's first name
    save_user(user_id, first_name)  # ✅ Store user info in JSON file

    keyboard = [
        [InlineKeyboardButton("📖 History", callback_data="history"),
         InlineKeyboardButton("📍 Location", callback_data="location")],
        [InlineKeyboardButton("🎓 Courses", callback_data="courses"),
         InlineKeyboardButton("☎ Contact", callback_data="contact")],
        [InlineKeyboardButton("🏫 Facilities", callback_data="facilities"),
         InlineKeyboardButton("📝 Admission", callback_data="admission")],
        [InlineKeyboardButton("🌐 Open Web App", web_app=WebAppInfo(url=BOT_WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Hello {first_name}! Welcome to GFGC College Bot.\n"
        "Tap a button below to get information or open the web app:",
        reply_markup=reply_markup
    )

# ✅ Callback Handler for Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    response = COLLEGE_DATA.get(query.data, "❌ Information not found.")
    if isinstance(response, list):
        response = "\n".join(f"• {item}" for item in response)

    await query.message.reply_text(response)

# ✅ Handle Text Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    app.add_handler(CallbackQueryHandler(button_handler))  # ✅ Handles button clicks

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
