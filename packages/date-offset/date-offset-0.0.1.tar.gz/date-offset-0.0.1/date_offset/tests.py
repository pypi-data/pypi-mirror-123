import unittest
from datetime import date, datetime, timedelta

from .date_offset import DateOffset


class DateOffsetTests(unittest.TestCase):
    def setUp(self):
        self.d = DateOffset()
        self.today = date.today()
        self.fixed_date = datetime(2014, 9, 11, 9, 0, 0)

    def test_today(self):
        result = self.d.get_offset("0")
        expected_result = self.today

        self.assertEqual(expected_result, result)

    def test_today_blank(self):
        result = self.d.get_offset("")
        expected_result = self.today

        self.assertEqual(expected_result, result)

    def test_tomorrow(self):
        result = self.d.get_offset("1d")
        expected_result = self.today + timedelta(days=1)

        self.assertEqual(expected_result, result)

    def test_yesterday(self):
        result = self.d.get_offset("-1d")
        expected_result = self.today - timedelta(days=1)

        self.assertEqual(expected_result, result)

    def test_next_week(self):
        result = self.d.get_offset("1w", self.fixed_date)
        expected_result = date(2014, 9, 18)
        self.assertEqual(expected_result, result)

    def test_month_and_fixed(self):
        result = self.d.get_offset("1m", self.fixed_date)
        expected_result = date(2014, 10, 11)

        self.assertEqual(expected_result, result)

    def test_one_month_one_day(self):
        result = self.d.get_offset("1m1d", self.fixed_date)
        expected_result = date(2014, 10, 12)

        self.assertEqual(expected_result, result)

    def test_last_monday(self):
        result = self.d.get_offset("#", self.fixed_date)
        expected_result = date(2014, 9, 8)
        self.assertEqual(expected_result, result)

    def test_time(self):
        result = self.d.get_offset("9:30t", self.fixed_date)
        expected_result = datetime(2014, 9, 11, 9, 30)
        self.assertEqual(expected_result, result)

    def test_time2(self):
        result = self.d.get_offset("-1w 9:30t", self.fixed_date)
        expected_result = datetime(2014, 9, 4, 9, 30)
        self.assertEqual(expected_result, result)

    def test_date_fixed(self):
        fixed_date = date(2019, 4, 30)
        result = self.d.get_offset("#", fixed_date)
        expected_result = date(2019, 4, 29)
        self.assertEqual(expected_result, result)

    def test_date_fixed_monday(self):
        fixed_date = date(2019, 4, 29)
        result = self.d.get_offset("#", fixed_date)
        expected_result = date(2019, 4, 29)
        self.assertEqual(expected_result, result)

    def test_date_fixed_sunday(self):
        fixed_date = date(2019, 4, 28)
        result = self.d.get_offset("#", fixed_date)
        expected_result = date(2019, 4, 22)
        self.assertEqual(expected_result, result)

    def test_first_day_of_month(self):
        result = self.d.get_offset("%", date(2019, 10, 20))
        expected_result = date(2019, 10, 1)
        self.assertEqual(expected_result, result)

    def test_weekend_friday(self):
        result = self.d.get_offset("~", date(2019, 11, 1))
        expected_result = date(2019, 11, 1)
        self.assertEqual(expected_result, result)

    def test_weekend_saturday(self):
        result = self.d.get_offset("~", date(2019, 11, 2))
        expected_result = date(2019, 11, 4)
        self.assertEqual(expected_result, result)

    def test_weekend_sunday(self):
        result = self.d.get_offset("~", date(2019, 11, 3))
        expected_result = date(2019, 11, 4)
        self.assertEqual(expected_result, result)

    def test_weekend_monday(self):
        result = self.d.get_offset("~", date(2019, 11, 4))
        expected_result = date(2019, 11, 4)
        self.assertEqual(expected_result, result)

    def test_land_on_weekend(self):
        result = self.d.get_offset("4d~", date(2019, 10, 29))
        expected_result = date(2019, 11, 4)
        self.assertEqual(expected_result, result)

    def test_end_of_week(self):
        result = self.d.get_offset("*", date(2020, 3, 10))
        expected_result = date(2020, 3, 15)
        self.assertEqual(expected_result, result)
