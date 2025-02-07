import difflib
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your Telegram bot token
TOKEN = "8065888962:AAFMgJZM4UGT2ukGOkG6UWmkkMSascxVpnc"

# ✅ College Information Database
COLLEGE_DATA = {
    "name": "Government First Grade College, Mangalore",
    "established": "2007",
    "location": "CarStreet, Mangalore, Karnataka",
    "principal": "Dr. Jayakara Bhandary",
    "history/about college":"The college is located in Mangalore, Karnataka, India. It was established in 2007 and was initially based at the Government PU College building in Balmatta but relocated to the Government Primary School building in Carstreet in 2008. The college was renamed to the Dr. P. Dayananda Pai- P. Sathisha Pai Government First Grade College in October 2017 and was reopened by Basavaraj Rayareddy, Minister for Higher Education of the State of Karnataka.[2] The inauguration ceremony was attended by patrons Dayananda Pai and Sathisha Pai.",
    "students_enrolled_2024": "1,200 students",
    "courses_offered": [
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
    "admission_process": "Admissions open in June. Apply online via the college website."
}

# ✅ Function to search for answers in predefined data
def get_best_answer(user_query):
    query_lower = user_query.lower()

    # 🔍 Direct keyword-based search
    if "establish" in query_lower or "founded" in query_lower:
        return f"🏛 The college was established in {COLLEGE_DATA['established']}."
    elif "location" in query_lower or "where" in query_lower:
        return f"📍 Location: {COLLEGE_DATA['location']}"
    elif "principal" in query_lower:
        return f"🎓 The principal of the college is {COLLEGE_DATA['principal']}."
    elif "students" in query_lower or "enrolled" in query_lower:
        return f"👨‍🎓 In 2024, {COLLEGE_DATA['students_enrolled_2024']} enrolled."
    elif "course" in query_lower or "program" in query_lower:
        return "🎓 Courses Offered:\n" + "\n".join(f"• {course}" for course in COLLEGE_DATA["courses_offered"])
    elif "contact" in query_lower or "phone" in query_lower:
        return f"📞 Contact: {COLLEGE_DATA['contact']}\n🌐 Website: {COLLEGE_DATA['website']}"
    elif "facilities" in query_lower or "infrastructure" in query_lower:
        return f"🏫 Facilities Available: {COLLEGE_DATA['facilities']}"
    elif "admission" in query_lower:
        return f"📅 {COLLEGE_DATA['admission_process']}"

    # 🔍 Fuzzy matching for unknown questions
    best_match = difflib.get_close_matches(query_lower, COLLEGE_DATA.keys(), n=1, cutoff=0.5)
    if best_match:
        key = best_match[0]
        return f"🔍 Here's what I found: {COLLEGE_DATA[key]}"

    return "❌ Sorry, I couldn't find that information. Try asking something else."

# ✅ Handle /start Command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "👋 Welcome to GFGC College Bot!\n"
        "You can ask about:\n"
        "1️⃣ About College / History\n"
        "2️⃣ Courses Offered\n"
        "3️⃣ Contact Details\n"
        "4️⃣ Location\n"
        "5️⃣ Admissions & Fees\n"
        "6️⃣ Principal & Staff\n"
        "7️⃣ Student Enrollment\n"
        "Type your question!"
    )

# ✅ Handle User Messages
async def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text.lower()
    response = get_best_answer(user_text)
    await update.message.reply_text(response)

# ✅ Main Function to Start Bot
def main():
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
