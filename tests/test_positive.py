from checker import checkout

tst = "/home/user/tst"
out = "/home/user/out"
folder = "/home/user/folder1"


def test_step1():
    # Создаём архив arx2 и проверяем его наличие в директории out.
    res1 = checkout(f"cd {tst}; 7z a /{out}/arx2", "Everything is Ok")
    res2 = checkout(f'ls {out}', "arx2.7z")
    assert res1 and res2, 'test1 FAILED'


def test_step2():
    # Разархивируем архив arx2.7z в директорию folder1 и проверяем наличие в ней файлов test1 и test2.
    res1 = checkout(f"cd {out}; 7z e arx2.7z -o{folder} -y", "Everything is Ok")
    res2 = checkout(f"ls {folder}", "test1")
    res3 = checkout(f"ls {folder}", "test2")
    assert res1 and res2 and res3, 'test2 FAILED'


def test_step3():
    # Проверяем целостность архива arx2.7z.
    assert checkout(f"cd {out}; 7z t arx2.7z", "Everything is Ok"), "test3 FAILED"


def test_step4():
    # Проверяем возможность обновить файл в архиве arx2.7z.
    assert checkout(f"cd {tst}; 7z u {out}/arx2.7z", "Everything is Ok"), "test4 FAILED"


# def test_step5():
#     # Удаляем файлы из архива.
#     assert checkout(f"cd {out}; 7z d arx2", "Everything is Ok")


def test_step6():
    # Вывод списка файлов в архиве arx2.7z.
    assert checkout(f"cd {out}; 7z l arx2.7z", "test1") and \
           checkout(f"cd {out}; 7z l arx2.7z", "test2"), "test6 FAILED"


def test_step7():
    # Разархивируем архив arx2.7z в директорию folder1 с сохранением путей и проверяем наличие файлов test1 и test2.
    res1 = checkout(f"cd {out}; 7z x -o{folder} -y arx2.7z", "Everything is Ok")
    res2 = checkout(f"ls {os.path.join(folder, tst)}", "test1")
    res3 = checkout(f"ls {os.path.join(folder, tst)}", "test2")
    assert res1 and res2 and res3, 'test7 FAILED'
