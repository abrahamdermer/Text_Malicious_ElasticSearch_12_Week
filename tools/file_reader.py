import csv




class Reader:


    @staticmethod
    def read_csv_by_address(address):
        with open(address, 'r',encoding='utf8') as f:
            list_of_dict  = list(csv.DictReader(f))
        return list_of_dict
    
