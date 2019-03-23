from elasticsearch import Elasticsearch
from flask import Flask,request
from flask import jsonify


es = Elasticsearch("http://localhost:9200")
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "LLR Open Soft 2019"

@app.route('/query1',methods=['GET','POST'])
def query1():
   
   query = request.get_json()
   # print(query)
   
   keywordsList=query[0]['query']
   fromDate=query[0]['time']['from']
   toDate=query[0]['time']['to']
   cat=query[0]['cat']
   act=query[0]['act']
   judge=query[0]['judge']
   
   if judge=="":
      judge="*"
   if act=="":
      act="*"
   if cat=="":
      cat="*"
   
   searchString=""
   for q in keywordsList:
      searchString+=q+','

   searchString=searchString[:-1]
   print(judge)
   res = es.search(index="cases",
   body={"query":{
   
    "bool": {
        "must": { "match":{"legal-key":searchString}},
        "filter": [
           { "wildcard":{"judge":{"value":judge}}},
           { "wildcard":{"act-used":{"value":act}}},
           { "wildcard":{"case-cat":{"value":cat}}},
        ]
    }

   }})
   # print("result is")
   # for cases in res['hits']['hits']:
   #    print(cases['_source']['judge'])
   # print(res)
   return jsonify(res['hits']['hits'])

@app.route('/query2',methods=['GET','POST'])
def query2():
   
   query = request.get_json()
   
   actquery=query[0]['query']
   fromDate=query[0]['time']['from']
   toDate=query[0]['time']['to']
   cat=query[0]['cat']
   judge=query[0]['judge']
   
   if judge=="":
      judge="*"
   if act=="":
      act="*"
   if cat=="":
      cat="*"
   
   print(actquery[0])
   res = es.search(index="acts",
   body={"query":{
    "bool": {
        "must": { "match":{"Act_Name":actquery[0]}},
    }
   }})

   file_list=[]
   for acts in res['hits']['hits']:
      temp=list(acts['_source']['File_Name'].replace(' ','').split(','))
      for i in temp:
         if i!='\n':
            file_list.append(i)

   res = []
   for i in file_list:
      if i[-1]=='\n':
         temp=i[:-5]
      else:
         temp=i[:-4]

      res.append(es.search(index="cases",
      body={"query":{
      "bool": {
         "must": { "match":{"filename":temp}},
         "filter": [
           { "wildcard":{"judge":{"value":judge}}},
           { "wildcard":{"act-used":{"value":act}}},
           { "wildcard":{"case-cat":{"value":cat}}},
        ]
      }
      }}))

   resultReturn = []
   for result in res:
      resultReturn.append(result['hits']['hits'][0])

   print(resultReturn)
   return jsonify(resultReturn)

@app.route('/query3',methods=['GET','POST'])
def query3():
   
   query = request.get_json()
   # print(query)
   
   searchString=query[0]['query']
   fromDate=query[0]['time']['from']
   toDate=query[0]['time']['to']
   cat=query[0]['cat']
   act=query[0]['act']
   judge=query[0]['judge']
   
   if judge=="":
      judge="*"
   if act=="":
      act="*"
   if cat=="":
      cat="*"
   # print(type(keywordsList))
   # print(toDate)
   #  = 

   # searchString=searchString[:-1]
   res = es.search(index="cases",
   body={"query":{
   
    "bool": {
        "must": { "match":{"title":searchString}},
        "filter": [
           { "wildcard":{"judge":{"value":judge}}},
           { "wildcard":{"act-used":{"value":act}}},
           { "wildcard":{"case-cat":{"value":cat}}},
        ]
    }

   }})
   print("result is")
   for cases in res['hits']['hits']:
      print(cases['_source']['judge'])

   return "Yo"

@app.route('/query4',methods=['GET','POST'])
def query4():
   
   query = request.get_json()
   # print(query)
   
   searchString=query[0]['query']
   fromDate=query[0]['time']['from']
   toDate=query[0]['time']['to']
   cat=query[0]['cat']
   act=query[0]['act']
   judge=query[0]['judge']
   

   res = es.search(index="cases",
   body={"query":{
   
    "bool": {
        "must": { "match":{"title":searchString}},
        "filter": [
           { "match":{"judge":judge}},
           { "match":{"act-used":act}},
           { "match":{"case-cat":cat}},
           { "range": {"date" : {"gte":"1 January 1900","lte":"1 January 2500", "format":"d M y || d M y"}}}
        ]
    }

   }})
   print("result is")
   for cases in res['hits']['hits']:
      print(cases['_source']['judge'])

   return "Yo"

if __name__ == '__main__':
   app.run(debug=True)
