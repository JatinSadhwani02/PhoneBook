from tkinter import *
import pymysql
from tkinter import ttk
from tkinter import messagebox

class Phonebook:
	def __init__(self,root):
		self.root = root
		self.root.title('Phone Book')
		self.root.geometry('500x600')

		self.name=StringVar()
		self.contact=StringVar()
		#Heading
		headinglbl = Label(root,text='Phone Book' ,font=('algerian',50,'bold'))
		headinglbl.pack(side=TOP)

	   
		


		#Functions

		def addcontact():
			if self.name.get()!='' and (len(self.contact.get())==10 or len(self.contact.get())==13) :
				con=pymysql.connect(host='localhost',user='root',password='',database='phonebook')
				cur=con.cursor()
				cur.execute('insert into contact values(%s,%s)',(self.name.get(),self.contact.get()))
				con.commit()
				con.close()
				focus()
				self.name.set("")
				self.contact.set("")
				messagebox.showinfo('Success','Record has been submitted')
			else:
				messagebox.showinfo('Alert','Please fill correct fields')

		
		def focus():
			con=pymysql.connect(host='localhost',user='root',password='',database='phonebook')
			cur=con.cursor()
			cur.execute('select * from contact')
			rows=cur.fetchall()

			if len(rows)!=0:
				listview.delete(*listview.get_children())

				for row in rows:
					listview.insert('',END,values=row)

				con.commit()
			
			con.close()
		
		def filldata(e):
			cursor=listview.focus()
			content=listview.item(cursor)
			row=content['values']
			self.name.set(row[0])
			self.contact.set(row[1])

		def deletecontact():
			con=pymysql.connect(host='localhost',user='root',password='',database='phonebook')
			cur=con.cursor()
			cur.execute('delete from contact where Contact_no=%s ',self.contact.get())
			con.commit()
			con.close()
			focus()
			self.name.set("")
			self.contact.set("")
			messagebox.showinfo('Success','Record has been deleted')


		 # Treeview
		bookframe = Frame(root,bd=4,relief='ridge',bg='red' ,width=400,height=300)
		bookframe.pack()

		y_scroll=Scrollbar(bookframe,orient=VERTICAL)
		listview = ttk.Treeview(bookframe,columns=('Name','Contact no.'),yscrollcommand=y_scroll.set)
		y_scroll.pack(side=RIGHT,fill=Y)
		y_scroll.configure(command=listview.yview)

		listview.heading('Name',text='Name')
		listview.heading('Contact no.',text='Contact no.')
		listview['show'] = 'headings'

		listview.column('Name',width=130)
		listview.column('Contact no.',width=190)

		listview.bind('<ButtonRelease-1>',filldata)
		listview.pack()


		# Data
		dataframe = Frame(root,bd=4,relief='ridge',bg='red' ,width=400,height=1000)
		dataframe.pack()

		namelbl=Label(dataframe,text='Name',width=15,font=("arial",12,))
		namelbl.grid(row=0,column=0)

		contactlbl=Label(dataframe,text='Contact no.',width=15,font=("arial",12,))
		contactlbl.grid(row=1,column=0,padx=40)

		nameentry = Entry(dataframe,bd=3,relief='ridge',font=("",12),width=15,textvariable=self.name)
		nameentry.grid(row=0,column=1,padx=20,pady=20)

		contactentry = Entry(dataframe,bd=3,relief='ridge',font=("",12),width=15,textvariable=self.contact)
		contactentry.grid(row=1,column=1,padx=20,pady=20)

		addbtn = Button(dataframe,bd=3,relief='ridge',font=("",12,'bold'),width=15,text='Add contact',command=addcontact)
		addbtn.grid(row=2,column=0,padx=20,pady=20)

		deletebtn = Button(dataframe,bd=3,relief='ridge',font=("",12,'bold'),width=15,text='Delete contact',command=deletecontact)
		deletebtn.grid(row=2,column=1,padx=20,pady=20)

		focus()

		
		






root=Tk()
pb=Phonebook(root)
root.mainloop()