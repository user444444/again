

import requests



class SendMail(object):



    @staticmethod
    def send_simple_message(data):
        requests.post(
            "https://api.mailgun.net/v3/sandbox6449fa2b794d441298aa546cfed6ced9.mailgun.org/messages",
            auth=("api", "c9d3ff7735f2d01e3cada3f92cc642c2-87cdd773-1552f5e2"),
            data = data)



"""
            
            data={"from": "Time-Off_Innvotek <do-not-reply@sandbox6449fa2b794d441298aa546cfed6ced9.mailgun.org>",
                  "to": ["i_botev@yahoo.com"],
                  "subject": "TimeOffReq",
                  "text": "Testing some Mailgun awesomeness!"})


"""



