# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


import pymysql


conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='123456',
                       db='rasa',
                       charset = 'utf8'
                       )

  
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
        # curcor = Conn.getConn("")
        # mysql = Database()
        sql = "select usex from tuser where uname = '%s'"%vall
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            resul = cursor.fetchall()
            usex=resul[0][0]
            print("resul")
            print(resul)

            return [SlotSet("db_get_sex",usex)]
            
        except Exception as e:
            print("Exception:")
            print(e)
            conn.rollback
            return [SlotSet("db_get_sex",usex)]
        finally:
            cursor.close()
