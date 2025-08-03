import os.path
import customtkinter as ctk
from datetime import date , timedelta
import json
last_check_date = None
habit = ""
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('C:/Users/ASUS/PyCharmMiscProject/breeze.json')
#main window
app = ctk.CTk()
app.title("Habitify🎀")
app.geometry("300x500")
label = ctk.CTkLabel(app,text = "Please enter the goal:\n",font=("Impact", 20))
label.pack(pady = 20)
habit_entry = ctk.CTkEntry(app,width = 250, placeholder_text='sth like coding-language learning...',font=("Courier New", 12))
habit_entry.pack(pady=20)
motivation_label = ctk.CTkLabel(app,text ="")
motivation_label.pack(pady=20)
status_label = ctk.CTkLabel(app,text ="",text_color="red",font=("Courier New", 12))
status_label.pack(pady=30)
data = {}
selected_habit = ""
#all functions:
def load_data():
    global habit,current_streak,last_check_date , data
    if os.path.exists("habit_date.json"):
        with open("habit_date.json","r") as file:
            try:
                data = json.load(file)
                habit = data.get("habit","")
                current_streak = data.get("current_streak",0)
                last_check_str = data.get("last_check_date",None)
                if last_check_str:
                    last_check_date = date.fromisoformat(last_check_str)
                else:
                     last_check_date = 0
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
def save_time():
    with open ("habit_date.json", "w") as file:
        json.dump(data,file,indent=4)
def add_new_habit():
    global selected_habit
    #remider : .get() to get the input from user//// .strip() for removing unwanted space from first and last of the str
    new_habit = habit_entry.get().strip()
    if new_habit and new_habit not in data:
        #for making sure the input is not empty and not duplicate
        data[new_habit] = {
            #this is making a new 'key' in dic
            "current_streak": 0,
            "last_check_date": None
        }
        save_time()
        update_dropdown_menu()
        selected_habit = new_habit
    selected_habit = new_habit
    habit_menu.set(new_habit)
    update_streak_label()

habit_menu = ctk.CTkOptionMenu(app,values=[],command=lambda h: set_selected_habit(h) )
habit_menu.pack(pady = 10)
def update_dropdown_menu():
    #for updating menu options
    #data keys are habits in the list in json file
    habit_menu.configure(values=list(data.keys()))
def select_habit(habit_name):
    #choosing the habit
    global selected_habit
    selected_habit = habit_name
    update_streak_label()
def update_streak_label():
    if selected_habit in data:
        streak = data[selected_habit]["current_streak"]
        streak_label.configure(text=f"Days done for {selected_habit}: {streak}")
def update_motivation_label():
    if selected_habit in data:
        streak = data[selected_habit]["current_streak"]
        message = motivational_message(streak)
        motivation_label.configure(text = message)
def submit_habit():
    global habit,selected_habit
    habit = habit_entry.get().strip()
    #check if habit is empty or not
    if habit:
        if habit not in data:#check if habit is not deplicate
            data[habit]={
                "current_streak":0,
                "last_check_date":None
            }
            save_time()
            update_dropdown_menu()
        selected_habit = habit
        habit_menu.set(habit) #show habit in the menu
        update_streak_label()
        print("the goal : ",habit)
        label.configure(text =f'this aim :{habit}')
    else:
        status_label.configure(text="Enter a habit!")

submit_button = ctk.CTkButton(app,text = "submit" , command = submit_habit)
submit_button.pack(pady = 10)
#first value of days
current_streak = 0
load_data()
streak_label = ctk.CTkLabel(app,text = f"Days done : {current_streak}")
streak_label.pack(pady=10)
def motivational_message(current_streak):
    if current_streak == 1:
        return "level 1 \t YOU DID START, don't give up💪🏻"
    elif current_streak < 15:
        return "just keep going"
    elif current_streak == 15:
        return "UPGRADED TO LEVEL 2 🥇"
    elif current_streak < 45:
        return "level 2 \t Doing amazing.Come back tomorrow 🎀"
    elif current_streak == 45:
        return "UPGRADED TO LEVEL 3 🥈 "
    elif current_streak < 90:
        return "level 3 \t You are a legend now.🏆"
    elif current_streak == 90:
        return "UPGRADED TO LEVEL 4 🥉 "
    else:
        return "you are amazing dude never stop!🎖"
def mark_done_today ():
    global data
    today = date.today()
    if not selected_habit:
        return
    if selected_habit not in data: #if no habit is chosen
        status_label.configure(text="No habit selected!")
        return
    habit_info = data[selected_habit]
    last_date_str = habit_info.get("last_check_date")
    last_date = date.fromisoformat(last_date_str) if last_date_str else None
    if last_date ==today:
        status_label.configure(text="You have already checked today!🙄")
        return
    if last_date is not None and (last_date + timedelta(days=1)) < today:
        habit_info["current_streak"]=0
    habit_info["current_streak"] += 1
    habit_info["last_check_date"] = today.isoformat()
    save_time()
    update_streak_label()
    print(update_motivation_label())

done_button = ctk.CTkButton(app,text = "DONE✔️" , command = mark_done_today,font=("Courier New", 12))
done_button.pack(pady = 10)
app.mainloop()