from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
import os 
import subprocess 
from werkzeug.utils import secure_filename
from string import Template
from datetime import date, datetime
import time
from plotly import graph_objs as go
import numpy as np
import csv


output_file=""
if not os.path.exists('uploads'):
    os.makedirs('uploads')
    user_info_file=open(os.getcwd()+'/uploads/users.txt','w+')
    user_info_file.close()
UPLOAD_FOLDER = os.getcwd() + '/uploads'
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
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            working_file=open(os.getcwd()+"/uploads/"+filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "temp.fasta"))
            temp_output_file=open(os.getcwd()+'/uploads/temp.fasta',"w+")
            for lines in working_file:
                if ">" in lines:
                    lines=""
                else:
                    temp_output_file.write(lines)           
            temp_output_file.close()            
            email=request.form.get("user_email")
            command_line = "zhunt 12 6 12 ./uploads/temp.fasta"
        
            stream=os.popen(command_line)
            output=stream.read()
            output
            
            os.rename(os.getcwd()+'/uploads/temp.fasta.Z-SCORE', os.getcwd()+"/uploads/"+filename+".Z-SCORE")            
            output_file="/uploads/"+filename+".Z-SCORE"
            user_info=open(os.getcwd()+'/uploads/users.txt','a')
            now=datetime.now()
            now=str(now)
            user_info.write(now + ": ")
            user_info.write(filename + " ")
            user_info.write(email + "\n")
            user_info.close()

            if os.path.exists(os.getcwd()+'/templates/figure.html'):
                os.remove(os.getcwd()+'/templates/figure.html')
            
            return render_template("downloads.html", output_file=output_file)
    return render_template("index.html")

@app.route('/return-file/', methods=['get','post'])
def downloadFile ():
    filename = request.form['download_output_file']
    path = os.getcwd() + filename
    return send_file(path, as_attachment=True)

@app.route('/see_graph/', methods=['get','post'])
def see_data ():
    filename = request.form['output_file']
    df_file="."+filename
    df=np.loadtxt(df_file, skiprows=1, usecols=[2],dtype=str)
    fig = go.Figure(data=go.Bar(y=df,marker_color="#000000"))
    fig.update_layout(xaxis=dict(title="Sequence"),yaxis=dict(title="Z-SCORE"),paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    run_filename= filename[8:] + "_figure.html"
    fig.write_html('./templates'+run_filename)
    return render_template(run_filename)

@app.route('/Z-mhunt/', methods=['GET', 'POST'])
def methyl_upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            working_file=open(os.getcwd()+"/uploads/"+filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "temp.fasta"))
            temp_output_file=open(os.getcwd()+'/uploads/temp.fasta',"w+")
            for lines in working_file:
                if ">" in lines:
                    lines=""
                else:
                    temp_output_file.write(lines)           
            temp_output_file.close()            
            email=request.form.get("methyl_user_email")
            command_line = "mhunt 12 6 12 ./uploads/temp.fasta"
        
            stream=os.popen(command_line)
            output=stream.read()
            output
            
            os.rename(os.getcwd()+'/uploads/temp.fasta.Z-SCORE.txt', os.getcwd()+"/uploads/"+filename+".Z-SCORE")            
            output_file="/uploads/"+filename+".Z-SCORE"
            user_info=open(os.getcwd()+'/uploads/methyl_users.txt','a')
            now=datetime.now()
            now=str(now)
            user_info.write(now + ": ")
            user_info.write(filename + " ")
            user_info.write(email + "\n")
            user_info.close()    
            
            for document in os.listdir('./templates/'):
                if document.endswith('figure.html'):
                    os.remove('./templates/' + document)
                    
            
            return render_template("mhunt_downloads.html",output_file=output_file)
    return render_template("mhunt_index.html")

@app.route('/methyl_return-file/', methods=['get','post'])
def methyl_downloadFile ():
    filename = request.form['download_output_file']
    path = os.getcwd() + filename
    return send_file(path, as_attachment=True)

@app.route('/methyl_see_graph/', methods=['get','post'])
def methyl_see_data ():
    filename = request.form['output_file']
    df_file="."+filename
    df=np.loadtxt(df_file, skiprows=1, usecols=[2],dtype=str)
    fig = go.Figure(data=go.Bar(y=df))
    fig.update_layout(xaxis=dict(title="Sequence"),yaxis=dict(title="Z-SCORE"))
    run_filename= filename[8:] + "_figure.html"
    fig.write_html('./templates'+run_filename)
    return render_template(run_filename)

@app.route('/codes/',methods=['get','post'])
def codes():
    return render_template("code.html")

@app.route('/about/',methods=['get','post'])
def about():
    return render_template("about.html")

@app.route('/research/',methods=['get','post'])
def research():
    return render_template("research.html")

@app.route('/contact/',methods=['get','post'])
def contact():
    return render_template("contact.html")


#To be able to run the analysis within the website

@app.route('/return-r-files/', methods=['get','post'])
def downloadRFiles ():
    
    filename = request.form['download_output_file']
    command_line = "Rscript /zhunt/graph.r " + os.getcwd()+"/uploads/"+filename + " " + os.getcwd()+"/uploads/temp.fasta"
        
    stream=os.popen(command_line)
    output=stream.read()
    output
    
    location = os.getcwd() + "/uploads/"
    
    stream=os.popen("zip -r " + location + "temp.zip NTS_\&_Sum_Zscore.pdf Z-score_across_Sequence.pdf")
    output=stream.read()
    output
    
    path=location + "temp.zip"
    
    return send_file(path, as_attachment=True)