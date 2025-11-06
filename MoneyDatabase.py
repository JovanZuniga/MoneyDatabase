import sqlite3
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Money Spent Database")
root.geometry("500x500")
root.config(bg="#000000")
root.wm_attributes("-topmost", True)

#Create Database
conn = sqlite3.connect('transactions.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS transactions (
        id integer PRIMARY KEY AUTOINCREMENT,
        card_name text NOT NULL,
        amountDollars integer NOT NULL,
        amountCents integer NOT NULL, 
        description text NOT NULL
          )
          """)
conn.commit()
conn.close()

def submit():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute(" INSERT INTO transactions VALUES (:id, :card_name, :amountDollars, :amountCents, :description)", 
              {
                'id': None,
                  'card_name': card_cbox.get(),
                  'amountDollars': amtDollars.get(),
                  'amountCents': amtCents.get(),
                  'description': descrip.get()
              })
    conn.commit()
    conn.close()

    card_cbox.set('Select a Card')
    amtDollars.delete(0, END)
    amtCents.delete(0, END)
    descrip.delete(0, END)

#Query the database
def query():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute(" SELECT * FROM transactions")
    records = c.fetchall()
    queryList.config(text=records)
    print(records)
    conn.commit()
    conn.close()

#Validate Entry is less than 5 digits
def validate(P):
    if len(P) == 0:
        #empty is ok
        return True
    elif len(P) <= 5 and P.isdecimal():
        return True
    else:
        return False
    
vcmd = (root.register(validate), '%P')

    
text_var1 = StringVar()
text_var2 = StringVar()
text_var3 = StringVar()
text_var4 = StringVar()


#Create Layout
topFrame = Frame(root)
topFrame.pack(side='top', padx=20, pady=(20, 5), fill='both')
topFrame.columnconfigure(0, weight=1)
# topFrame.columnconfigure(1, weight=1)
topFrame.columnconfigure(2, weight=1)

bottomFrame = Frame(root)
bottomFrame.pack(side='bottom', padx=10, pady=(5, 10))

titleLbl = Label(topFrame, text="Enter a New Record")
titleLbl.grid(column=0, row=0, columnspan=3)
#Dropdown List
card_options = ["Discover Debit", "Discover Credit", "Capital One", "Blue Cash Everyday", "Wells Fargo", "Paypal", "Costco"]

card_cbox = ttk.Combobox(topFrame, values=card_options, textvariable=text_var3)
card_cbox.set("Select a Card")
card_cbox['state'] = 'readonly'
card_cbox.grid(row=3, column=1)

amtFrame = Frame(topFrame)
amtFrame.grid(row=1, column=1, columnspan=3)


amtLbl = Label(amtFrame, text="Amount:   $")
amtLbl.pack(side='left')

#Entry
amtDollars = Entry(amtFrame, width=5, textvariable=text_var1, validate="key", validatecommand=vcmd)
amtDollars.pack(side='left')
amtLbl2 = Label(amtFrame, text='.')
amtLbl2.pack(side='left')
amtCents = Entry(amtFrame, width=2, textvariable=text_var4)
amtCents.pack(side='left')


descrip = Entry(topFrame, width=20, textvariable=text_var2)
descrip.grid(row=2, column=1)


def clear():
    amtDollars.delete(0, END)
    amtCents.delete(0, END)
    descrip.delete(0, END)
    card_cbox.set("Select a Card")


#Submit Button
submitBtn = Button(topFrame, text="Submit Record", command=submit)
submitBtn.config(state='disabled')
submitBtn.grid(row=4, column=1)

def checkButton(*args):
    if text_var1.get() and text_var2.get() and text_var4.get() != '' and card_cbox.get() != "Select a Card":
        submitBtn.config(state='normal')
    else:
        submitBtn.config(state='disabled')

text_var1.trace('w', checkButton)
text_var2.trace('w', checkButton)
text_var4.trace('w', checkButton)
card_cbox.bind('<<ComboboxSelected>>', checkButton)

#Clear Button
clearBtn = Button(topFrame, text="Clear", command=clear)
clearBtn.grid(row=5, column=1)

#Query Button
queryBtn = Button(bottomFrame, text="Load Records", command=query)
queryBtn.pack()

queryList = Label(bottomFrame)
queryList.pack()

root.mainloop()