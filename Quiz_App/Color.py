

class Color():
    def __init__(self, line, delimiter):
        self.c1 = ""
        self.c2 = ""
        self.c3 = ""
        self.c4 = ""
        self.c5 = ""
        self.name = ""
        self.deserialize(line, delimiter)
        
    def deserialize(self, line, delimiter):
        colors = line.split("*")
        self.name = colors[0]
        self.c1 = colors[1]
        self.c2 = colors[2]
        self.c3 = colors[3]
        self.c4 = colors[4]
        self.c5 = colors[5]