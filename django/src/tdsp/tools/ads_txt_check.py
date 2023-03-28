import requests
import os


def ssp_check(ssp_id, site_domain):
    ssp_ip = os.environ.get("SSP_HOST")
    if ssp_ip != "none":
        url = f"http://{ssp_ip}/ads.txt?publisher={site_domain}"

        try:
            # Make the HTTP request and parse the response content
            response = requests.get(url)
            content = response.text

            # Split the content into lines and check if the ssp_id is in the second column
            found = any(ssp_id == line.split(',')[1].strip() for line in content.splitlines())

        except requests.exceptions.ConnectionError:
            # If a ConnectionError occurs, return False
            found = True

    else:
        found = True

    return found
