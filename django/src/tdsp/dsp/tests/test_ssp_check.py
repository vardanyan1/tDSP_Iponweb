import os
import unittest
import requests
from unittest.mock import patch, MagicMock

# Relative import for ads_txt_check
from ...tools import ads_txt_check


class TestSSPCheck(unittest.TestCase):

    @patch('tdsp.tools.ads_txt_check.requests.get')
    @patch('tdsp.tools.ads_txt_check.os.environ.get')
    def test_ssp_check(self, mock_env_get, mock_requests_get):
        # Set up a test ads.txt content
        test_ads_txt = '''criteo.com, 9SP54, DIRECT
        google.com, 67812, DIRECT
        smartadserver.com, 4074, DIRECT'''

        # Mock the response from requests.get
        response = requests.Response()
        response.status_code = 200
        response._content = test_ads_txt.encode()
        mock_requests_get.return_value = response

        # Mock the environment variable SSP_HOST
        mock_env_get.return_value = "test_ssp_ip"

        # Test with an existing ssp_id
        existing_ssp_id = "9SP54"
        site_domain = "nw.com"
        self.assertTrue(ads_txt_check.ssp_check(existing_ssp_id, site_domain))

        # Test with a non-existing ssp_id
        non_existing_ssp_id = "12345"
        self.assertFalse(ads_txt_check.ssp_check(non_existing_ssp_id, site_domain))

        # Test with SSP_HOST set to "none"
        mock_env_get.return_value = "none"
        self.assertTrue(ads_txt_check.ssp_check(existing_ssp_id, site_domain))


if __name__ == '__main__':
    unittest.main()

