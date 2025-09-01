from tools.file_reader import Reader

from tools.dal import DAL

dal = DAL()
dal.build_index()
dal.send_twwit_list(Reader.read_csv_by_address('./data/tweets_injected.csv')[:5])

# print(Reader.read_csv_by_address('./data/tweets_injected.csv')[0])
print(dal.es.indices.get_mapping(index=dal.index_name))