class Get_Messages:

    def __init__(self, thing):
        self.thing = thing

    @property
    def Id(self):
        self.thing = self.thing[7:]
        self.thing = self.thing[0:self.thing.index(",")]
        return self.thing

    @property
    def Infos(self):
        return self.thing

    @property
    def Subject(self):
        self.thing = self.thing[self.thing.index('"subject":"'):][11:]
        self.thing = self.thing[0:self.thing.index("\"")]
        return self.thing

    @property
    def Date(self):
        self.thing = self.thing[self.thing.index('"date":'):][8:]
        self.thing = self.thing[0:self.thing.index("\"")]
        return self.thing

    @property
    def From(self):
        self.thing = self.thing[self.thing.index("\"from\":"):]
        self.thing = self.thing[8:]
        self.thing = self.thing[0:self.thing.index("\"")]
        return self.thing

class Fetch_Message():

    def __init__(self,thing):
        self.thing = thing

    @property
    def Body(self):
        self.thing = self.thing[self.thing.index("\"body\":"):][8:]
        self.thing = self.thing[0:self.thing.index("\"}")]
        self.thing = self.thing.replace("\n","")
        self.thing = self.thing.replace("\\","")
        return self.thing

    @property
    def Infos(self):
        return self.thing


    '''This For Amino Verify Code'''
    @property
    def Amino_Verify(self):
        self.thing = self.thing[self.thing.index("href="):]
        self.thing = self.thing.replace("\\","")
        self.thing = self.thing[6:]
        self.thing = self.thing[0:self.thing.index("\"")]
        return self.thing