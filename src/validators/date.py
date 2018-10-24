from datetime import timedelta

class DateController:
    def __init__(self, date, index_date, timenow):
        self.date = date
        self.index_date = index_date
        self.timenow = timenow

    def compare(self):
        if (self.date in self.index_date):
            return True
        else:
            return False    
         
    def control(self):
        now = self.timenow.strftime("%d-%m-%Y")
        if (self.date == "today"):
            self.date = now
            return self.compare()
        else:
            for day in range(0, self.date):
                past = (self.timenow - timedelta(days=day)).strftime("%d-%m-%Y")
                self.date = past
                if (self.compare()):
                    return True
        return False