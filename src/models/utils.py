from passlib.hash import pbkdf2_sha512


import string
from src.common.database import Database
#import random
from datetime import datetime

class Utils(object):
    def __init__(self,corr_auth_code):
        self.corr_auth_code  = corr_auth_code



    @staticmethod
    def hash_password(password:str)->str:
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password:str,hashed_password:str)->bool:
        return pbkdf2_sha512.verify(password,hashed_password)


    @staticmethod
    def codecheck(str1):
        alphabet_upper = string.ascii_uppercase
        alphabet_lower = string.ascii_lowercase

        digits = string.digits

        dictt = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8',
                 'i': '9', 'j': '10', 'k': '11', 'l': '12', 'm': '13', 'n': '14', 'o': '15', 'p': '16', 'q': '17',
                 'r': '18', 's': '19', 't': '20', 'u': '21', 'v': '22', 'w': '23', 'x': '24', 'y': '25', 'z': '26'
                 }

        dictt_rev = {v: k for k, v in dictt.items()}

        if len(str1) > 12:
            return False

        if str1[0] not in alphabet_upper:
            print("Pos0")
            return False

        if str1[1] not in digits:
            print("Pos1")
            return False

        if str1[2] not in dictt_rev.values():
            print("Pos2")
            return False

        if str1[3] not in alphabet_lower:
            print("Pos3")
            return False

        if str(str1[4]) not in digits:
            print("Pos4")
            return False

        if int(str1[4]) >= int(str1[1]):
            if int(str1[5]) != int(str1[4]) - int(str1[1]):
                print("Pos5-1")
                return False
        """   
            elif int(str1[5]) != int(str1[1]) - int(str1[4]):
                print(str1[5])
                print(str1[1])
                print(str1[4])
                print("Pos5-2")
                return False
        """
        third_digit = int(str1[5]) + 1

        if str1[6] != dictt_rev[str(third_digit)]:
            print("Pos6")
            return False

        if str1[7] != dictt[str1[6]]:
            print("Pos7")
            return False

        if str1[8] and str1[9] in digits:

            last_but_one_char = int(str(str1[8]) + str(str1[9]))
            print("here")
            print(last_but_one_char)
            if last_but_one_char != int(str1[7]) + int(str1[1]):
                print(str1[9])
                print(str1[8])
                print(str1[7])
                print(str1[1])
                print("Pos8-1")
                return False

            if str1[10] not in alphabet_upper:
                print("Pos9")
                return False

            return True
        else:
            if str1[8] != str(int(str1[7]) + int(str1[1])):
                # print(int(str1[7]) + int(str1[1]))
                # print(str1[9])
                print(str1[8])
                print(str1[7])
                print(str1[1])
                print("Pos8-2")
                return False

        if str1[9] not in alphabet_upper:
            print("Pos9")
            return False

        return True

    def json(self):
        return {
            "code":self.corr_auth_code
        }

    def save_to_mongo(self):
        return Database.insert(collection="auth_codes",data=self.json())

    @staticmethod
    def code_exits(code):
        return Database.find(collection="auth_codes", query={"code": code}).count() == 0



    @staticmethod
    def extract_auth_from_lst(lst_of_lsts, lsts_of_durs):
        q = 0
        i = 0
        out = []
        temp = 0
        while q < len(lst_of_lsts):
            sublist = lst_of_lsts[q]
            print("sublist here: ", sublist)
            while i < len(sublist):

                if sublist[i] == "Authorised Leave":
                    dur_sublist = lsts_of_durs[q]
                    temp += int(dur_sublist[i])

                    # auth_indexes.append(i)
                    # subl_auth_ind.append(q)
                i += 1
            out.append(temp)
            temp = 0
            q += 1
            i = 0

        return out

    @staticmethod
    def extract_sick_from_lst(lst_of_lsts, lsts_of_durs):
        q = 0
        i = 0
        out = []
        temp = 0
        while q < len(lst_of_lsts):
            sublist = lst_of_lsts[q]
            print("sublist here: ", sublist)
            while i < len(sublist):

                if sublist[i] == "Sick Leave":
                    dur_sublist = lsts_of_durs[q]
                    temp += int(dur_sublist[i])

                    # auth_indexes.append(i)
                    # subl_auth_ind.append(q)
                i += 1
            out.append(temp)
            temp = 0
            q += 1
            i = 0

        return out

    @staticmethod
    def extract_unauth_from_lst(lst_of_lsts, lsts_of_durs):
        q = 0
        i = 0
        out = []
        temp = 0
        while q < len(lst_of_lsts):
            sublist = lst_of_lsts[q]
            print("sublist here: ", sublist)
            while i < len(sublist):

                if sublist[i] == "Unauthorised Leave":
                    print("Unauthorised Leave Found")
                    dur_sublist = lsts_of_durs[q]
                    temp += int(dur_sublist[i])

                    # auth_indexes.append(i)
                    # subl_auth_ind.append(q)
                i += 1
            out.append(temp)
            temp = 0
            q += 1
            i = 0

        return out

    @staticmethod
    def extract_other_from_lst(lst_of_lsts, lsts_of_durs):
        q = 0
        i = 0
        out = []
        temp = 0
        while q < len(lst_of_lsts):
            sublist = lst_of_lsts[q]
            print("sublist here: ", sublist)
            while i < len(sublist):

                if sublist[i] == "Other":
                    dur_sublist = lsts_of_durs[q]
                    temp += int(dur_sublist[i])

                    # auth_indexes.append(i)
                    # subl_auth_ind.append(q)
                i += 1
            out.append(temp)
            temp = 0
            q += 1
            i = 0

        return out

    @staticmethod
    def ext_days(start_date, end_date, days_prov):
        date_format = "%d/%m/%Y"
        a = datetime.strptime(start_date, date_format)
        b = datetime.strptime(end_date, date_format)
        delta = b - a
        print("delta_days = ",delta.days)
        return int(delta.days + 1) == int(days_prov)  # that's it











