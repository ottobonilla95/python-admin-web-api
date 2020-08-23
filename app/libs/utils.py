from datetime import datetime


class Utils():
    @classmethod
    def get_current_datetime_in_string(cls):

        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        return dt_string
                 