import tkinter as tk
from tkinter import messagebox
import random

# Define diverse quiz questions by category
quiz_data = {
    "Nature": [
        {"question": "Which gas do plants absorb?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"], "answer": "Carbon Dioxide"},
        {"question": "What part of the plant conducts photosynthesis?", "options": ["Root", "Stem", "Leaf", "Flower"], "answer": "Leaf"},
    ],
    "Space": [
        {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": "Mars"},
        {"question": "What is the center of our solar system?", "options": ["Earth", "Sun", "Moon", "Milky Way"], "answer": "Sun"},
    ],
    "Music": [
        {"question": "Which note comes after G in the musical scale?", "options": ["A", "B", "C", "F"], "answer": "A"},
        {"question": "Who is known as the King of Pop?", "options": ["Elvis Presley", "Justin Bieber", "Michael Jackson", "Prince"], "answer": "Michael Jackson"},
    ],
    "Love": [
        {"question": "Valentine's Day is celebrated in which month?", "options": ["January", "February", "March", "April"], "answer": "February"},
        {"question": "Which organ is most associated with love?", "options": ["Liver", "Heart", "Brain", "Lungs"], "answer": "Heart"},
    ],
    "Religion": [
        {"question": "Which book is sacred to Christians?", "options": ["Quran", "Torah", "Vedas", "Bible"], "answer": "Bible"},
        {"question": "What day is the Sabbath in Judaism?", "options": ["Friday", "Saturday", "Sunday", "Monday"], "answer": "Saturday"},
    ],
    "Python": [
        {"question": "Which keyword defines a function in Python?", "options": ["func", "def", "define", "lambda"], "answer": "def"},
        {"question": "What data type is this: 'True'?", "options": ["String", "Boolean", "Integer", "Float"], "answer": "Boolean"},
    ]
}

# Global game state
questions = []
score = 0
current_question_index = 0
selected_category = None
timer_seconds = 15
timer_id = None

# --- GUI ---
root = tk.Tk()
root.title("🧠 Diverse Quiz App")
root.geometry("600x400")
root.config(bg="#1e1e1e")

question_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="#00ffff", wraplength=500)
question_label.pack(pady=20)

option_buttons = []
for i in range(4):
    btn = tk.Button(root, text="", font=("Arial", 12), width=40, bg="#444", fg="white", command=lambda i=i: check_answer(i))
    btn.pack(pady=5)
    option_buttons.append(btn)

timer_label = tk.Label(root, text="", font=("Arial", 12), bg="#1e1e1e", fg="yellow")
timer_label.pack(pady=10)

# --- Functions ---
def select_category_screen():
    global selected_category
    clear_screen()

    cat_frame = tk.Frame(root, bg="#1e1e1e")
    cat_frame.pack(pady=30)

    tk.Label(root, text="Select a Quiz Category", font=("Arial", 16, "bold"), fg="white", bg="#1e1e1e").pack(pady=10)

    for category in quiz_data.keys():
        btn = tk.Button(cat_frame, text=category, font=("Arial", 12), width=20,
                        command=lambda c=category: start_quiz(c), bg="#009688", fg="white")
        btn.pack(pady=5)

def start_quiz(category):
    global selected_category, questions, score, current_question_index
    selected_category = category
    score = 0
    current_question_index = 0
    questions = quiz_data[category][:]
    random.shuffle(questions)
    show_question()

def show_question():
    global current_question_index, timer_seconds, timer_id

    if current_question_index >= len(questions):
        return show_score()

    question = questions[current_question_index]
    question_label.config(text=f"Q{current_question_index + 1}: {question['question']}")
    options = question["options"]
    random.shuffle(options)

    for i in range(4):
        option_buttons[i].config(text=options[i], state=tk.NORMAL)

    timer_seconds = 15
    update_timer()

def update_timer():
    global timer_seconds, timer_id

    timer_label.config(text=f"⏰ Time left: {timer_seconds}s")
    if timer_seconds > 0:
        timer_seconds -= 1
        timer_id = root.after(1000, update_timer)
    else:
        disable_buttons()
        show_timeout()

def check_answer(selected_index):
    global score, current_question_index

    root.after_cancel(timer_id)
    question = questions[current_question_index]
    selected_option = option_buttons[selected_index]["text"]

    if selected_option == question["answer"]:
        score += 1
        question_label.config(text="✅ Correct!")
    else:
        question_label.config(text=f"❌ Wrong! Answer: {question['answer']}")

    disable_buttons()
    root.after(2000, next_question)

def show_timeout():
    global current_question_index
    question = questions[current_question_index]
    question_label.config(text=f"⏱️ Time's up! Correct answer: {question['answer']}")
    root.after(2000, next_question)

def disable_buttons():
    for btn in option_buttons:
        btn.config(state=tk.DISABLED)

def next_question():
    global current_question_index
    current_question_index += 1
    show_question()

def show_score():
    clear_screen()
    tk.Label(root, text=f"🎯 Final Score: {score} / {len(questions)}", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="cyan").pack(pady=30)

    tk.Button(root, text="🔁 Play Again", font=("Arial", 12), bg="#00a86b", fg="white",
              command=select_category_screen).pack(pady=10)
    tk.Button(root, text="❌ Exit", font=("Arial", 12), bg="crimson", fg="white",
              command=root.destroy).pack(pady=10)

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# Start with category selection
select_category_screen()
root.mainloop()
