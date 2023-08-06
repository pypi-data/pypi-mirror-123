import os
import csv
import json
from tqdm import tqdm

class read_data():

    def __init__(self,fileName):
        
        self.fileName = fileName
        self.res = []

        if fileName.endswith('.txt'):
            self.res = self.read_txt()
        elif fileName.endswith('.json'):
            self.res = self.read_json()
        elif fileName.endswith('.csv'):
            self.res = self.read_csv() 
        else:
            raise ValueError(
                "The format of the read file can only be JSON, TXT or CSV"
            )          

    def read_txt(self):
        
        res = []
        with open(self.fileName, "r" ,encoding='utf8') as f:
            data = f.readlines()
            for d in tqdm(data):
                res.append(d)

        return res

    def read_json(self):
        
        try:
            with open(self.fileName,'r', encoding='utf8') as f:
                json_data = json.load(f)
        except:
            json_data = []
            with open(self.fileName,encoding='utf-8') as f:
                for line in tqdm(f):
                    json_data.append(json.loads(line))        
        return json_data    

    def read_excel(self):
        # TODO
        pass 

    def read_csv(self):
        res = []
        with open(self.fileName,encoding='utf-8') as f:
            reader = csv.reader(f)
            for l in tqdm(reader):
                res.append(l)
        return res        
    

def read(fileName):
    return read_data(fileName).res

