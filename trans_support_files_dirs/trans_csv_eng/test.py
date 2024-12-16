def parse_line(
        line: str,
) -> list:
    import re
    wordlist = re.findall(r"([а-яА-Я\s]+)", line)
    wordlist = sorted(wordlist, key=len, reverse=True)
    return wordlist

print(parse_line('переходная характеристика системы '))


    # def pkl_create(self) -> None:
    #     """Creating decoded_dictionary.pkl."""
    #     with open(self.path_for_main_dict, 'xb') as pkl:
    #         csv_data = self.take_csv_data()
    #         pickle.dump(csv_data, pkl)
        
    # def pkl_update(self, update):
    #     with open(self.path_for_main_dict, 'rb') as pkl:
    #         pkl_data = pickle.load(pkl)
    #         pkl_data.update(update)
    #     with open(self.path_for_main_dict, 'wb') as pkl:
    #         pickle.dump(pkl_data, pkl)
    #     with open(self.path_for_main_dict, 'rb') as pkl:
    #         self.core_dict = pickle.load(pkl)
    #     self.temp_dict = dict()