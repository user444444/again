from flask import Flask

from src.models.Employee import Employee
"""
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Helo Word"


app.run()
"""
from src.models.user import User
from flask import Flask,render_template,request,session,jsonify
from src.models.Employee import Employee
from src.models.Make_Req import Request
from src.common.database import Database
from src.libs.mailgun import SendMail
from src.models.utils import Utils
from src.models.Request_Info import Req_Info
from src.models.summary import User_Summary
uri = "mongodb://127.0.0.1:27017"
import collections
import pandas as pd
from collections import OrderedDict
pd.set_option('display.width', 1000)
pd.set_option('colheader_justify', 'center')




import bcrypt
#Database.initiaize()

#emp1 = Employee(name="ivan stani",email="i_stani@yahoo.com",manager="Immad",holidays_rem=22)
#emp2 = Employee(name="dragan stankov",email="d_stankov@yahoo.com",manager="Immad_vtori",holidays_rem=16)

#emp1.save_to_mongo()
#emp2.save_to_mongo()

#emp1 = emp1 = Employee(name="ivan stani",email="i_stani@yahoo.com",manager="Immad",holidays_rem=22)

#emp1.save_to_mongo()

#emp1.change_holiday_rem(email_of_user="i_stani@yahoo.com",holiday_days_new_value=2)

#emp1_1 = Employee.fetch_emp_by_email(email="i_stani@yahoo.com")

#emp1_1.change_holiday_rem(email_of_user="i_stani@yahoo.com",holiday_days_new_value=0)


#emp1_1 = Employee.fetch_emp_by_email(email="i_stani@yahoo.com")

#emp1_1.change_holiday_days(email_of_user="i_stani@yahoo.com",holiday_days_new_value=0)
#Database.initiaize()

app = Flask(__name__)
app.secret_key = "Ivan"

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/login', methods = ['POST'])
def login_template():
    return render_template('login.html')


@app.route('/logout',methods = ['POST'])
def logout():
    email = session['email']
    User.logout(email)
    return render_template('home.html')

"--------------------------------------------------"
@app.route('/codecheck_rend',methods = ['POST'])
def codecheck_rend():
    print("WTF")
    return render_template('codecheck.html')

@app.route('/codecheck',methods = ['POST'])
def pre_auth():
    code_provided = request.form['code']
    code_obj = Utils(code_provided)
    if not Utils.codecheck(str(code_provided)):
        return render_template("wrong_passcode.html")


    elif code_obj.code_exits(code_provided):
        code_obj.save_to_mongo()
        return render_template("register.html")
    else:
        return "Code exists.\n Please try a new one"




"-------------------------------------------------------"

@app.route('/register',methods = ['POST'])
#what the user will be accessing is 127.0.0.1:4995/login
def register_template():
    return render_template('register.html')



@app.before_first_request
def initialize_database():
    Database.initiaize()

@app.route('/auth/login', methods = ['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    email1 = "a_ver@yahoo.com"
    print("Email is :",email)
    print("Email's type is : ",type(email))
    if email1 == email:
        print("Equal")
    else:
        print("Non-equal")

    if User.login_valid(email,password):
        User.login(email)
    else:
        session['email'] = None
        return render_template("invalid_user.html")
    print(email)
    print(type(email))

    #emp1 = Employee.fetch_emp_by_email(email=email)
    #days_rem = emp1.get_holidays()
    #days_rem = str(int(days_rem))
    #print(str(int(days_rem)))
    #return render_template("profile.html",email = session['email'],days_rem_output=days_rem)
    return render_template("profile.html", email=session['email'])


@app.route('/auth/register', methods = ['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    if User.user_exists(email= email):
        retJson = {
            "status":301,
            "msg":"Invalid user name! Choose Another"
        }
        return jsonify(retJson)

    #hashed_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    User.register(email,password)

    return render_template("employee_reg.html",email = session['email'])
("-----------------------------------------------------------------------------------------------")
@app.route('/update/info',methods = ['POST'])
def update_info():
    return render_template("update_info.html")


@app.route('/update/emp',methods = ['POST'])
def update_info_emp():
    email = session['email']

    emp_new_name = request.form['emp_name']
    emp_new_email = request.form['emp_email']
    manager_new_name = request.form['manager_name']
    manager_new_email = request.form['manager_email']
    company_new_possition = request.form['company_possition']
    holidays_new_rem = request.form['holidays_rem']
    act_req = False
    Employee.update_data(employee_email=email,new_name=emp_new_name,new_email=emp_new_email,new_manager=manager_new_name,new_manager_email=manager_new_email,new_company_pos=company_new_possition,
                         new_holiday_rem=holidays_new_rem,new_act_req=act_req)


    return render_template("profile.html", email=session['email'])


("-----------------------------------------------------------------------------------------------")

@app.route('/profile',methods = ['POST'])
def emp_prof():
    emp_name = request.form['emp_name']
    emp_email = request.form['emp_email']
    manager_name = request.form['manager_name']
    manager_email = request.form['manager_email']
    company_possition = request.form['company_possition']
    holidays_rem = request.form['holidays_rem']
    act_req = False
    new_employee  = Employee(name = emp_name,email=emp_email,manager=manager_name,manager_email=manager_email,
                             company_possition = company_possition,holidays_rem=holidays_rem,act_req=act_req)

    new_emp_summary = User_Summary(emp_email=emp_email,manager_email=manager_email,allowence=holidays_rem,
                                   lst_of_hol_dur_req=[],lst_of_hol_types=[],lst_of_hol_decisions=[],lst_hol_rem=[])
    new_emp_summary.save_to_mongo()
    new_employee.save_to_mongo()
    return render_template("profile.html",email = session['email'])


#@app.route('/enp_info/<string:user_email>')

@app.route('/emp_info', methods=['POST'])
def emp_info(user_email=None):
    user_email_param = session['email']
    print(user_email_param)
    print(type(user_email_param))
    emp = Employee.fetch_emp_by_email(user_email_param)
    name = emp.name
    manager = emp.manager
    print("Manager is : ",manager)
    holidays = int(emp.get_holidays())
    company_pos = emp.company_possition
    holiday_req = emp.act_req
    if company_pos != "Manager":
        return render_template("Employee's info.html",name = name, manager = manager, holidays = holidays,holiday_requested =holiday_req)

    else:
        items=  []
        item = {}
        lst_emps = Employee.fetch_all_emp(manager_name=name)
        print(lst_emps)
        for emp in lst_emps:
            print("------------------------------")
            print(emp.name)
            #item[emp.name] = [emp.holidays_rem,emp.act_req]
            item = collections.OrderedDict(name = emp.name,holidays = emp.holidays_rem, holiday_requested = emp.act_req,
                                           User_Email = emp.email)
            items.append(item)


        print(items)
        return render_template("employees_info_for_managers.html",items=items)











@app.route('/manager_table',methods = ['POST','GET'])
def render_table():
    man_email = session['email']
    print("Supposed Man email: ",man_email)

    lst_of_summaries = User_Summary.fetch_summary_by_man_email(manager_email=man_email)

    lst_dur_req_total = []
    lst_of_hol_types_total = []
    lst_of_hol_dec = []
    lst_of_hol_rem = []
    lst_of_names = []
    lst_of_allowences = []
    for summary in lst_of_summaries:
        lst_dur_req_total.append(summary.lst_of_hol_dur_req)
        lst_of_hol_types_total.append(summary.lst_of_hol_types)
        lst_of_hol_dec.append(summary.lst_of_hol_decisions)
        lst_of_hol_rem.append(summary.lst_hol_rem)
        lst_of_names.append(summary.emp_email)
        lst_of_allowences.append(summary.allowence)
    print("Types total: ",lst_of_hol_types_total)

    sick_indexes = []
    other_indexes = []
    unauth_indexes = []
    auth_indexes = []
    subl_auth_ind = []

    sick_leave_days = []
    auth_days = []
    i=0
    """
    for q in lst_of_hol_types_total:
        print("q is ",q)
        while i <len(q):
            if q[i]== "Sick Leave":
                sick_indexes.append(i)
            elif q[i] == "Authorised Leave":
                auth_indexes.append(i)
            elif q[i] == "Other":
                other_indexes.append(i)
            i+=1
        if len(auth_indexes) !=0:
            for au_ind in auth_indexes:

    """
    """
    q = 0
    i = 0

    while q < len(lst_of_hol_types_total):
        sublist = lst_of_hol_types_total[q]
        print("sublist here: ",sublist)
        while i < len(sublist):

            if sublist[i] == "Authorised Leave":
                auth_indexes.append(i)
                subl_auth_ind.append(q)
            i+=1

        q+=1

    """
    auth_out = Utils.extract_auth_from_lst(lst_of_lsts=lst_of_hol_types_total,lsts_of_durs=lst_dur_req_total )
    
    sick_out = Utils.extract_sick_from_lst(lst_of_lsts=lst_of_hol_types_total,lsts_of_durs=lst_dur_req_total )

    unauth_out = Utils.extract_unauth_from_lst(lst_of_lsts=lst_of_hol_types_total,lsts_of_durs=lst_dur_req_total )

    other_out = Utils.extract_other_from_lst(lst_of_lsts=lst_of_hol_types_total, lsts_of_durs=lst_dur_req_total)



    print("auth_indexes: ",auth_indexes)
    print("subl: ",subl_auth_ind)

    print(subl_auth_ind)

    durs_lst = []


    if len(subl_auth_ind) != 0 and len(auth_indexes)!=0:
        for q in subl_auth_ind:
            print("q: ",q)
            temp_lst = []
            for i in auth_indexes:
                print(i)
                sublist = lst_dur_req_total[q]
                print(sublist)
                temp_lst.append(sublist[i])

            durs_lst.append(sum(temp_lst))







    #flat_lst_dur_req_total = [item for sublist in lst_dur_req_total for item in sublist]
    """
    if len(sick_indexes) != 0:
        for i in sick_indexes:
            sick_leave_days.append(flat_lst_dur_req_total[i])

    if len(auth_indexes) != 0:
        for i in auth_indexes:
            auth_days.append(flat_lst_dur_req_total[i])

    """


    sick_days = sum(sick_leave_days)
    print("Sick Days: ",sick_days)
    q = 0
    count = 0
    print(lst_dur_req_total)
    counts = []
    for i in lst_dur_req_total:
        while q<len(i):
            print(q)
            print(type(q))
            if isinstance(i[q],str):
                print("it is a string: ",i[q])
                temp = int(i[q])
                i[q] = temp
            q+=1

        print(i)
        counts.append(sum(i))
    num_of_days_rem = []
    for i in lst_of_hol_rem:
        print("i is: ",i)
        if len(i)!=0:
            num_of_days_rem.append(i[len(i)-1])
        else:
            num_of_days_rem.append(0)
    print(lst_of_hol_types_total)
    print(lst_of_hol_dec)
    print(lst_of_hol_rem)
    print(lst_of_names)
    print(lst_of_allowences)

    data = {"Allowence": lst_of_allowences,
            "Requested Number of Days":lst_dur_req_total,
            "Leave Requests Types": lst_of_hol_types_total,
            "Leave Requests Manager Decisions": lst_of_hol_dec,
            "Number of Days Remaining": lst_of_hol_rem,
            }

    data1 = {"Allowence": lst_of_allowences,
            "Total Number of Days Requested": counts,
            "Number of Days Remaining": num_of_days_rem,
             "Number of Authorised Days": auth_out,
             "Number of Sick Days":sick_out,
             "Other  Holidays Taken": other_out,
             "Number of Unauthorised Days": unauth_out
            }

    df = pd.DataFrame(data, index= lst_of_names)
    df1 = pd.DataFrame(data1,index = lst_of_names,columns=["Allowence","Total Number of Days Requested","Number of Days Remaining","Number of Authorised Days","Number of Sick Days",
                                                           "Other  Holidays Taken","Number of Unauthorised Days"])


    return render_template("manager_table.html", tables=[df.to_html(classes='data'),df1.to_html(classes='data1')],titles=(df.columns.values,df1.columns.values))


"""
    lst_reqs = Request.fetch_reqs_to_man(man_email=man_email)

    #lst_of_reqs = Request.fetch_reqs_to_man(man_email=man_email)
    #lst_of_reqs = Req_Info.fetch_by_man_email(man_email=man_email)
    print(man_email)
    print("I am f here")
    print(lst_reqs)
    items = []
    lst_of_names = []
    lst_of_dates = []
    lst_of_hold_durs = []
    lst_of_holidays_rem = []
    lst_of_types=  []
    count = 0
    for req in lst_reqs:

        st_date = req.start_date
        print(st_date)
        end_date = req.end_date
        print(end_date)
        total_date = str(st_date) + "-" + str(end_date)
        print(total_date)
        print(req.emp_name)
        emp = Employee.fetch_emp_by_email(email = req.emp_email)
        holidays_rem_per_emp = emp.holidays_rem
        print("here mf")
        print(st_date)


        #count +=1

        #item = collections.OrderedDict(name=req.emp_name, holiday_period=total_date, holiday_duration=req.tot_dur,order = count)


        #items.append(item)
        lst_of_types.append(req.req_type)
        lst_of_names.append(req.emp_name)
        lst_of_dates.append(total_date)
        lst_of_hold_durs.append(str(req.tot_dur))
        lst_of_holidays_rem.append(holidays_rem_per_emp)
        
        print(lst_of_dates)

    pd.set_option('display.width', 1000)
    pd.set_option('colheader_justify', 'center')

    data = {"Allowence":25,
            "Period":lst_of_dates,
            "Duration":lst_of_hold_durs,
            "Remaining":lst_of_holidays_rem,
            "Leave Type":lst_of_types}


    df = pd.DataFrame(data,index=lst_of_names)


    return render_template("manager_table.html",tables=[df.to_html(classes='data')], titles=df.columns.values)
    #return render_template("manager_tableV2.html",items = items)

"""















@app.route('/auth_rej',methods = ['POST'])
def auth_rej():
    email = request.form['emp_email']
    print("Here Here")
    print(email)
    #if 'Authorise' in request.form:
    if request.form['action'] == 'Authorise':
        emp = Employee.fetch_emp_by_email(email = email)

        employee_sum_email = emp.email  #email for summary search per employee
        User_Summary.update_hol_decisions(emp_email=employee_sum_email,hold_decision="Auth")




        print(emp.manager_email)
        print(emp.name)
        req = Request.fetch_req(email = email)

        print("Now here")
        print(type(req))
        #Need to put emp.act_req = False
        current_days = int(emp.holidays_rem)
        req_days = int(req.tot_dur)
        print("req_days = :",req_days)
        print("current_days = :", current_days)
        if req_days > current_days:
            print("ERROR: Not Enough Days Remaining")
            return False
        elif req.req_type == "Sick Leave":
            print("Sick LEave")
            ("====================================================================================================")
            emp = Employee.fetch_emp_by_email(email=email)
            req = Request.fetch_req(email=email)
            emp.act_req_set_to_false()

            st_date_mail = req.start_date
            end_date_mail = req.end_date

            print("-------------------------------------------------------")
            txt = "SICK LEAVE REQUEST Approved" + "\n" + "Your sick leave request for the period of : " + st_date_mail + "-" + end_date_mail + "has been approved"
            data = {"from": "Time-Off_Innvotek <do-not-reply@sandbox6449fa2b794d441298aa546cfed6ced9.mailgun.org>",
                    "to": ["i_botev@yahoo.com"],
                    "subject": "Sick Leave",
                    "text": txt}
            SendMail.send_simple_message(data=data)

            print("-------------------------------------------------------")

            req.remove_req(email=email)

            ("-----------------------------------------------------------------------------------------")
            User_Summary.update_hol_types(emp_email=employee_sum_email,hold_types='Sick Leave')
            User_Summary.update_hol_dur(emp_email=employee_sum_email,hold_dur=req_days)
            User_Summary.update_hol_remaining(emp_email=employee_sum_email,hold_rem=current_days)

            ("-----------------------------------------------------------------------------------------")
            # emp.emp_made_req_auth()
            print("Sick Leave Authorised")
            return ("Sick Leave Authorised")
            ("=================================================================================================================")

        elif req.req_type == "Unauthorised Leave":
            print("CAn you see this ")

            emp = Employee.fetch_emp_by_email(email=email)
            req = Request.fetch_req(email=email)
            emp.act_req_set_to_false()

            st_date_mail = req.start_date
            end_date_mail = req.end_date

            print("-------------------------------------------------------")
            txt = "Unauthorised LEAVE REQUEST Approved" + "\n" + "Your Unauthorised leave request for the period of : " + st_date_mail + "-" + end_date_mail + "has been approved"
            data = {"from": "Time-Off_Innvotek <do-not-reply@sandbox6449fa2b794d441298aa546cfed6ced9.mailgun.org>",
                    "to": ["i_botev@yahoo.com"],
                    "subject": "Unauthorised Leave",
                    "text": txt}
            SendMail.send_simple_message(data=data)

            print("-------------------------------------------------------")

            req.remove_req(email=email)

            ("-----------------------------------------------------------------------------------------")
            User_Summary.update_hol_types(emp_email=employee_sum_email, hold_types='Unauthorised Leave')
            User_Summary.update_hol_dur(emp_email=employee_sum_email, hold_dur=req_days)
            User_Summary.update_hol_remaining(emp_email=employee_sum_email, hold_rem=current_days)

            ("-----------------------------------------------------------------------------------------")
            # emp.emp_made_req_auth()
            print("Unauthorised Leave Authorised")
            return ("Unauthorised Leave Authorised")

            ("===============================================================================================================")

        elif req.req_type == "Other":

            emp = Employee.fetch_emp_by_email(email=email)
            req = Request.fetch_req(email=email)
            emp.act_req_set_to_false()

            st_date_mail = req.start_date
            end_date_mail = req.end_date

            print("-------------------------------------------------------")
            txt = "REQUEST Approved" + "\n" + "Your leave request for the period of : " + st_date_mail + "-" + end_date_mail + "has been approved"
            data = {"from": "Time-Off_Innvotek <do-not-reply@sandbox6449fa2b794d441298aa546cfed6ced9.mailgun.org>",
                    "to": ["i_botev@yahoo.com"],
                    "subject": "Request Type Other",
                    "text": txt}
            SendMail.send_simple_message(data=data)

            print("-------------------------------------------------------")

            req.remove_req(email=email)

            ("-----------------------------------------------------------------------------------------")
            User_Summary.update_hol_types(emp_email=employee_sum_email, hold_types='Other')
            User_Summary.update_hol_dur(emp_email=employee_sum_email, hold_dur=req_days)
            User_Summary.update_hol_remaining(emp_email=employee_sum_email, hold_rem=current_days)

            ("-----------------------------------------------------------------------------------------")

            # emp.emp_made_req_auth()
            print("Other Leave Authorised")
            return ("Other Leave Authorised")










            ("====================================================================================================================")
        elif req.req_type == "Authorised Leave":
            print("Authorised LEave Here")

            new_rem_days = current_days - req_days
            print(new_rem_days)

            #self.act_req = False
            #emp.act_req = False
            emp.act_req_set_to_false()

            st_date_mail = req.start_date
            end_date_mail = req.end_date

            print("-------------------------------------------------------")
            txt = "TIME OFF APPROVED" + "\n" + "Your request for the period of : " + st_date_mail + "-" + end_date_mail+ "has been approved"
            data = {"from": "Time-Off_Innvotek <do-not-reply@sandbox6449fa2b794d441298aa546cfed6ced9.mailgun.org>",
                    "to": ["i_botev@yahoo.com"],
                    "subject": "Time Off Approved",
                    "text": txt}
            SendMail.send_simple_message(data=data)

            name = req.emp_name
            st_date = req.start_date
            end_date = req.end_date
            hol_rem = new_rem_days

            print("hol_rem: ",hol_rem)

            req_info_obj = Req_Info(emp_name=name,st_date=st_date,end_date=end_date,hol_dur=req_days,hol_rem=hol_rem,man_email=emp.manager_email)
            #req_info_obj = Req_Info(emp_name=name, st_date=st_date, end_date=end_date, hol_dur=req_days,
            #                       hol_rem=hol_rem, man_e=email)

            req_info_obj.save_to_mongo()

            print("-------------------------------------------------------")

            emp.change_holiday_days(email_of_user=email,holiday_days_new_value=new_rem_days)

            ("-------------------------------------------------------------------------------------------------")
            """
            name = req.emp_name
            st_date = req.start_date
            end_date = req.end_date
            hol_rem = new_rem_days

            req_info_obj = Req_Info(emp_name=name,st_date=st_date,end_date=end_date,hol_dur=req_days,hol_rem = hol_rem,manager_email=email)
            req_info_obj.save_to_mongo()

            """

            print("-------------------------------------------------------------------------------------------------")

            req.remove_req(email = email)

            ("-----------------------------------------------------------------------------------------")
            User_Summary.update_hol_types(emp_email=employee_sum_email, hold_types='Authorised Leave')
            User_Summary.update_hol_dur(emp_email=employee_sum_email, hold_dur=req_days)
            User_Summary.update_hol_remaining(emp_email=employee_sum_email, hold_rem=hol_rem)

            ("-----------------------------------------------------------------------------------------")
            print("Holiday Authorised")
            return ("Holiday Authorised")

    elif request.form['action'] == "Reject":
    #elif 'Reject' in request.form:
        emp = Employee.fetch_emp_by_email(email=email)

        hol_rem = int(emp.holidays_rem)
        employee_sum_email = emp.email  # email for summary search per employee
        User_Summary.update_hol_decisions(emp_email=employee_sum_email, hold_decision="Rej")



        req = Request.fetch_req(email=email)
        emp.act_req_set_to_false()

        st_date_mail = req.start_date
        end_date_mail = req.end_date
        req_days = int(req.tot_dur)
        print("-------------------------------------------------------")
        txt = "TIME OFF REQUEST Rejected" + "\n" + "Your request for the period of : " + st_date_mail + "-" + end_date_mail + "has been rejected"
        data = {"from": "Time-Off_Innvotek <do-not-reply@sandbox6449fa2b794d441298aa546cfed6ced9.mailgun.org>",
            "to": ["i_botev@yahoo.com"],
            "subject": "Time Off Approved",
            "text": txt}
        SendMail.send_simple_message(data=data)

        print("-------------------------------------------------------")
        ("-----------------------------------------------------------------------------------")
        User_Summary.update_hol_types(emp_email=employee_sum_email, hold_types='NaN')
        User_Summary.update_hol_dur(emp_email=employee_sum_email, hold_dur=req_days)
        User_Summary.update_hol_remaining(emp_email=employee_sum_email, hold_rem=hol_rem)

        ("-----------------------------------------------------------------------------------")
        req.remove_req(email=email)
        #emp.emp_made_req_auth()
        print("Hiliday rejected")
        return ("Holiday Rejected")
    else:
        print("Something messed up")
        return ("shit")




"""
self.emp_manager = emp_manager
        self.emp_manager_email = emp_manager_email
        self.tot_dur = tot_dur
        self.start_date = start_date
        self.end_date = end_date

"""

@app.route('/req', methods=['POST'])
def req():
    return render_template('make_req.html')



@app.route('/make_req',methods = ['GET','POST'])
def make_req():
    emp_name = request.form['emp_name']
    emp_email = request.form['emp_email']
    manager_name = request.form['manager_name']
    manager_email = request.form['manager_email']
    total_dur = request.form['total_dur']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    req_type = request.form.get('req_type')

    if not Utils.ext_days(start_date=start_date,end_date=end_date,days_prov=total_dur):
        return render_template(("wrong_dates.html"))


    req = Request(emp_name=emp_name,emp_email= emp_email,emp_manager=manager_name,emp_manager_email=manager_email,
                  tot_dur=total_dur,start_date=start_date,end_date=end_date,req_type = req_type)

    req.save_to_mongo_again()
    req.save_to_mongo()
    req.make_req()

    print("-------------------------------------------------------")
    txt = "NEW TIME OFF REQUEST MADE" + "\n" + "Request made from: " + emp_name + " " + "with email: " + emp_email + "\nDuration of: " + str(total_dur) + "\nDates: " + start_date + "-" + end_date
    data = {"from": "Time-Off_Innvotek <do-not-reply@sandbox6449fa2b794d441298aa546cfed6ced9.mailgun.org>",
                  "to": ["i_botev@yahoo.com"],
                  "subject": "TimeOffReq",
                  "text": txt}
    SendMail.send_simple_message(data=data)

    print("-------------------------------------------------------")

    return 'OK'

    """"
    if req.make_req():
        return render_template("req_sucess.html")
    
    else:
        return render_template("req_fail.html")
        
    """

@app.route('/man_info',methods = ['POST'])
def man_info():
    email = session['email']
    emp = Employee.fetch_emp_by_email(email=email)

    name = emp.name
    manager = emp.manager
    holidays = emp.holidays_rem
    req_hol = emp.act_req

    return render_template("manager_info.html",name = name, manager = manager,
                           holidays = holidays,holiday_requested = req_hol)





if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
    #app.run(port=4995,debug=True)






#email = "a_var@yahoo.com"
#emp = Employee.fetch_emp_by_email(email=email)
#print(type(emp.email))
#print(emp.get_holidays())