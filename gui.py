import threading
from tkinter import *
# from PIL.ImageQt import rgb
import email_handler
import tkinter.scrolledtext as ScrolledText
import tkinter.font as font
from PIL import Image, ImageTk

contacts = dict()
root = Tk()
root.geometry("800x700")
root.title("HAK MESSENGER")
root.option_add( "*font", "Rockwell" )
root.configure(bg='white')
p1 = PhotoImage(file='Assets/iphoto.png')
root.iconphoto(False, p1)
sid = ""
counter_msg = 0
first_counter = 0

with open("counter_update.txt","r") as rr:
    num = ""
    for i in rr:
        num = i
    counter_msg = int(num)


def file_writer():
    with open("counter_update.txt", "w") as rw:
        rw.truncate(0)
        rw.write(str(counter_msg))

def message_reader():
    global counter_msg
    global sid
    service = email_handler.get_service()
    user_id = 'me'
    Output.tag_configure('tag-left', justify='left')
    while thread_receive.getName() == "Started":
        if len(sid) == 0:
            continue
        results = service.users().messages().list(userId=user_id, labelIds=['INBOX']).execute()
        msg = results.get('messages', [])
        for midx in range(10,-1,-1):
            rw = open(f".\Rec_Msgs\\{sid.split()[0]}_{sid.split()[1]}.txt", 'r+', encoding="utf-8")
            msg1 = msg[midx]
            mg = service.users().messages().get(userId='me', id=msg1['id']).execute()
            if contacts[sid] not in str(mg):
                rw.close()
                continue
            string = str(mg)
            rw.seek(0)
            flag = False
            for k in rw:
                k = k[k.find(' ') + 1:]
                if 'threadId' in k and eval(k)['id'] == mg['id']:
                    flag = True
                    break
            if flag:
                rw.close()
                continue
            if eval(string)['snippet'][0] != '$':
                continue
            service.users().messages().trash(userId='me', id=msg1['id']).execute()
            rw.write(str(counter_msg) + " " + string + "\n")
            counter_msg += 1
            dstring = ""
            count = 0
            for wd in eval(string)['snippet'][1:]:
                dstring += wd
                count += 1
                if count > 40:
                    dstring += "\n"
                    count = 0
            label1 = Label(Output, text=dstring, background='#ffffd0', justify='left', padx=10, pady=5)
            Output.configure(state='normal')
            Output.insert('end', '\n\n ', 'tag-left')  # space to move Label to the right
            Output.window_create('end', window=label1)
            Output.see(END)
            Output.update()
            Output.configure(state='disabled')
            rw.close()

def message_sender():
    global counter_msg
    global sid
    global inputtxt
    service = email_handler.get_service()
    Output.tag_configure('tag-right', justify='right')
    user_id = 'me'
    if len(sid) != 0:
        sender_id = contacts[sid]
    string = inputtxt.get("1.0", "end-1c").strip()
    string = "$" + string
    if len(sid) != 0:
        with open(f".\Sent_Msgs\{sid.split()[0]}_{sid.split()[1]}.txt","a") as wr:
            wr.write(str(counter_msg) + " " + string + "\n")
            counter_msg += 1
    if len(sid) != 0:
        msg = email_handler.create_message_with_attachment(user_id, sender_id, 'this is the subject line', string,'./sample_file.txt')
        email_handler.send_message(service, user_id, msg)
        dstring = ""
        count = 0
        for i in string[1:]:
            dstring += i
            count += 1
            if count > 40:
                dstring += "\n"
                count = 0
        label1 = Label(Output, text=dstring, background='#d0ffff', justify='left', padx=10, pady=5)
        Output.configure(state='normal')
        Output.insert('end', '\n\n ','tag-right')
        Output.window_create('end',window=label1)
        Output.see(END)
        Output.update()
        Output.configure(state='disabled')
    inputtxt.delete("1.0", "end")
    file_writer()


Output = ScrolledText.ScrolledText(width=5,background='#6E28FC')

button_font = font.Font(family='Rockwell',size=20)
l = Label(root,text="HAK MESSENGER", font=button_font, bg='white', fg='black')
inputtxt = Text(root, height=1,width=30, bg='white', fg='black', highlightcolor='White', highlightthickness=2)



# nav_bar = Scrollbar(root, bg="#5865f2", width=220, orient='vertical')
# nav_bar.pack(side='left',fill='y')
# root.config(yscrollcommand=nav_bar.set)

# nav_bar = Frame(root, yscrollcommand = scrollbar.set)
# scrollbar = Scrollbar(root,orient='vertical')
# scrollbar.pack(side = LEFT, fill = Y)
# nav_bar.pack(side='left', fill='both')

canvas_container=Canvas(root, width=230,height=700)
nav_bar=Frame(canvas_container)
myscrollbar=Scrollbar(root,orient="vertical",command=canvas_container.yview) # will be visible if the frame2 is to to big for the canvas
canvas_container.create_window((0,0),window=nav_bar,anchor='nw')
clist = []
def compare(item1, item2):
    a = int(item1.split()[1])
    b = int(item2.split()[1])
    if a < b:
        return -1
    else:
        return 1

contact_name =""
contact_id = ""
input_taker = ""
def contact_checker(name,emid):
    with open("contact_list.txt","r") as cl:
        for i in cl:
            nm = i.split()[0] + " " + i.split()[1]
            ed = i.split()[2]
            if nm == name or ed == emid:
                return False
    return True

def add_action(field1,field2,err):
    global clist
    if len(field1.get()) == 0 or len(field2.get()) == 0:
        err.config(text="Incorrect Field Input")
        return
    if len(field1.get().split()) != 2:
        err.config(text="Contact Name Must Have Exactly 2 Words")
        return
    if '@' not in field2.get():
        err.config(text="Invalid Email-ID")
        return
    if contact_checker(field1.get(),field2.get()):
        with open("contact_list.txt","a+") as cl:
            cl.write(f"{field1.get()} {field2.get()}\n")
        contacts[field1.get()] = field2.get()
        f = open(f".\Rec_Msgs\\{field1.get().split()[0]}_{field1.get().split()[1]}.txt",'x')
        f =  open(f".\Sent_Msgs\\{field1.get().split()[0]}_{field1.get().split()[1]}.txt", 'x')
        button_font = font.Font(family='Rockwell', size=12)
        button = Button(nav_bar, text="   " + field1.get(), height=70, width=220, command=lambda: contact_handler(len(clist)-1),
                        bg='white', font=button_font, borderwidth=0, anchor=W)
        button.config(image=master, compound=LEFT)
        button.pack(side=TOP, fill="both")
        nav_bar.update()
        canvas_container.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % nav_bar.winfo_height())

        clist.append(button)
        print(clist)
        input_taker.destroy()
    else:
        err.config(text="Input Provided Already In Use")
        return

image3 = Image.open('Assets/acbt.png')
resize_img = image3.resize((200, 70))
acbt = ImageTk.PhotoImage(resize_img)
def contact_adder():
    global input_taker
    input_taker = Toplevel()
    input_taker.geometry("700x130")
    input_taker.title("ADD CONTACT")

    lbl_a1 = Label(input_taker, text="Enter Name : ", width=20,bg="white")
    lbl_a1.grid(sticky="w", column=0, row=10, padx=10)
    entrybox_a1 = Entry(input_taker, width=30)
    entrybox_a1.grid(sticky="w", column=1, row=10)
    lbl_a2 = Label(input_taker, text="Enter Email-ID : ", width=20,bg="white")
    lbl_a2.grid(sticky="w", column=0, row=11, padx=10)
    entrybox_a2 = Entry(input_taker, width=30)
    entrybox_a2.grid(sticky="w", column=1, row=11)
    err = Label(input_taker, text="", fg="red", bg='white')
    err.grid(sticky="w", column=1, row=22)
    button = Button(input_taker,image=acbt,command=lambda: add_action(entrybox_a1,entrybox_a2,err),height=35,width=170,borderwidth=0,bg='white',activebackground='white')
    button.grid(sticky="w", column=1, row=13)

    input_taker.option_add("*font", "Rockwell")
    input_taker.configure(bg='white')

def contact_handler(idx):
    global label
    global first_counter
    if first_counter == 0:
        label.destroy()
        Output.pack(fill="both", expand=True)
        inputtxt.pack(side="left", fill="both", expand=True)
        Display.pack(side="right", fill="both", expand=False)

    l.config(text=clist[idx].cget('text').strip())
    global sid
    sid = ""
    Output.config(state='normal')
    Output.delete(1.0,END)
    Output.config(state='disabled')
    fn1 = clist[idx].cget('text').split()[0]
    fn2 = clist[idx].cget('text').split()[1]
    mg_lst = []
    with open(f".\Sent_Msgs\\{fn1}_{fn2}.txt", "r") as wr:
        with open(f".\Rec_Msgs\\{fn1}_{fn2}.txt", "r") as rw:
            for k in rw:
                if len(k) == 0 or len(k) == 1:
                    continue
                mg_lst.append("r " + k)
            for k in wr:
                if len(k) == 0 or len(k) == 1:
                    continue
                mg_lst.append("s " + k)
    print(mg_lst)
    mg_lst = sorted(mg_lst, key= lambda x: x.split()[1])
    for k in mg_lst:
        if k[0] == 'r':
            Output.tag_configure('tag-left', justify='left')
            dstring = ""
            count = 0
            k = k[2:]
            k = k[k.find(' ')+1:]
            for i in eval(k)['snippet'][1:]:
                dstring += i
                count += 1
                if count > 40:
                    dstring += "\n"
                    count = 0
            label1 = Label(Output, text=dstring, background='#ffffd0', justify='left', padx=10, pady=5)
            Output.configure(state='normal')
            Output.insert('end', '\n\n ', 'tag-left')  # space to move Label to the right
            Output.window_create('end', window=label1)
            Output.see(END)
            Output.update()
            Output.configure(state='disabled')
        else:
            Output.tag_configure('tag-right', justify='right')
            dstring = ""
            count = 0
            k = k[2:]
            k = k[k.find(' ') + 1:]
            print(k)
            print(mg_lst)
            for i in k[1:]:
                dstring += i
                count += 1
                if count > 40:
                    dstring += "\n"
                    count = 0
            label1 = Label(Output, text=dstring, background='#d0ffff', justify='left', padx=10, pady=5)
            Output.configure(state='normal')
            Output.insert('end', '\n\n ', 'tag-right')  # space to move Label to the right
            Output.window_create('end', window=label1)
            Output.see(END)
            Output.update()
            Output.configure(state='disabled')
    sid = clist[idx].cget('text').strip()

    if first_counter == 0:
        global thread_receive
        thread_receive.start()
        first_counter += 1

count = 0
originalImg = Image.open('Assets/user.png')
originalImg = originalImg.resize((40, 40))
master = ImageTk.PhotoImage(originalImg)

image = Image.open('Assets/abt.png')
resize_img = image.resize((50,40))
add_btn = ImageTk.PhotoImage(resize_img)
button = Button(root,image=add_btn,borderwidth=0,bg='#F14747',command=lambda: contact_adder(),width=60,height=70)
# nav_bar.insert('end',button)
button.pack(side=LEFT, fill="both")
def contact_list_retriever():
    with open("contact_list.txt",'r') as cl:
        for i in cl:
            contacts[i.split()[0] + " " + i.split()[1]] = i.split()[2]


contact_list_retriever()
for i in contacts.keys():
    button_font = font.Font(family='Rockwell',size=12)
    button = Button(nav_bar,text="   " + i, height=70, width=220,command=lambda idx = count:contact_handler(idx), bg='white',font=button_font, borderwidth=0,anchor=W)
    # nav_bar.insert('end',button)
    button.config(image=master,compound=LEFT)
    button.pack(side=TOP, fill="both")
    clist.append(button)
    count += 1
nav_bar.update()
canvas_container.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % nav_bar.winfo_height())
canvas_container.pack(side=LEFT)
myscrollbar.pack(side=LEFT, fill = Y)

image = Image.open('Assets/sbt.png')
resize_img = image.resize((70,70))
send_btn = ImageTk.PhotoImage(resize_img)
Display = Button(root,image=send_btn,command=lambda: message_sender(),borderwidth=0,bg='white')
l.pack()
Output.update()
label = Label(root, image = "",width=900,height=1200,bg="#4BB89F",anchor='center')
label.pack(fill="both",expand=True)
num = 0
img = None
frames = [PhotoImage(file = f"animater\\frame_{num}_delay-0.1s.gif") for num in range(20)]
def animate():
    global num
    global img
    label.configure(image = frames[num])
    num = (num+1)%20
    root.after(100, animate)
animate()






thread_receive = threading.Thread(target=message_reader)
thread_receive.name = "Started"
def x_button_pressed():
    thread_receive.name = "Closed"
    root.destroy()
root.protocol("WM_DELETE_WINDOW", x_button_pressed)
mainloop()