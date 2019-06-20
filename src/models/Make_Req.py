

from src.common.database import Database
from src.models.Employee import Employee
import uuid
import pymongo



class Request(object):
    def __init__(self,emp_name,emp_email,emp_manager,emp_manager_email,tot_dur,start_date,end_date,req_type,_id=None):
        self.emp_name = emp_name
        self.emp_email = emp_email
        self.emp_manager = emp_manager
        self.emp_manager_email = emp_manager_email
        self.tot_dur = tot_dur
        self.start_date = start_date
        self.end_date = end_date
        self.req_type = req_type
        self._id = uuid.uuid4().hex if _id == None else _id





    def json(self):
        return {
        "emp_name":self.emp_name,
        "emp_email":self.emp_email,
        "emp_manager": self.emp_manager,
        "emp_manager_email": self.emp_manager_email,
        "tot_dur": self.tot_dur,
        "start_date": self.start_date,
        "end_date":self.end_date,
        "req_type":self.req_type
        }


    def save_to_mongo(self):
        return Database.insert(collection="requests",data=self.json())



    def make_req(self):
        emp = Employee.fetch_emp_by_email(self.emp_email)
        days_rem = int(emp.get_holidays())
        if days_rem < int(self.tot_dur):
            return False

        else:
            emp.emp_made_req()
            return True





            #NEED TO COMPLETE THIS PART WITH CHANGING THE req_made from the employee class

            """
            emp.emp_made_req(self.emp_email)_
            return True
            
            
            
            """

            """
            new_days_rem = days_rem - int(self.tot_dur)
            emp_email_to_write = emp.email
            emp.change_holiday_days(email_of_user=emp_email_to_write,holiday_days_new_value=new_days_rem)
            print("I am here: SUCCESS SAVING A CHANGE IN USERS HOLIDAYS")
            return True
            """

    """"
    @classmethod
    def fetch_req(cls,email):
        req = Database.find_one(collection="requests", query={"emp_email": email})
        if req==None:
            print("Emp is None")
        else:
            return cls(**req)
    """

    @classmethod
    def fetch_req(cls, email):

        #req = Database.find(collection="requests", query={"emp_email": email}).limit(1).sort=(['_id',pymongo.ASCENDING])
        #req = Database.find(collection="requests", query={"emp_email": email}).skip(Database.Database["requests"].count()-1)
        #print(req)
        #req = Database.find(collection="requests",query={"emp_email":email}).limit(1).sort({"$natural":-1})
        req = Database.find_one(collection="requests", query={"emp_email": email})
        if req == None:
            print("Emp is None")
        else:



            #name = emp_name["name"], email = emp["email"], manager = emp["manager"], manager_email = emp['manager_email'],
            #company_possition = emp['company_possition'],
            #holidays_rem = emp["holidays_rem"], act_req = emp['act_req'], _id = emp["_id"])
            return cls(**req)


    def remove_req(self,email):
        Database.remove(collection="requests",query={"emp_email":email})


    @classmethod
    def fetch_reqs_to_man(cls,man_email):
        reqs = Database.find(collection="requests_perm", query={"emp_manager_email": man_email})
        lst_of_reqs = [cls(**req) for req in reqs]
        return lst_of_reqs



    def save_to_mongo_again(self):
        return Database.insert(collection="requests_perm",data=self.json())

