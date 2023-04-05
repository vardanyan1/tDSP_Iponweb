import os
import requests


def ssp_check(ssp_id, site_domain):
    ssp_ip = os.environ.get("SSP_HOST")
    if ssp_ip != "none":
        url = f"http://{ssp_ip}/ads.txt"
        params = {'domain': site_domain}
        timeout = 3  # Set the timeout in seconds

        try:
            # Make the HTTP request with added parameters, timeout, and check for 200 status code
            response = requests.get(url, params=params, timeout=timeout)
            if response.status_code == 200:
                content = response.text

                # Split the content into lines and check if the ssp_id is in the second column
                found = any(ssp_id == line.split(',')[1].strip() for line in content.splitlines())
            else:
                found = False

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # If a ConnectionError or Timeout occurs, return False
            found = False

    else:
        found = True

    return found
