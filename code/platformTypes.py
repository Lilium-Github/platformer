from platforms import Platform

class BasePlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.color = (114, 230, 101)

class Cloud(Platform):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.color = (255, 201, 241)

class Ice(Platform):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.color = (153, 208, 232)