from flask import Flask, render_template,request,redirect,url_for,session
import os,subprocess

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot("FAQ",logic_adapters=[{
     "import_path": 'chatterbot.logic.BestMatch',
     "threshold": 0.2,
     "default_response": 'For more information,write us an email at info@zetech.ac.ke or call us on 0716 600 116 / 0720 554 555.'}
    ])

trainer = ChatterBotCorpusTrainer(chatbot)
data = "chatterbot.corpus.questions.faq"
trainer.train(data)

app= Flask(__name__)

app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')#start page
def index():
    return render_template('home.html')

@app.route('/redirect',methods=['POST'])#talk to us button
def redir():
    return render_template('index.html')

@app.route('/admin',methods=['POST'])#for admin login button
def admin():
    return render_template('admin.html')


@app.route('/login', methods=['POST'])#handles login form for admin
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('panel.html')
    return render_template('admin.html', error=error)

@app.route('/signout',methods=['GET','POST'])
def signout():
    session.pop('username',None)
    return render_template('admin.html')

@app.route('/panel')#admin page
def panel():
    return render_template('panel.html')

@app.route('/buttons',methods=['GET','POST'])#admin button functions
def buttons():
    message = None
    if request.method=='POST':
        if request.form['Delete_button'] =='Delete data':
            chatbot.storage.drop()
            message = 'Data cleared'
    return render_template('panel.html',message=message)


@app.route('/edit',methods=['GET','POST'])
def edit():
    if request.method=='POST':
        if request.form['edit_button'] == 'Edit data':
                subprocess.Popen([r'C:\Program Files (x86)\Brackets\\Brackets.exe'])
    return render_template('panel.html')


@app.route('/process',methods=['POST'])
def process():            
    user_input=request.form['user_input']
    response = chatbot.get_response(user_input)
    print("Bot: ",response)
    if user_input not in data:
        t = open("new data.txt","a+")
        t.write(user_input+"\n")  
    return render_template('index.html',user_input=user_input,response=response)

@app.route('/view',methods=['GET','POST'])
def view():
    if request.method == 'POST':
        if request.form['view_button'] == 'view':
            e = open("new data.txt","r+")
            content = e.readlines()
            e.close()
    return render_template('panel.html',content=content)

if __name__ == "__main__":
    app.run(debug=True,threaded=True)
    