class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        

class GameField():
    def __init__(self, lenght, height, user_one_point, user_two_point):
        self.lenght = lenght
        self.height = height
        self.user_one_point = user_one_point
        self.user_two_point = user_two_point
        self.crossed_points = list()

    
    def to_graph_field(self):
        return
        """
         ______________________________
        |     |     |     |     |=^.^=|
       5|_____|_____|_____|_____|__()/|
        |     |     |     |     |     |
       4|_____|_____|_____|_____|_____|
        |     |     |     |     |     |
       3|_____|_____|_____|_____|_____|
        |     |     |     |     |     |
       2|_____|_____|_____|_____|_____|
        |=^.^=|     |     |     |     |
       1|\()__|_____|_____|_____|_____|
        1     2     3     4     5
        
        """