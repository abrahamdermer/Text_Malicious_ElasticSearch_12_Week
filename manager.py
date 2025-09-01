from tools.file_reader import Reader

from tools.dal import DAL

from tools.emotion_classifier import Classification

from tools.find_weapons import Find_weapons


class Manager:

    def __init__(self):
        

        dal = DAL()
        dal.build_index()
        dal.send_twwit_list(Reader.read_csv_by_address('./data/tweets_injected.csv')[:180])


        # data = dal.get_all_documents()

        # # print(data)

        # new = Classification.add_val_to_emotion_fild(data)

        # # print(new)

        # dal.update_fild('emotion',new)



        # f  = Find_weapons()
        # f.find_and_update(dal)

        # data = dal.get_all_documents()

        # # print(data)

        dal.delete_not_intaresting()


        # # data = dal.find_ids_by_weapon('Gun')
        # # print(data)
        # # print(Reader.read_csv_by_address('./data/tweets_injected.csv')[0])
        # # print(dal.es.indices.get_mapping(index=dal.index_name))
        # q = {"query": {"term": {"weapons": ""}}}
        # print(dal.es.search(index=dal.index_name, query=q["query"]))  