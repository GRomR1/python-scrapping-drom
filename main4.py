import os
import zipfile
from time import sleep

from selenium import webdriver
from main3 import *

PROXY_HOST = 'vpn.w2w2.top'  # rotating proxy
PROXY_PORT = 32382
PROXY_USER = 'nas'
PROXY_PASS = 'ESiztsS8frQ55Gpg'
# https://botproxy.net/docs/how-to/setting-chromedriver-proxy-auth-with-selenium-using-python/

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
          },
          bypassList: ["localhost"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        chrome_options=chrome_options)
    return driver

def main():
    driver = get_chromedriver(use_proxy=True)
    # driver = webdriver.Chrome()
    # user_id = 'Aniku'
    # for user_id in ['Replika777', 'Aniku', 'WorldWheels']:
    # for user_id in ['Aniku', 'WorldWheels']:
    for user_id in ['WorldWheels']:
        print("user_id {}".format(user_id))
        # content = get_html(driver, 'https://baza.drom.ru/user/{}'.format(user_id))
        # save_content(content, "{}.html".format(user_id))
        content = open_content("{}.html".format(user_id))
        disks = parse_user_page(content)
        # save_disks(disks, '{}.csv'.format(user_id))
        disks_full_info = []
        i = 0
        for disk in disks:
            print("{}/{}".format(i, len(disks)))
            disk_content = get_disk_page(disk['link'], driver)
            # disk_content = get_disk_page("https://baza.drom.ru/vladivostok/wheel/disc/novye-dipovye-js-105-hyper-r17-64794648.html", driver)
            # parse_disk_page(disk_content, 0)
            add_info = parse_disk_page(disk_content, disk['price'])
            add_info['seller'] = user_id
            disk.update(add_info)
            disks_full_info.append(disk)
            i += 1
        save_disks(disks, "{}_full_info.csv".format(user_id))

if __name__ == '__main__':
    main()