# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

import pymssql   #sqlserver

import pymysql   #mysql


conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='123456',
                       db='rasa',
                       charset = 'utf8'
                       )

  
sqlserver = pymssql.connect('localhost', 
                       'sa', 
                       '123456', 
                       'rasa', 
                       charset="CP936")
if sqlserver:
    print("已连接数据库")

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



# class ActionGetName(Action):

#     def name(self):

#         return 'action_name'

#     def run(self, dispatcher, tracker, domain):
        
#         return [SlotSet("name","shy")]


class ActionGetSexByName(Action):

    def name(self):

        return 'action_getSexByName'

    def run(self, dispatcher, tracker, domain):
        usex = "男"
        vall = tracker.get_slot("user_input_name")
        print("slot:")
        print(vall)

        sql = "select usex from tuser where uname = %s"


        cursor = conn.cursor()

        try:
            cursor.execute(sql,vall)
            resul = cursor.fetchall()
            usex=resul[0][0]
            print("resul")
            print(resul)

        except Exception as e:
            print("Exception:")
            print(e)
            conn.rollback
            return [SlotSet("db_get_sex",usex)]
        finally:
            cursor.close()

        return [SlotSet("db_get_sex",usex)]

class ActionGetUserByName(Action):
    def name(self):
        return 'action_getUserByName'
    
    def run(self, dispatcher, tracker, domain):
        uname = ""
        uname = tracker.get_slot("user_input_name")
        print("slot:")
        print(uname)

        cursor = sqlserver.cursor()

        sql = "select uname,usex,uidcard,uaddress from t_test where uname = %s"

        try:
            cursor.execute(sql,uname)
            res = cursor.fetchone()
        except Exception as e:
            print(e) 
            cursor.close()
            conn.rollback
            return [SlotSet('db_usex',None)]
        
        while res:
            print(res[0], res[1], res[2], res[3])
            res = cursor.fetchone()

        cursor.close()
        return [SlotSet('db_uname',res[0]),
                SlotSet('db_usex',res[1]),
                SlotSet('db_uidcard',res[2]),
                SlotSet('db_uaddress',res[3])]





