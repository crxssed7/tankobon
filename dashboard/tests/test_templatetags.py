from django.test import TestCase

from dashboard.templatetags import dashboard_tags


class TestDashboardTags(TestCase):
    def test_dashboard_active_tab(self):
        value = "/dashboard/stats/"
        expected_1 = "bg-hint text-blay font-bold"
        actual_1 = dashboard_tags.dashboard_active_tab(value, "/dashboard/stats/")
        self.assertEquals(expected_1, actual_1)
        expected_2 = "hover:bg-hint hover:text-blay hover:border-hint focus:bg-hint focus:blay focus:text-blay transition duration-300 ease-in-out"
        actual_2 = dashboard_tags.dashboard_active_tab(value, "test")
        self.assertEquals(expected_2, actual_2)
