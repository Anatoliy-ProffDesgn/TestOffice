import os



# ---------------Отримуемо список імен файлів--------------
#   n_m - текст якій має бути у назві файлу
#   x - розширення файлу
#   dirName - дерикторія в якій має бути файл
def get_file(dir_name, n_m, x):
    file_names = []
    x = '.' + x.replace('.', '')
    for root, distr, files in os.walk(dir_name):
        for name in files:
            if n_m.lower() in name.lower() and x.lower() in name.lower():
                file_names.append(str(root+'/').replace('//', '/') + name)
    # print(len(file_names))
    return file_names


# -----------------тест--------------
dirName_Test = './DownloadPrices/'
x_Test = '.html'
n_m_Test = 'pric'
# dirName_Test = 'c:'
# x_Test = ''
# n_m_Test = ''
for f in get_file(dirName_Test, n_m_Test, x_Test):
    print(f)
