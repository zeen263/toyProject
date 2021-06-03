from flask import Flask, render_template, request
from random import randint


user_id=['guest','jiin'] # add more user
user_pw=['0000','1234']

gift_list=['gift1','gift2','gift3'] # add more gift
got_gift=[None,None,None]

income_id=u""
income_pw=u""
current_user=current_user_index=None

app = Flask(__name__)

@app.route("/") 
def mainPage():
        return render_template('login.html')

@app.route("/gift/greet", methods=['post'])
def Greet():
        global current_user, current_user_index
        income_id = request.form['id']
        income_pw = request.form['pw']

        if income_id in user_id and income_pw == user_pw[user_id.index(income_id)]:
                current_user = income_id
                current_user_index = user_id.index(income_id)
                return render_template('greet.html', ID=income_id, PW=income_pw) 
                
        else:
                return render_template('login_fail.html') 


@app.route("/gift/open", methods=['post'])
def Open():
        income_id = request.form['id']
        income_pw = request.form['pw']

        if income_id in user_id and income_pw == user_pw[user_id.index(income_id)]:
                return render_template('open.html', ID=income_id, PW=income_pw)
        else:
                return render_template('login_fail.html')
        
@app.route("/gift/congrats", methods=['post'])
def Congrats():
        global got_gift
        income_id = request.form['id']
        income_pw = request.form['pw']

        if current_user=='guest':
                got_gift[0]=None
        
        if got_gift[current_user_index] == None:
                num=randint(1,100)
                if num<=33: got_gift[current_user_index] = gift_list[0];      #airfrier
                elif num<=66: got_gift[current_user_index] = gift_list[1];  #scarf
                else: got_gift[current_user_index] = gift_list[2];          #nerf
        
        if income_id in user_id and income_pw == user_pw[user_id.index(income_id)]:
                return render_template('congrats.html', ID=income_id, PW=income_pw,GIFT=got_gift[current_user_index]) # need rebuild
        else:
                return render_template('login_fail.html')
        
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug= True, port=80)






