#flask testing
from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from Tkinter import * #Needed for the GUI portion
import Tkinter as tk
import os #Needed for the GUI portion 
import shlex, subprocess #Needed to call on the C program
from email.mime.multipart import MIMEMultipart #Needed to email user
from email.mime.text import MIMEText #Needed to email user
from werkzeug.utils import secure_filename
import smtplib
from string import Template

MY_ADDRESS = 'example@gmail.com' #need to setup an email account for this
PASSWORD = '####'
output_file=""
UPLOAD_FOLDER = '/Users/Team_HoLab/Desktop/RSC/Documents/Coding/Zhunt/uploads'
ALLOWED_EXTENSIONS = {'txt', 'fasta'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #f=open("./uploads/"+filename)
            email=request.form.get("user_email")
            command_line = "zhunt 12 6 12 ./uploads/" + filename
        
            args = shlex.split(command_line)
            p = subprocess.Popen(args)
            tmp=subprocess.call("./a.out")
            
            # message_template = "Your Zhunt run is complete"
            #         
            # # set up the SMTP server
            # s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            # s.starttls()
            # s.login(MY_ADDRESS, PASSWORD)
            # 
            # msg = MIMEMultipart()       # create a message
            # 
            # # setup the parameters of the message
            # msg['From']=MY_ADDRESS
            # msg['To']=request.form.get("user_email")
            # msg['Subject']="Zhunt Run Complete"
            #     
            # # add in the message body
            # msg.attach(MIMEText(message_template, 'plain'))
            # message = 'Subject: {}\n\n{}'.format("Zhunt Run Complete", message_template)    
            # # send the message via the server set up earlier.
            # s.sendmail(MY_ADDRESS,request.form.get("user_email"),message)                    
            # del msg
            #     
            # # Terminate the SMTP session and close the connection
            # s.quit()
            
            output_file="/uploads/"+filename+".Z-SCORE"

            return render_template("downloads.html",output_file=output_file)
    return '''
    <!doctype html>
    <title>Zhunt</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <style>
        body{
            padding:15px;
        }
    </style>
    <h1>Zhunt</h1>
    <body>
    <p>
            <br>Welcome to Zhunt.<br>
            <br>
            Please upload the .fasta file you would like to analyze and your email address to get an email after run completion.<br>
    </p>
    <form method=post enctype=multipart/form-data>
      FASTA File: <input type=file name=file></br>
      Email: <input type="text" name="user_email" /></br></br>
      <input type=submit value=Submit>
    </form>
    </body>
    '''

@app.route('/return-file/')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    filename = request.form['output_file']
    print(filename)

    path = "/Users/Team_HoLab/Desktop/RSC/Documents/Coding/Zhunt" + filename
    return send_file(path, as_attachment=True)
