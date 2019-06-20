from src.common.database import Database
import uuid


class Req_Info(object):
    def __init__(self,emp_name,st_date,end_date,hol_dur,hol_rem,man_email,_id=None):
        self.emp_name = emp_name
        self.st_date = st_date
        self.end_date = end_date
        self.hol_dur = hol_dur
        self.hol_rem = hol_rem
        self.man_email = man_email
        self._id = uuid.uuid4().hex if _id == None else _id



    def json(self):
        return {
            "emp_name":self.emp_name,
            "st_date":self.st_date,
            "end_date":self.end_date,
            "hol_dur":self.hol_dur,
            "hol_rem":self.hol_rem,
            "man_email":self.man_email,
            "_id": self._id
        }

    def save_to_mongo(self):
        return Database.insert(collection="req_info2",data=self.json())


    """
    @classmethod
    def fetch_by_man_email(cls,st_date):
        lst_of_reqs = Database.find(collection="req_info", query={"st_date": st_date})
        print(lst_of_reqs)
        #return [cls(**req) for req in lst_of_reqs]


        #[cls(name=emp_to_manager["name"],email=emp_to_manager["email"],manager=emp_to_manager["manager"],manager_email=emp_to_manager['manager_email'],
                     #  company_possition=emp_to_manager['company_possition'],
                  #    holidays_rem=emp_to_manager["holidays_rem"],act_req=emp_to_manager['act_req'],_id=emp_to_manager["_id"]) for emp_to_manager in emps_to_manager]
        return [cls(emp_name=req["emp_name"],st_date=req["st_date"],end_date=req["end_date"],hol_dur=req["hol_dur"],hol_rem=req["hol_rem"],manager_email=req["manager_email"],_id=req["_id"]) for req in lst_of_reqs]
"""
#Req_Info.fetch_by_man_email(st_date ="1/07/2019")


    @classmethod
    def fetch_by_man_email(cls,man_email):
        lst_of_reqs = Database.find(collection="req_info",query={"man_email":man_email})

        print("Here Again")
        print(type(lst_of_reqs))
        #return [cls(**emp_to_manager) for emp_to_manager in emps_to_manager]
        return [cls(emp_name=req["emp_name"],st_date=req["st_date"],end_date=req["end_date"],hol_dur=req['hol_dur'],
                       hol_rem=req["hol_rem"],man_email=req['man_email'],_id=req["_id"]) for req in lst_of_reqs]



#Req_Info.fetch_by_man_email(manager_email = "new_emp_to_man@innvotek.com")


#Req_Info.fetch_by_man_email(man_email = "new_manager@invotek.com")







