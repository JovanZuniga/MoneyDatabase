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

    card_cbox.selection_clear()
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
    
            
#Create Layout
topFrame = Frame(root)
topFrame.pack(side='top', padx=10, pady=(10, 5))

bottomFrame = Frame(root, )
bottomFrame.pack(side='bottom', padx=10, pady=(5, 10))

#Create Attributes

#Check if any attritbutes have no value
# global notSelected;
notSelected = True

#Dropdown List
card_options = ["Discover Debit", "Discover Credit", "Capital One", "Blue Cash Everyday", "Wells Fargo", "Paypal", "Costco"]

card_cbox = ttk.Combobox(topFrame, values=card_options)
card_cbox.set("Select a Card")
card_cbox['state'] = 'readonly'
card_cbox.pack()

#Track Entry Changes
def on_text_change(*args):
    if(amount.get() and descrip.get() != ''):
      notSelected = False

text_var = StringVar()
text_var.trace_add("write", on_text_change)


#Entry
amount = Entry(topFrame, width=10, textvariable=text_var)
amount.pack()


descrip = Entry(topFrame, width=20, textvariable=text_var)
descrip.pack()


def clear():
    amount.delete(0, END)
    descrip.delete(0, END)
    card_cbox.set("Select a Card")


#Submit Button
submitBtn = Button(topFrame, text="Submit Record", command=submit)
submitBtn.pack()

#Clear Button
clearBtn = Button(topFrame, text="Clear", command=clear)
clearBtn.pack()

#Query Button
queryBtn = Button(bottomFrame, text="Load Records", command=query)
queryBtn.pack()

queryList = Label(bottomFrame)
queryList.pack()

if(notSelected):
    submitBtn.config(state='disabled')
else:
    submitBtn.config(state='normal')




root.mainloop()