from elasticsearch import Elasticsearch
import datetime





class DAL:

    def __init__(self)->None:
        self.es = Elasticsearch('http://localhost:9200')
        self.index_name = "newsgroups"
    
    def build_index(self)->None:
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name, ignore_unavailable=True)
        mapping = {
            'properties': {
                'text': {'type': 'text'},
                'Antisemitic': {'type': 'boolean'},
                'CreateDate': {'type': 'date'},
                "weapons": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                        },
                'emotion': {'type': 'keyword'},
            }
        }    
        # self.es.indices.create(index=self.index_name,)
        self.es.indices.create(index=self.index_name,mappings=mapping)


    # def manual_mapping(self)->None:
    #     mapping = {
    #         'properties': {
    #             'text': {'type': 'text'},
    #             'Antisemitic': {'type': 'boolean'},
    #             'CreateDate': {'type': 'date'},
    #             'weapons': {'type': 'text'},
    #             'emotion': {'type': 'keyword'},
                
    #         }
    #     }    
    #     self.es.indices.get_mapping(index=self.index_name, body=mapping)

    def convert(self,date_time):
        format = "%Y-%m-%d %H:%M:%S"
        datetime_str = datetime.datetime.strptime(date_time, format)

        return datetime_str



    def send_twwit_list(self,twwits:list[dict])->None:
        for i, document in enumerate(twwits):
            document.pop('TweetID')
            document['Antisemitic'] = bool(int(document['Antisemitic']))
            # document['weapons'] =' '
            document['emotion'] = ''
            document['CreateDate'] = self.convert(document['CreateDate'][:18])
            self.es.index(index=self.index_name, id=i, body=document)
        self.es.indices.refresh(index=self.index_name)


    def get_all_documents(self)->list[dict]:
        query = {
            "size":9999,
            "query": {
                "match_all": {}
            }
        }
        # print(self.es.indices.exists(index=self.index_name))

        res = self.es.search(index=self.index_name, body=query)
        # print(res)
        # print(len(res['hits']['hits']))
        return res['hits']['hits']
            

    def update_fild(self,fild,new_data:dict):
        for id in new_data.keys():
            self.es.update(
                index=self.index_name,
                id=id,
                script={
                    "source": f"ctx._source.{fild} = params.{fild}",
                    "params": {
                       fild : new_data[id]
                    }
                },
            )
        self.es.indices.refresh(index=self.index_name)

    def find_ids_by_weapon(self , weapon):
        query = {
            'size':9999,
            "_source":['id'],
            "query": {
                "match": {
                    'text':weapon
                }
            }
        }
       
        res = self.es.search(index=self.index_name, body=query)
        # print(res)
        ids = []
        for doc in res['hits']['hits']:
            ids.append(doc['_id'])
        return ids
    
    def update_weaopn_by_ids(self,weapon:str,ids:list):
        for id in ids:
            self.es.update(
                index=self.index_name,
                id=id,
                script={
                    "source": """if (ctx._source.weapons == null){ctx._source.weapons = params.weapons;}
                    else:
                      ctx._source.weapons += ' '+ params.weapons""",
                    "params": {
                       'weapons' : weapon
                    }
                },
            )
        self.es.indices.refresh(index=self.index_name)

    def delete_not_intaresting(self):
        print(self.es.count(index=self.index_name))
        query = {
                "query": {
                    'bool':{
                        "must": [
                            {'term':{"Antisemitic": False}},
                            # {'term':{"weapons":''}},
                            {"script": {"script": {"lang": "painless", "source": "doc['weapons'].size() == 0"}}}
                        ],
                        'should':[
                            {"term": {"emotion": "positive"}},
                            {"term": {"emotion": "neutral"}}
                        ],
                        "minimum_should_match": 1,
                        'must_not':[{'exists':{'field':'weapons'}}]
                        }
                }
            }
        self.es.delete_by_query(index=self.index_name, body=query)
        self.es.indices.refresh(index=self.index_name)
        print(self.es.count(index=self.index_name))
