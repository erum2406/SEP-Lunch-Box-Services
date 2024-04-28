from flask import Flask, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
import json

with open ('config.json','r') as c:
    params=json.load(c)["params"]
    
local_server=True

app = Flask(__name__)
app.secret_key='Prateek-Secret-Key'

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['pro_uri']
    
db = SQLAlchemy(app)

class book_table_data(db.Model):
    S_No = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Date_Time = db.Column(db.String(50), nullable=False)
    People = db.Column(db.Integer, nullable=False)
    Request = db.Column(db.String(100), nullable=False)
    E_Mail = db.Column(db.String(100), nullable=False)

class login_user_data(db.Model):
    L_S_No = db.Column(db.Integer, primary_key=True, nullable=False)
    L_Name = db.Column(db.String(20), nullable=False)
    L_Phone_Number = db.Column(db.String(20), nullable=False)
    L_E_Mail = db.Column(db.String(20), nullable=False)
    L_Pass = db.Column(db.String(20), nullable=False)
    L_Con_Pass = db.Column(db.String(20), nullable=False)
    
class membership_table(db.Model):
    # M_S_No 	M_Name 	M_E_Mail 	M_Start_Date 	M_Address 	M_CIty 	M_State 	M_Pin_Code 	M_Menu_Type 	M_Phone
    M_S_No = db.Column(db.Integer, nullable=False)
    M_Name = db.Column(db.String(20), nullable=False)
    M_E_Mail = db.Column(db.String(20), primary_key=True, nullable=False)
    M_Start_Date = db.Column(db.String(20), nullable=False)
    M_No_Months = db.Column(db.Integer, nullable=False)
    M_Address = db.Column(db.String(50), nullable=False)
    M_CIty = db.Column(db.String(10), nullable=False)
    M_State = db.Column(db.String(10), nullable=False)
    M_Pin_Code = db.Column(db.Integer, nullable=False)
    M_Menu_Type = db.Column(db.String(10), nullable=False)
    M_Phone = db.Column(db.String(13), nullable=False)
    
    
@app.route("/",methods=['GET', 'POST'])
def index():
    # if ('user' in session) :
    #     return render_template('Profile.html', params=params)
    
    if (request.method == 'POST'):
        # return render_template('home.html', params=params,dtaa=dtaa)
        '''Add Entry To Database'''
        dtaa=login_user_data.query.filter_by().all()
        User_Email = request.form.get('User_Email')
        Create_Pass = request.form.get('Create_Pass')
        # print(User_Email)
        for login in dtaa:
            if (User_Email==login.L_E_Mail and Create_Pass==login.L_Pass):
                session['user']=User_Email
                return render_template('Home.html', params=params)
        return render_template('index.html', params=params,dtaa=dtaa)
    else : 
        return render_template('index.html', params=params)


@app.route("/login",methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        '''Add Entry To Database'''
        user_name = request.form.get('user_name')
        User_Email = request.form.get('User_Email')
        User_Num = request.form.get('User_Num')
        Create_Pass = request.form.get('Create_Pass')
        Confirm_Pass = request.form.get('Confirm_Pass')
        # S_No 	Name 	E_Mail 	Date_Time 	People 	Reques
        entry = login_user_data(L_Name=user_name, L_E_Mail=User_Email, L_Phone_Number=User_Num, L_Pass=Create_Pass, L_Con_Pass=Confirm_Pass)
        if(Create_Pass==Confirm_Pass):
            db.session.add(entry)
            db.session.commit()
    return render_template('login_Page_2.html', params=params)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/booking", methods=['GET', 'POST'])
def booking():
    if (request.method == 'POST'):
        '''Add Entry To Database'''
        name = request.form.get('name')
        Email = request.form.get('email')
        date = request.form.get('date')
        People = request.form.get('People')
        Special = request.form.get('Special')
        # S_No 	Name 	E_Mail 	Date_Time 	People 	Reques
        entry = book_table_data(Name=name, E_Mail=Email, Date_Time=date, People=People, Request=Special)
        db.session.add(entry)
        db.session.commit()
    return render_template('booking.html', params=params)


@app.route("/contact")
def contact():
    return render_template('contact.html', params=params)


@app.route("/Nonveg")
def menu():
    return render_template('Nonveg.html', params=params)


@app.route("/service")
def service():
    return render_template('service.html', params=params)


@app.route("/team")
def team():
    return render_template('team.html', params=params)


@app.route("/testimonial")
def testimonial():
    return render_template('testimonial.html', params=params)


@app.route("/guest")
def guest():
    return render_template('guest.html', params=params)


@app.route("/home")
def home():
    return render_template('Home.html', params=params)


@app.route("/veg")
def veg():
    return render_template('veg.html', params=params)

@app.route("/profile")
def profile():
    global User_Email
    global Create_Pass
    dta=login_user_data.query.filter_by().all()
    return render_template('Profile.html', params=params, dta=dta)

@app.route("/member", methods=['GET', 'POST'])
def member():
    if (request.method == 'POST'):
        '''Add Entry To Database'''
        name = request.form.get('name')
        Email = request.form.get('email')
        date = request.form.get('date')
        select1 = request.form.get('select1')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        select2 = request.form.get('select2')
        phone = request.form.get('phone')
        entry = membership_table(M_Name=name, M_E_Mail=Email, M_Start_Date=date, M_No_Months =select1, M_Address=address, M_CIty=city, M_State=state, M_Pin_Code=pincode, M_Menu_Type=select2, M_Phone=phone)
        db.session.add(entry)
        db.session.commit()
    return render_template('member.html', params=params)


# it automatic Dedect The changement in File
app.run(debug=True)
