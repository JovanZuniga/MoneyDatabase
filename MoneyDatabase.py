import sqlite3
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Money Spent Database")
root.geometry("500x500")
root.config(bg="#38f7f7")
root.wm_attributes("-topmost", True)

#Create Database
conn = sqlite3.connect('transactions.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS transactions (
        id integer PRIMARY KEY AUTOINCREMENT,
        card_name text NOT NULL,
        amount integer NOT NULL,
        description text NOT NULL
          )
          """)
conn.commit()
conn.close()

def submit():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute(" INSERT INTO transactions VALUES (:id, :card_name, :amount, :description)", 
              {
                'id': None,
                  'card_name': card_cbox.get(),
                  'amount': amount.get(),
                  'description': descrip.get()
              })
    conn.commit()
    conn.close()

    card_cbox.set('Select a Card')
    amount.delete(0, END)
    descrip.delete(0, END)

def query():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute(" SELECT * FROM transactions")
    records = c.fetchall()
    queryList.config(text=records)
    print(records)
    conn.commit()
    conn.close()

    
text_var1 = StringVar()
text_var2 = StringVar()
text_var3 = StringVar()


#Create Layout
topFrame = Frame(root)
topFrame.pack(side='top', padx=10, pady=(10, 5))

bottomFrame = Frame(root, )
bottomFrame.pack(side='bottom', padx=10, pady=(5, 10))

#Dropdown List
card_options = ["Discover Debit", "Discover Credit", "Capital One", "Blue Cash Everyday", "Wells Fargo", "Paypal", "Costco"]

card_cbox = ttk.Combobox(topFrame, values=card_options, textvariable=text_var3)
card_cbox.set("Select a Card")
card_cbox['state'] = 'readonly'
card_cbox.pack()

#Entry
amount = Entry(topFrame, width=10, textvariable=text_var1)
amount.pack()


descrip = Entry(topFrame, width=20, textvariable=text_var2)
descrip.pack()


def clear():
    amount.delete(0, END)
    descrip.delete(0, END)
    card_cbox.set("Select a Card")


#Submit Button
submitBtn = Button(topFrame, text="Submit Record", command=submit)
submitBtn.config(state='disabled')
submitBtn.pack()

def checkButton(*args):
    if text_var1.get() and text_var2.get() != '' and card_cbox.get() != "Select a Card":
        submitBtn.config(state='normal')
    else:
        submitBtn.config(state='disabled')

text_var1.trace('w', checkButton)
text_var2.trace('w', checkButton)
card_cbox.bind('<<ComboboxSelected>>', checkButton)

#Clear Button
clearBtn = Button(topFrame, text="Clear", command=clear)
clearBtn.pack()

#Query Button
queryBtn = Button(bottomFrame, text="Load Records", command=query)
queryBtn.pack()

queryList = Label(bottomFrame)
queryList.pack()

root.mainloop()