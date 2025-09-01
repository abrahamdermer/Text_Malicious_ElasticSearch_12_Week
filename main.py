from tools.file_reader import Reader

from tools.dal import DAL

from tools.emotion_classifier import Classification

dal = DAL()
dal.build_index()
dal.send_twwit_list(Reader.read_csv_by_address('./data/tweets_injected.csv')[:5])


data = dal.get_all_documents()

print(data)

new = Classification.add_val_to_emotion_fild(data)

# print(new)

dal.update_fild('emotion',new)


data = dal.get_all_documents()
print(data)

# print(Reader.read_csv_by_address('./data/tweets_injected.csv')[0])
# print(dal.es.indices.get_mapping(index=dal.index_name))