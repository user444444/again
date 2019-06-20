from src.common.database import Database
import uuid



class User_Summary(object):


    def __init__(self,emp_email,manager_email,allowence,lst_of_hol_dur_req,lst_of_hol_types,lst_of_hol_decisions,lst_hol_rem,_id=None):
        self.emp_email = emp_email
        self.manager_email = manager_email
        self.allowence = allowence
        self.lst_of_hol_dur_req = lst_of_hol_dur_req
        self.lst_of_hol_types = lst_of_hol_types
        self.lst_of_hol_decisions = lst_of_hol_decisions
        self.lst_hol_rem = lst_hol_rem
        self._id = uuid.uuid4().hex if _id == None else _id

    def json(self):
        return {
            "emp_email": self.emp_email,
            "manager_email": self.manager_email,
            "allowence": self.allowence,
            "lst_of_hol_dur_req": self.lst_of_hol_dur_req,
            "lst_of_hol_types": self.lst_of_hol_types,
            "lst_of_hol_decisions": self.lst_of_hol_decisions,
            "lst_hol_rem": self.lst_hol_rem,
            "_id": self._id
        }


    def save_to_mongo(self):
        return Database.insert(collection="summary",data=self.json())


    @staticmethod
    def update_hol_dur(emp_email,hold_dur):
        sum_cls = User_Summary.fetch_summary_by_emp_email(emp_email)

        lst = sum_cls.lst_of_hol_dur_req
        lst.append(hold_dur)

        #new_lst = sum_cls.lst_of_hol_dur_req.append(hold_dur)
        #print(new_lst)

        Database.update(collection="summary",query={"emp_email": emp_email},
                        update={"$set": {"lst_of_hol_dur_req": lst}})

    @staticmethod
    def update_hol_types(emp_email, hold_types):
        sum_cls = User_Summary.fetch_summary_by_emp_email(emp_email)
        print(sum_cls.lst_of_hol_types)
        lst = sum_cls.lst_of_hol_types
        lst.append(hold_types)

        print(lst)
        #new_lst = sum_cls.lst_of_hol_dur_req.append(hold_types)
        #print(new_lst)

        Database.update(collection="summary", query={"emp_email": emp_email},
                        update={"$set": {"lst_of_hol_types": lst}})

    @staticmethod
    def update_hol_decisions(emp_email, hold_decision):
        sum_cls = User_Summary.fetch_summary_by_emp_email(emp_email)
        lst = sum_cls.lst_of_hol_decisions
        lst.append(hold_decision)
        print("summary here")
        print(sum_cls.lst_of_hol_dur_req)
        print(type(sum_cls.lst_of_hol_dur_req))
        #new_lst = sum_cls.lst_of_hol_dur_req.append(hold_decision)
        #print(new_lst)

        Database.update(collection="summary", query={"emp_email": emp_email},
                        update={"$set": {"lst_of_hol_decisions": lst}})

    @staticmethod
    def update_hol_remaining(emp_email, hold_rem):
        sum_cls = User_Summary.fetch_summary_by_emp_email(emp_email)
        print(sum_cls.emp_email)
        print(sum_cls.lst_hol_rem)
        lst = sum_cls.lst_hol_rem
        lst.append(hold_rem)
        print(lst)
        #out = sum_cls.lst_hol_rem.append("4")
        #print(out)
        #new_lst = sum_cls.lst_of_hol_dur_req.append(hold_rem)
        #print(new_lst)

        Database.update(collection="summary", query={"emp_email": emp_email},
                        update={"$set": {"lst_hol_rem": lst}})






    @classmethod
    def fetch_summary_by_emp_email(cls, emp_email):
        emp = Database.find_one(collection="summary", query={"emp_email": emp_email})
        if emp == None:
            print("Emp is None")
        else:

            # return cls(**emp)
            return cls(emp_email=emp["emp_email"],manager_email=emp["manager_email"],allowence=emp["allowence"],lst_of_hol_dur_req=emp["lst_of_hol_dur_req"],lst_of_hol_types=emp["lst_of_hol_types"],
                       lst_of_hol_decisions=emp["lst_of_hol_decisions"],lst_hol_rem=emp["lst_hol_rem"])


    @classmethod
    def fetch_summary_by_man_email(cls, manager_email):
        emps = Database.find(collection="summary", query={"manager_email": manager_email})
        if emps == None:
            print("Emp is None")
        else:

            # return cls(**emp)
            return [cls(emp_email=emp["emp_email"],manager_email=emp["manager_email"],allowence=emp["allowence"],lst_of_hol_dur_req=emp["lst_of_hol_dur_req"],lst_of_hol_types=emp["lst_of_hol_types"],
                       lst_of_hol_decisions=emp["lst_of_hol_decisions"],lst_hol_rem=emp["lst_hol_rem"]) for emp in emps]



#cls_output = User_Summary.fetch_summary_by_emp_email(emp_email="emp2_sum@innvotek.com")
#User_Summary.update_hol_remaining(emp_email="emp2_sum@innvotek.com",hold_rem=20)

#Database.initiaize()

#sum = User_Summary(emp_email="hello_email@inn.com",manager_email="hi_man_email",allowence=25,lst_of_hol_dur_req=[],lst_of_hol_types=[],lst_of_hol_decisions=[],lst_hol_rem=[])
#sum.save_to_mongo()

#User_Summary.update_hol_types(emp_email="hello_email@inn.com",hold_types="Rej")

#User_Summary.update_hol_dur(emp_email="hello_email@inn.com",hold_dur=10)
#User_Summary.update_hol_decisions(emp_email="hello_email@inn.com",hold_decision="Whatever")



#User_Summary.update_hol_types(emp_email="hello_email@inn.com",hold_types="Auth")

#User_Summary.update_hol_dur(emp_email="hello_email@inn.com",hold_dur=9)
#User_Summary.update_hol_decisions(emp_email="hello_email@inn.com",hold_decision="Whatever 22")