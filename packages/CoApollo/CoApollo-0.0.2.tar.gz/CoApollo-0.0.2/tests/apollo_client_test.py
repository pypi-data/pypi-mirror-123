# Press the green button in the gutter to run the script.
import os

import pytest

from apollo.apollo_client import ApolloClient


class TestApolloClient:
    def setup(self):
        APOLLO_APP_ID = 'COMS.Spider'
        APOLLO_META_SERVER = 'http://apollo-api.dev.co:80'
        APOLLO_SECRET = 'e5e6586f10984d66971a85871e568590'
        print('初始化客户端')
        self.apollo_client = ApolloClient(app_id=APOLLO_APP_ID,
                                     secret=APOLLO_SECRET,
                                     config_url=APOLLO_META_SERVER)

    def teardown(self):
        print('关闭客户端')


    def test_get_json_value(self):
        ftp_configs = self.apollo_client.get_json_value('ftp', None, 'container_tracking_inttra')

        assert ftp_configs is not None

    def test_get_json_from_net(self):
        configs = self.apollo_client.get_json_from_net('container_tracking_inttra')

        assert configs is not None


if __name__ == '__main__':
    pytest.main("-q --html=report.html")
