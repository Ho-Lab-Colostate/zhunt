from Tkinter import * #Needed for the GUI portion
import Tkinter as tk
import os #Needed for the GUI portion 
import shlex, subprocess #Needed to call on the C program
from email.mime.multipart import MIMEMultipart #Needed to email user
from email.mime.text import MIMEText #Needed to email user
import smtplib
from string import Template #

# Call upon the compiled zhunt program from the ./bin folder
MY_ADDRESS = '#####@gmail.com' #need to setup an email account for this
PASSWORD = '####'
    

class MyFirstGUI:
    def __init__(self,master):
        self.master=master
        master.title("DNA Translation")
        
        self.label=Label(master, text="DNA Translator")
        self.label.pack()
        self.label1=Label(master, text="Enter the file name (including .txt) for the sequence:")
        self.label1.pack()

        
        self.entry1=Entry(master)
        self.entry1.pack()
        
        self.label2=Label(master,text="Enter email address:")
        self.label2.pack()
        
        self.entry2=Entry(master)
        self.entry2.pack()
        
        #dna=Entry(master)
        #dna.pack()
        #dna.delete(0, END)
        #new_dna=dna
        
        def submit():
            def zhunt():
                print("zhunt 12 6 12 " + self.entry1.get())
            
            def read_template():
                """
                Returns a Template object comprising the contents of the 
                file specified by filename.
                """
                
                template_file_content = "Your Zhunt run is complete"
                return template_file_content
            
            def send_email():
                message_template = read_template()
            
                # set up the SMTP server
                s = smtplib.SMTP(host='smtp.gmail.com', port=587)
                s.starttls()
                s.login(MY_ADDRESS, PASSWORD)
            
                msg = MIMEMultipart()       # create a message
           
                # setup the parameters of the message
                msg['From']=MY_ADDRESS
                msg['To']=self.entry2.get()
                msg['Subject']="Zhunt Run Complete"
                    
                # add in the message body
                msg.attach(MIMEText(message_template, 'plain'))
                message = 'Subject: {}\n\n{}'.format("Zhunt Run Complete", message_template)    
                # send the message via the server set up earlier.
                s.sendmail(MY_ADDRESS,self.entry2.get(),message)
                del msg
                    
                # Terminate the SMTP session and close the connection
                s.quit()

            zhunt()
            send_email()
            print("Your run is complete, please close Submit window.\n")
        self.submit_button=Button(master, text="Submit", command=submit)
        self.submit_button.pack()

    
    
root=Tk()
root.geometry("400x200")
my_gui=MyFirstGUI(root)
root.mainloop()
