import random
import string
import yaml
import pytest
import time
from sshcheckers import ssh_checkout_negative

with open("config.yaml") as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout_negative(f"{data['host']}", f"{data['remote_user']}", "2222",
                        "mkdir {} {} {} {}".format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                   data['folder_badarx']), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout_negative(f"{data['host']}", f"{data['remote_user']}", "2222",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                            data['folder_badarx']), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data['count_files']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout_negative(f"{data['host']}", f"{data['remote_user']}", "2222",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(
                            data['folder_in'], filename, data["size_file"]), ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout_negative(f"{data['host']}", f"{data['remote_user']}", "2222",
                        "cd {}; mkdir {}".format(data['folder_in'], subfoldername), ""):
        return None, None
    if not ssh_checkout_negative(f"{data['host']}", f"{data['remote_user']}", "2222",
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_badarx():
    ssh_checkout_negative(f"{data['host']}", f"{data['remote_user']}", "2222",
                 "cd {}; 7z a {}/badarx.7z".format(data['folder_in'], data['folder_badarx']), "Everything is Ok")
    ssh_checkout_negative(f"{data['host']}", f"{data['remote_user']}", "2222",
                 "truncate -s 1 {}/badarx.7z".format(data['folder_badarx']), "Everything is Ok")
    yield 'badarx'
    ssh_checkout_negative(f"{data['host']}", f"{data['remote_user']}", "2222",
                 "rm -f {}/badarx.7z".format(data['folder_badarx']), "")


@pytest.fixture(autouse=True)
def write_stats_to_file():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    count_files = data['count_files']
    size_file = data['size_file']
    with open("/proc/loadavg") as load_file:
        load_avg = load_file.readline().strip()
    stat_line = f"{timestamp}, {count_files}, {size_file}, {load_avg}\n"
    with open("stat.txt", 'a') as stat_file:
        stat_file.write(stat_line)
    yield
