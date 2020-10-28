#coding=utf-8
from public import mytest
from ddt import ddt, data
from public.data_info import get_test_case_data, data_info
# import json
file = 'data'

@ddt
class Other(mytest.MyTokenTest):
    """其他需要验证token的接口"""

    @data(*get_test_case_data(data_info, file, 'other'))
    def test_api(self, data):
        r = self.send_requests.send_request_all(data)
        assert_info = data['assert_info']
        self.assertEqual(r['code'], assert_info['code'])
        self.assertEqual(r['msg'], assert_info['msg'])