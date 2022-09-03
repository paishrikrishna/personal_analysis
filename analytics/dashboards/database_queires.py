import firebase_admin
from firebase_admin import credentials, firestore
import random


class firebase_actions:
    def __init__(self,path_to_certificate):
        self.cred = credentials.Certificate(path_to_certificate)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def initialize_collection_object(self,collection_name):
        self.collection_name = collection_name
        self.collection = self.db.collection(self.collection_name)
        return self.collection
        
    def insert_credit_card_records(self,row_number,data):
        self.initialize_collection_object('credit_card').document("credit_card_transaction_log"+row_number).set(data)
        print("Inserted")
        
    def existing_data(self,collection_name):
        return self.initialize_collection_object(collection_name).stream()
    
    def day_wise_transactions(self):
        self.data_list = []
        for self.record in self.initialize_collection_object('credit_card').stream():
            self.data = {}
            self.details = self.record.to_dict()
            self.data["date"] = self.details["date"]
            self.data["amount"] = float(self.details["amount"])
            self.data_list.append(self.data)
                
        return self.data_list
    
    def receiver_wise_transactions(self):
        self.data = {}
        for self.record in self.initialize_collection_object('credit_card').stream():
            self.details = self.record.to_dict()
            try:
                self.data[self.details["receiver"]] += float(self.details["amount"])
            except:
                self.data[self.details["receiver"]] = float(self.details["amount"])
                
        return self.data
        
