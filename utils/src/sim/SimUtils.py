import datetime
import utils.consts as consts
from sim.TimeSlice import TimeSlice

class SimUtils():
    def __init__(self):
        pass

    @staticmethod
    def isTradingDay(timeSlice : TimeSlice):
        """
        SimUtils.isTradingDay(date) should return True or False
        """
        tradingDayInts = [0,1,2,3,4]
        return (not SimUtils.isTradingDayHoliday(timeSlice.currentTime) and (timeSlice.currentTime.weekday() in tradingDayInts))

    @staticmethod
    def isTradingDayHoliday(dateObj : datetime.datetime):
        if(dateObj in consts.HOLIDAYS):
            return True
        else:
            return False
        