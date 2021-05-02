import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from GFG_analysis import compute_metrics


class MyTestCase(unittest.TestCase):
    def test_compute_metrics(self):
        data = [['App install network A', 'Paid', '20', '3,000', '30', '1,000', '42'],
                ['App install network B', 'Free', '80', '20020', '50', '200', '42'],
                ['Web channel A', 'Paid', '19', '4', '35', '20', '42'],
                ['Web channel B', 'Free', '2000', '15', '17', '30', '42'],
                ['PR', 'Paid', '40', '17', '18', '9', '42'],
                ['Web channel A', 'Free', '1', '300,000', '19', '4', '43'],
                ['Web channel B', 'Paid', '3', '20', '20', '5', '43'],
                ['PR', 'Free', '33', '1', '100', '8,888', '43']]

        df = pd.DataFrame(data=data, columns=['Channel', 'Paid_Free', 'Spend', 'Visits', 'Orders', 'Revenue', 'Week'])
        output_data = \
            [['App install network A', 'Paid', '20', '3,000', '30', '1,000', '42', 0.01, 33.33, 0.02,
              'App install network'],
             ['App install network B', 'Free', '80', '20020', '50', '200', '42', 0.0025, 4, 0.4, 'App install network'],
             ['Web channel A', 'Paid', '19', '4', '35', '20', '42', 8.75, 0.5714, 0.95, 'Web channel'],
             ['Web channel B', 'Free', '2000', '15', '17', '30', '42', 1.1333, 1.7647, 66.6667, 'Web channel'],
             ['PR', 'Paid', '40', '17', '18', '9', '42', 1.0588, 0.5, 4.444, 'PR'],
             ['Web channel A', 'Free', '1', '300,000', '19', '4', '43', 0.0000133, 0.2105, 0.25, 'Web channel'],
             ['Web channel B', 'Paid', '3', '20', '20', '5', '43', 1, 0.25, 0.6, 'Web channel'],
             ['PR', 'Free', '33', '1', '100', '8,888', '43', 100, 88.88, 0.003713, 'PR']]
        df_expected_output = pd.DataFrame(data=output_data,
                                          columns=['Channel', 'Paid_Free', 'Spend', 'Visits', 'Orders', 'Revenue',
                                                   'Week', 'CR', 'ABS', 'CIR', 'Channel_Type'])
        df_expected_data_week = pd.DataFrame([{'Week': '42', 'CR': 2.1909, 'ABS': 8.034, 'CIR': 14.496},
                                              {'Week': '43', 'CR': 33.6667, 'ABS': 29.78, 'CIR': 0.2846}])
        df_expected_data_paid_free = pd.DataFrame([{'Paid_Free': 'Paid', 'CR': 2.7047, 'ABS': 8.6637, 'CIR': 1.5036},
                                                   {'Paid_Free': 'Free', 'CR': 25.284, 'ABS': 23.7138, 'CIR': 16.83}])
        df_expected_data_channel_type = pd.DataFrame(
            [{'Channel_Type': 'App install network', 'CR': 0.006249, 'ABS': 18.6667, 'CIR': 0.21},
             {'Channel_Type': 'Web channel', 'CR': 2.7208, 'ABS': 0.6992, 'CIR': 17.1167},
             {'Channel_Type': 'PR', 'CR': 50.5294, 'ABS': 44.69, 'CIR': 2.22408}, ])

        df_output, df_data_week, df_data_channel_type, df_data_paid_free = compute_metrics(df)
        assert_frame_equal(df_expected_output, df_output)
        assert_frame_equal(df_expected_data_week, df_data_week)
        assert_frame_equal(df_expected_data_paid_free, df_data_paid_free)
        assert_frame_equal(df_expected_data_channel_type, df_data_channel_type)


if __name__ == '__main__':
    unittest.main()
