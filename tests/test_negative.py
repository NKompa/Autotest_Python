from checker import checkout_negative


badarx = "/home/user/badarx"
folder = "/home/user/folder1"


def test_step1():
    # Разархивируем архив arx2.7z в директорию folder1 и проверяем наличие в ней файлов test1 и test2.
    assert checkout_negative(f"cd {badarx}; 7z e arx2.7z -o{folder} -y", "ERRORS"), 'test1 FAILED'


def test_step2():
    # Проверяем целостность архива arx2.7z.
    assert checkout_negative(f"cd {badarx}; 7z t arx2.7z", "ERRORS"), "test2 FAILED"