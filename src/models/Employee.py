
from src.common.database import Database
import uuid

class Employee(object):

    def __init__(self,name,email,manager,manager_email,company_possition, holidays_rem,act_req, _id=None):
        self.name = name
        self.email = email
        self.manager = manager
        self.manager_email = manager_email
        self.company_possition = company_possition
        self.holidays_rem = holidays_rem
        self.act_req = act_req
        self._id = uuid.uuid4().hex if _id == None else _id


    def json(self):
        return {
            "name":self.name,
            "email":self.email,
            "manager":self.manager,
            "manager_email":self.manager_email,
            "company_possition":self.company_possition,
            "holidays_rem":self.holidays_rem,
            "act_req":self.act_req,
            "_id":self._id
        }


    def save_to_mongo(self):
        return Database.insert(collection="employees",data=self.json())

    @classmethod
    def fetch_emp_by_email(cls,email):
        emp = Database.find_one(collection="employees",query={"email":email})
        if emp==None:
            print("Emp is None")
        else:

        #return cls(**emp)
            return cls(name=emp["name"],email=emp["email"],manager=emp["manager"],manager_email=emp['manager_email'],
                       company_possition=emp['company_possition'],
                       holidays_rem=emp["holidays_rem"],act_req=emp['act_req'],_id=emp["_id"])

    @classmethod
    def fetch_emp_by_name(cls, name):
        emp = Database.find_one(collection="employees", query={"name": name})
        if emp == None:
            print("Emp is None")
        else:

            # return cls(**emp)
            return cls(name=emp["name"], email=emp["email"], manager=emp["manager"], manager_email=emp['manager_email'],
                       company_possition=emp['company_possition'],
                       holidays_rem=emp["holidays_rem"], act_req=emp['act_req'], _id=emp["_id"])



    def change_holiday_days(self,email_of_user,holiday_days_new_value):
        Database.update(collection="employees",query={"email":email_of_user},update={"$set":{"holidays_rem":holiday_days_new_value}})


    def get_holidays(self):
        return self.holidays_rem


    @classmethod
    def fetch_all_emp(cls,manager_name):
        emps_to_manager = Database.find(collection="employees",query={"manager":manager_name})

        print("Here Again")
        print(type(emps_to_manager))
        #return [cls(**emp_to_manager) for emp_to_manager in emps_to_manager]
        return [cls(name=emp_to_manager["name"],email=emp_to_manager["email"],manager=emp_to_manager["manager"],manager_email=emp_to_manager['manager_email'],
                       company_possition=emp_to_manager['company_possition'],
                       holidays_rem=emp_to_manager["holidays_rem"],act_req=emp_to_manager['act_req'],_id=emp_to_manager["_id"]) for emp_to_manager in emps_to_manager]



    def emp_made_req(self):
        self.act_req = True
        Database.update(collection="employees", query={"email": self.email}, update={"$set": {"act_req": self.act_req}})




    def act_req_set_to_false(self):
        self.act_req = False
        Database.update(collection="employees",query={"email":self.email},update={"$set":{"act_req":self.act_req}})

#Employee.fetch_emp_by_email(email="new_emp_to_man@innvotek.com")

    @staticmethod
    def update_data(employee_email,new_name,new_email,new_manager,new_manager_email,new_company_pos,new_holiday_rem,new_act_req):
        #emp = Database.find_one(collection="employees",query={"email":employee_email})

        Database.update(collection="employees",query={"email":employee_email},update={"$set":{"name":new_name,"email":new_email,
                                                                                              "manager":new_manager,"manager_email":new_manager_email,
                                                                                              "company_possition":new_company_pos,"holidays_rem":new_holiday_rem,"act_req":new_act_req}})






