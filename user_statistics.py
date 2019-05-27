from datetime import datetime
class UserStatistics:

    def __init__(self, user_name, registration_date, status):
        self.user_name = user_name
        self.registration_date = registration_date
        self.status = status

    
    def to_dict(self):
        return {
            "user_name" : self.user_name,
            "registration_date" : datetime.strftime(self.registration_date, '%d/%m/%Y %H/%M/%S'),
            "status" : self.status
            }
