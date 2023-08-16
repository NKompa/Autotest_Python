import subprocess
import string


def check_command_output(command, text, modify_text=False):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout
        if modify_text:
            output = output.split()
            output = [word.strip(string.punctuation) for word in output]
            output = ' '.join(output)
        if text in output:
            return True
    return False


if __name__ == "__main__":
    command1 = "cat /etc/os-release"
    text1 = 'Ubuntu 22.04.1 LTS'
    if check_command_output(command1, text1, modify_text=True):
        print("SUCCESS")
    else:
        print("FAIL")
