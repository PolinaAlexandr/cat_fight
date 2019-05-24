
class UserStatistics:

    def __init__(self, user_name, registration_date):
        self.user_name = user_name
        self.registration_date = registration_date

    
    def to_dict(self):
        return {
            "user_name" : self.user_name,
            "registration_date" : self.registration_date
            }
