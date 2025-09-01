from tools.file_reader import Reader
from tools.dal import DAL



class Find_weapons:

    def __init__(self):
        self.weapons = Reader.read_by_address('./data/weapon_list.txt')

    def find_and_update(self,dal:DAL):

        for w in self.weapons:
            print(w)
            ids = dal.find_ids_by_weapon(w)
            print(ids)
            dal.update_weaopn_by_ids(w,ids)
