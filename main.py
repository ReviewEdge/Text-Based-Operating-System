# -*- coding: utf-8 -*-
import time
import requests
import datetime
import smtplib
import imapclient
import imaplib
imaplib._MAXLINE = 10000000
import pprint
import pyzmail




# Declares globals
global logged_in
logged_in = False
global has_email
has_email = False

# creates date and time variables
now = datetime.datetime.now()

date_and_time_data = now.strftime("%b %d, %Y %I:%M %p")
date_data = now.strftime("%b %d, %Y")
time_data = now.strftime("%I:%M %p")
# for email
email_search_date = now.strftime("%Y/%m/%d")



def new_file():
    new_file_name = input("Enter a name for your file:\n") + ".txt"
    file_1 = open(new_file_name, "w")
    new_file_text = input("Enter text for your new file. Press ENTER when you are finnished:\n") + "\n\n"
    file_1.write(new_file_text)
    file_1.close()
    print("File created. Closing file creator...\n")
    time.sleep(1)


def open_file_func():
    file_name_op = input("Enter the name of the file you would like to access (without .txt):\n") + ".txt"
    try:
        open_file = open(file_name_op, "r+")
    except IOError:
        print("\nFile not found.\n")
        time.sleep(.8)
        open_file_func()
    else:
        #open_file.read()
        print("\n\n" + open_file.read() + "\n\n")
        ans = input("Would you like to edit this file? (Y/n)\n").lower()
        if ans == "y":
            print("Enter text to add to the file.\nPress ENTER when you are finnished:\n")
            text_to_add = input() + "\n\n"
            open_file.write(text_to_add)
        print("Closing editor...\n")
        open_file.close()
        time.sleep(1)


# runs the files app
def files():
    x = "on"
    while x != "off":
        print("\tFILES\n")
        print("\t\t'create' 'open' 'off'")
        x = input()
        if x == "create":
            new_file()
        if x == "open":
            open_file_func()


def weather():
    city_id = "5122534"
    url = "http://api.openweathermap.org/data/2.5/weather?id=" + city_id + "&units=imperial&APPID=c3e072c5029f60ac53dac3d1c7d9b06f"
    json_data = requests.get(url).json()

    temp_val = str(json_data["main"]["temp"])

    description = str(json_data["weather"][0]["description"])
    description = description.capitalize()

    format_add = description + "\n" + "Temperature: " + temp_val + " " + "°F"
    # prints what is being returned
    #print("Current weather in Jamesown, NY: \n\n" + format_add)
    return "Current weather in Jamesown, NY: \n" + format_add


def save_email_know(email_ad,password):
    # ADD ABILITY TO CHECK IF NUMBER HAS BEEN USED
    account_num = input("Enter a user number for your account:")
    new_file_name = "email_account_" + account_num + ".txt"
    file_1 = open(new_file_name, "w")
    new_file_text = "A" + email_ad + "P" + password
    file_1.write(new_file_text)
    file_1.close()
    print("Your email account information has been saved as account #" + account_num + "\n\n")
    time.sleep(2)


def send_email():
    if logged_in and has_email:
        email = global_email_address
        password = global_email_password

    if logged_in and (has_email == False):
        print("\nYou have not saved an email to your account.  You can do this in the 'account' app.\n")
        time.sleep(1)

    if has_email == False:
        email = input("Enter your email adress: ")
        password = input("Enter password: ")
        #save_it = input("\nWould you like to save your information? (Y/n):\n").lower()
        #if save_it == "y":
        #    save_email_know(email,password)

    # starts connection
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()

    '''
    saved = input("Do you have a saved account (Y/n)?\n").lower()
    if saved == "y":
        account_num = input("Enter you account #:\n")
        open_file = open("email_account_" + account_num + ".txt", "r+")
        info = open_file.read()
        pas_idx = info.index("P")

        email = info[1:pas_idx]
        password = info[pas_idx+1:]
    '''


    time.sleep(.4)
    print("\nSending email as " + email + "\n")
    time.sleep(1)

    # creates variables
    sendaddress = input("Enter the recipient's email address:\n")
    subject = input("Enter the email's subject:\n")
    message = input("Enter the email's message:\n")
    full_message = "Subject: " + subject + " " + " \n" + message
    # sends email
    smtpObj.login(email, password)
    smtpObj.sendmail(email, sendaddress, full_message)
    # quits connection
    smtpObj.quit()
    print("\nEmail sent.\n")
    time.sleep(1.5)


#add ability to search for emails -google search?
#ability to show only beginning of email then ask to see more

def read_email():
    global has_email

    print(has_email) #delete

    if logged_in and has_email:
        email = global_email_address
        password = global_email_password


    if logged_in and (has_email == False):
        print("\nYou have not saved an email to your account.  You can do this in the 'account' app.\n")
        time.sleep(1)

    if has_email == False:
        email = input("Enter your email address: ")
        password = input("Enter password: ")
        #save_it = input("\nWould you like to save your information? (Y/n):\n").lower()
        #if save_it == "y":
        #    save_email_know(email, password)


    '''
    saved = input("Do you have a saved account (Y/n)?\n").lower()
    if saved == "y":
        account_num = input("Enter you account #:\n")
        open_file = open("email_account_" + account_num + ".txt", "r+")
        info = open_file.read()
        pas_idx = info.index("P")

        email = info[1:pas_idx]
        password = info[pas_idx + 1:]
    '''

    print("\nViewing email as " + email + "\n")
    imapObj = imapclient.IMAPClient("imap.gmail.com", ssl=True)
    imapObj.login(email, password)
    imapObj.select_folder("INBOX", readonly=True)
    #print(email_search_date)
    #choses search terms:
    UIDs = imapObj.gmail_search("after:" + email_search_date)
    #UIDs = imapObj.search(['SINCE '+ email_search_date])
    #print(UIDs)
    print("You have " + str(len(UIDs)) + " recent emails.\n")
    time.sleep(1)
    def fetch_email(pos,email_num):
        rawMessages = imapObj.fetch(UIDs, ["BODY[]"])
        message = pyzmail.PyzMessage.factory(rawMessages[UIDs[pos]][b'BODY[]'])
        readable_text = ""
        if message.text_part != None:
            readable_text += str(message.text_part.get_payload().decode())
        # this is code for handling HTML:
        # if message.html_part != None:
        # readable_text += "\n" + str(message.html_part.get_payload().decode(message.html_part.charset))
        print("\t" + "Email " + str(email_num) + "\n")
        time.sleep(.6)
        print("\nEmail from: " + str(message.get_address('from')[1]) + "\n\n\"" + str(
            message.get_subject()) + "\"\n\n" + readable_text)
        if pos > 0:
            email_num += 1
            pos -= 1
            next_ask = input("\n\n\t'n' for next email, 'off' to stop: \n").lower()
            print("\n")
            if next_ask == "n":
                fetch_email(pos,email_num)
    fetch_email(len(UIDs)-1,1)

# This is now obsolete:
def save_email():
    x = input("\n'save' allows you to enter and store your email account information.\nWould you like to proceed (Y/n)?\n").lower()
    if x == "y":
        email_ad = input("Enter your email adress: ").lower()
        password = input("Enter password: ")
        # ADD ABILITY TO CHECK IF NUMBER HAS BEEN USED
        account_num = input("Enter a user number for your account:")
        new_file_name = "email_account_" + account_num + ".txt"
        file_1 = open(new_file_name, "w")
        new_file_text = "A" + email_ad + "P" + password
        file_1.write(new_file_text)
        file_1.close()
        print("Your email account information has been saved as account #" + account_num + "\n\n")
        time.sleep(2)


# runs the email app
def email():
    x = "on"
    while x != "off":
        print("\tEMAIL\n")
        print("\t\t'send' 'read' 'save' 'off'")
        x = input()
        if x == "send":
            send_email()
        if x == "read":
            read_email()
        if x == "save":
            save_email()


def phys():
    print("\nEnter knowns. Enter unknowns as \".0\"\n")
    time.sleep(.5)
    try:
        v_i = float(input("Initial Velocity (m/s): "))
        v_f = float(input("Final Velocity (m/s): "))
        a = float(input("Acceleration (m/s^2): "))
        t = float(input("Time (s): "))
        d = float(input("Distance (d): "))
    except(ValueError):
        time.sleep(.5)
        print("\nInvalid Input")
        time.sleep(1)
        phys()


    print("\n")

    # finds final velocity
    def find_v_f(v_i, a, t):
        return v_i + a * t

    # finds initial velocity
    def find_v_i(v_f, a, t):
        return v_f - (a * t)

    # finds acceleration
    def find_a(v_f, v_i, t):
        return (v_f - v_i) / t

    # finds time
    def find_t(v_f, v_i, a):
        return (v_f - v_i) / a

    # finds v_i (with distance)
    def find_v_i_with_d(a, t, d):
        return (-0.5 * a * t * t + d) / t

    time.sleep(.5)

    # decides what function to run

    # runs if doesn't have v_f, and fines v_i
    if v_f == .0 and v_i != .0 and a != .0 and t != .0:
        print("Final Velocity: " + str(find_v_f(v_i, a, t)))
    # runs if doensn't have v_i, and finds v_i
    elif v_i == .0 and v_f != .0 and a != .0 and t != .0:
        print("Initial Velocity: " + str(find_v_i(v_f, a, t)))
    # runs if doensn't have a, and finds a
    elif a == .0 and v_f != .0 and v_i != .0 and t != .0:
        print("Acceleration: " + str(find_a(v_f, v_i, t)))
    # runs if doensn't have t, and finds t
    elif t == .0 and v_f != .0 and v_i != .0 and a != .0:
        t = find_t(v_f, v_i, a)
        if t >= 0:
            print("Time: " + str(t))
        else:
            print("Invalid Knowns (would result in negative time)")
            print("Time: " + str(t))
    # runs if doesn't have v_i or v_f but has d, t, and a
    elif v_f == .0 and v_i == .0 and t != .0 and a != .0 and d != .0:
        v_i = find_v_i_with_d(a, t, d)
        print("Initial Velocity: " + str(v_i))
        # now finds v_f
        v_f = find_v_f(v_i, a, t)
        print("Final Velocity: " + (str(v_f)))
    else:
        print("Knowns are invalid, or calculator does not yet have this ability.")

    # finds distance
    if d == .0:
        d = (v_i * t) + 0.5 * a * t * t
        print("Distance: " + str(d))
    print("\n")
    time.sleep(1)


#FINNISH THIS
def calc_nums():
    calculate = input("Enter math problem:\n")
    print("\n" + str(calculate) + " = " + str(eval(calculate)) + "\n\n")
    time.sleep(1.2)


def calc():
    x = "on"
    while x != "off":
        print("\tCALCULATOR\t")
        print("\t\t'calc' 'phys' 'off'")
        x = input()
        if x == "calc":
            calc_nums()
        if x == "phys":
            phys()

user = "***"
def log_in():
    saved = input("Do you have a login account (Y/n)?\n").lower()
    if saved == "y":
        username = input("Enter your username:\n").lower()
        
        def password_check(username_param):
            file_name_op = ("user_" + username_param + ".txt")
            try:
                open_file = open(file_name_op, "r+")
            except IOError:
                print("\nThat username doesn't exist.\n")
                time.sleep(1)
                log_in()
                return
            else:
                open_file = open(file_name_op, "r+")
                info = open_file.read()
                pas_attempt = input("Enter your password:\n")

                pas_idx_start = info.index(";2P;")
                pas_idx_end = info.index("#2P#")
                password = info[pas_idx_start + 4:pas_idx_end]
                if pas_attempt == password:
                    open_file.close()
                    global logged_in
                    logged_in = True
                    global user
                    user = username
                    time.sleep(.4)
                    print("\nYou are now logged in as " + username + ".\n\n")
                    time.sleep(1.5)
                else:
                    time.sleep(.5)
                    print("Incorrect Password\n")

                    continue_pascheck = input("Do you know your password? (Y/n)\n")
                    if continue_pascheck != "Y" or "y":
                        log_in()
                        return
                    
                    time.sleep(.5)
                    open_file.close()
                    password_check(username)
                    return
        
        password_check(username)

    else:
        def revert(entering):
            print("\nInvalid " + entering + "\n")
            time.sleep(.5)
            print("Please restart.\n")
            time.sleep(.8)
            log_in()
            
            
        save_it = input("\nWould you like to create a login account? (Y/n):\n").lower()
        
        if save_it == "y": 
            username = input("Enter a username (do not use special characters):\n").lower()
            if "#" in username:
                revert("username")
            elif ";" in username:
                revert("username")
            else:
                new_file_name = ("user_" + username + ".txt")
                
                
                
                
                """
                file_1 = open(new_file_name, "w")
                new_file_text = ";1U;" + username + "#1U#" + ";2P;" + password + "#2P#"
                file_1.write(new_file_text)
                file_1.close()
                print("Your login, " + username + ", has been saved\n\n")
                time.sleep(2)
                log_in()
                """
            
            password = input("Enter password (case sensitive, do not use special characters): \n")
            if "#" in password:
                revert("password")
            elif ";" in password:
                revert("password")
            else:    
                new_file_name = ("user_" + username + ".txt")
                file_1 = open(new_file_name, "w")
                new_file_text = ";1U;" + username + "#1U#" + ";2P;" + password + "#2P#" + "#"
                file_1.write(new_file_text)
                file_1.close()
                print("Your login, " + username + ", has been saved\n\n")
                time.sleep(2)
                log_in()


# allows user to save email to account
def email_account():
    file_name_op = ("user_" + user + ".txt")
    open_file = open(file_name_op, "r+")
    info = open_file.read()
    pas_idx_end = info.index("#2P#")
    
    if info[pas_idx_end + 4:] == "#":
        email_address = input("Enter your email address:\n")
        email_password = input("Enter your email password:\n")
        new_file_text = ";3A;" + email_address + "#3A#" + ";4E;" + email_password + "#4E#" + "#"
        open_file.write(new_file_text)

        #set_email_info_vari()

        time.sleep(1.8)
        print("Your email, " + email_address + ", has been saved.\n\n")

    else:

        try:
            info[pas_idx_end + 8] == None
        except IndexError:
            yes = input("\nYou have an outdated account. Would you like to update your account? (Y/n)\n").lower()
            if yes == "y":

                open_file.write("#")
                time.sleep(1.2)
                print("Your account has been updated.\n\n")
                open_file.close()
                time.sleep(1)
                email_account()
                return
            else:
                return

        print("You have already saved an email to your account.\n")
        time.sleep(1)

    open_file.close()


# runs the account app
def account():
    x = "on"
    while x != "off":
        print("\tACCOUNT\t")
        print("\t\t'email' 'view' 'off'")
        x = input()
        if x == "email":
            email_account()
        if x == "view":
            print("still in progress...")


# checks if account has email, sets email info as global variables
def set_email_info_vari():
    if logged_in:
        file_name_op = ("user_" + user + ".txt")
        open_file = open(file_name_op, "r+")
        info = open_file.read()
        try:
            pas_idx_end = info.index("#2P#")
            info[pas_idx_end + 6] == "3"
        except IndexError:
            return
        pas_idx_end = info.index("#2P#")
        if info[pas_idx_end + 6] == "3":
            global has_email
            has_email = True
            global global_email_address
            global global_email_password
            email_ad_idx_start = info.index(";3A;")
            email_ad_idx_end = info.index("#3A#")
            global_email_address = info[email_ad_idx_start + 4:email_ad_idx_end]
            email_pas_idx_start = info.index(";4E;")
            email_pas_idx_end = info.index("#4E#")
            global_email_password = info[email_pas_idx_start + 4:email_pas_idx_end]
        open_file.close()





# runs the program
x = "on"
print("Hello!\n")
time.sleep(.5)
log_in()
set_email_info_vari()



while x != "off":
    if logged_in == True:
        print("\n" + date_and_time_data + "\nLogged in as: " + user + "\n")
    else:
        print("\n" + date_and_time_data + "\nUsing as guest." + "\n")


    x = input("Enter:  'files' 'weather' 'email' 'calc' 'login' 'account' 'off' '?'\n").lower()
    if x == "files":
        files()
    if x == "weather":
        print("\n" + weather()+ "\n")
    if x == "email":
        email()
    if x == "calc":
        calc()
    if x == "login":
        if logged_in == True:
            print("\nYou are already logged in.\n")
        else:
            print("\n")
            log_in()
    if x == "account":
        if logged_in == True:
            account()
        else:
            print("You are not logged in.")
    if x == "?":
        print("Enter: \n'files' to open the files app and work with files \n'weather' to get a weather report \n'email' to send an email \n'calc' to use the calculator app \n'login' to login with an account, or to create an account \n'account' to edit your user account \n'off' to close the program")

print("Ending Program...")
time.sleep(1)

#tag files with profile, only let you open if tagged with your profile
#list users files
#check if username is taken (look for file) -handle no file found erorr
#make profile as a class (save email info, files, etc.)
#create activity log (times, apps opened)
