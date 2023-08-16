import subprocess


def check_command(command, text):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0 and text in result.stdout:
        return True
    else:
        return False


if __name__ == "__main__":
    command = "cat /etc/os-release"
    text = 'PRETTY_NAME="Ubuntu 22.04.1 LTS"'
    if check_command(command, text):
        print("SUCCESS")
    else:
        print("FAIL")
