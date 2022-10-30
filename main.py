import os
import exifread
import shutil


def rename(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)

    FIELD = 'EXIF DateTimeOriginal'
    if FIELD in tags:
        _type = os.path.splitext(file_path)[1]
        _name = str(tags[FIELD]).replace(':', '').replace(' ', '_')
        _year = _name[:4]
        _name = 'IMG_' + _name
        copy(file_path, _name, _type, _year)
        return True
    else:
        print("copy {} -> {}".format(file_path,
              os.path.join('./cannot', os.path.split(file_path)[1])))
        shutil.copy(file_path,
                    os.path.join('./cannot', os.path.split(file_path)[1]))
        return False


def copy(old_path, _name, _type, year):
    if not os.path.exists(year):
        os.mkdir(year)

    new_path = os.path.join(year, _name + _type)
    c = 0
    while os.path.exists(new_path):
        new_path = os.path.join(year, _name + str(c) + _type)
        c += 1

    print("copy {} -> {}".format(old_path, new_path))
    shutil.copy(old_path, new_path)


if __name__ == '__main__':
    cnt = len(os.listdir("./data"))
    cur = 1
    succ = 0
    fail = 0
    for file in os.listdir("./data"):
        path = os.path.join("./data", file)
        print('[{}/{}] {}'.format(cur, cnt, path))
        cur += 1
        if rename(path):
            succ += 1
        else:
            fail += 1
    print("Total: {}, Succ: {}, Fail: {}".format(cnt, succ, fail))
