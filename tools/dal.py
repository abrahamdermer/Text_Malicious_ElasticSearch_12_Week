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
                'weapons': {'type': 'text'},
                'emotion': {'type': 'keyword'},
            }
        }    
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
            document['Antisemitic'] = bool(document['Antisemitic'])
            document['weapons'] =''
            document['emotion'] = ''
            document['CreateDate'] = self.convert(document['CreateDate'][:18])
            self.es.index(index=self.index_name, id=i, body=document)
            