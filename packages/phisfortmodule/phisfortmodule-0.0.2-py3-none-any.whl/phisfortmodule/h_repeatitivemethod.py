import os
import zipfile
import tarfile
import requests
import subprocess
import platform
import tldextract
from fuzzywuzzy import fuzz


RATIO_LIMIT = 65

dir_path = os.path.dirname(os.path.realpath(__file__))

PUSH_SIMPLE_PAYLOAD = {
    'Content-Type': 'application/json',
    'x-api-key': 'fRnKDdW6TC3XSnCg1HPKA4xVemLIebL398jnxNd9'
}

def add_harvester(a,b):
    return a+b

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def inv_intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3


def write_list_data_to_file(data_list, file_name="dynamic_previous.txt"):
    text_file = open(file_name, 'w')
    for element in data_list:
        text_file.write(element + "\n")
    text_file.close()
    return "written done"


def write_existing_list_data(data_list, file_name="dynamic_previous.txt"):
    text_file = open(file_name, 'a')
    for element in data_list:
        text_file.write(element + "\n")
    text_file.close()
    return "appending done"


def collect_data_from_file(file_name="dynamic_previous.txt"):
    f = open(file_name, "r")
    prev_all = []
    for single in f:
        str_data = str(single)
        refined = str_data.rstrip("\n")
        prev_all.append(refined)

    return prev_all


def make_unique_list(get_list):
    set_list = set(get_list)
    u_list = list(set_list)
    return u_list


def extract_zip():
    with zipfile.ZipFile("filename.zip", "r") as zip_ref:
        zip_ref.extractall(dir_path)


def extract_tar():
    tar = tarfile.open("ALL-phishing-domains.tar.gz", "r:gz")
    tar.extractall()
    tar.close()
    return "extraction done"


def download_file(url):
    result = requests.get(url)
    with open("ALL-phishing-domains.tar.gz", "wb") as code:
        code.write(result.content)


def ping_domain(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0


def download_txt_from_online():
    url = "https://www.openphish.com/feed.txt"
    result = requests.get(url)
    with open("feed.txt", "wb") as code:
        code.write(result.content)


def make_a_file_unique(file_name="dynamic_previous.txt"):
    f = open(file_name, "r")
    prev_all = []
    for single in f:
        str_data = str(single)
        refined = str_data.rstrip("\n")
        prev_all.append(refined)
    f.close()
    data_list = list(set(prev_all))
    text_file = open(file_name, 'w')
    for element in data_list:
        text_file.write(element + "\n")
    text_file.close()


def domain_matcher(client_domain, matching_domain):
    parent_domain = []
    l = len(client_domain)

    # detect all domain that is 70% match with the client domain
    for i in range(l):
        for single_domain in matching_domain:
            d1 = tldextract.extract(single_domain).domain
            d2 = tldextract.extract(client_domain[i]).domain
            r_point = fuzz.ratio(d1,d2)
            if r_point>=RATIO_LIMIT:
                parent_domain.append(single_domain)

    return parent_domain


def get_active_client_domains():
    simple_payload = PUSH_SIMPLE_PAYLOAD
    acd_url = "https://serverless.phishfort.com/dev/getActiveClientDomains"
    result = requests.get(acd_url, headers=simple_payload)
    result2 = result.json()
    miscDomains = result2["miscDomains"]
    #print(miscDomains)
    return result2["domains"]


def reduce_duplicate_and_return_with_suffix(domain_list):
    domain_suffix = {}
    tdomain = []
    for single_domain in domain_list:
        domain = tldextract.extract(single_domain)
        dsuffix = domain.suffix
        domain = domain.domain
        tdomain.append(domain)
        domain_suffix[domain] = dsuffix

    unique_domain = list(set(tdomain))
    reduced_duplicat = []
    for single_domain in unique_domain:
        if domain_suffix[single_domain]!="":
            reduced_duplicat.append((single_domain+"."+domain_suffix[single_domain]))

    return reduced_duplicat
