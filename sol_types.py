class Scraped_Result: # parent class for standard methods
    def __init__(self, keys, values):   # constructor
        dict = {}
        self.id = values[0]     # id used in site backend
        for i in range(len(keys)):
            dict[keys[i]] = values[i + 1]   # create dict using keys, values except id
        self.data = dict

    def __str__(self):  # tostring
        s = ''
        for k in self.data.keys():
            s += str(k) + ' = ' + str(self.data.get(k)) + '\n' 
        return s
    
    def get_data(self, key): # get value pair of given key name
        if key not in self.data.keys():
            raise Exception("invalid data type, must be in " + str(self.data.keys()))
        return self.data[key]
    
    def get_keys(self):  # get all data types 
        return self.data.keys()
    
    def get_id(self):   # get data id
        return self.id

class Champion(Scraped_Result):     # Champion data type
    def get_kda(self):
        return self.data['KDA']

class Team(Scraped_Result): # Team data type
    def get_kda(self):
        return self.data['KDA']

class Player(Scraped_Result):
    def get_kda(self):
        return self.data['KDA']
    
