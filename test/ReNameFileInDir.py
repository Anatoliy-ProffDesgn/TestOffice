import os

dirname = 'C:/Users/natol_ba3j6nf/OneDrive/RFlesh/Pro100-5.20-GIV/Библиотека/Материалы/[anatolij]/Столешницы Мрамор, Гранит, Камень, Крошка, Дерево/Egger Viyar'
rep_str = 'Viyar Стільниця Egger '
new_str = ''
no_iter = 0


def startRename(dirname, rep_str, new_str, no_iter=0):
    print('Умови:\n', dirname, '\n', rep_str, '\n', new_str, '\n', 'Start')
    for root, distr, files in os.walk(dirname):  # Separate the base name and the extension name,
        for filename in files:
            no_iter += 1
            # print(root)
            try:
                # ext = os.path.splitext(filename)  # Create the new file name
                # print(filename)
                old_nm = root + '/' + filename
                new_nm = filename.replace('  ', ' ')
                new_nm = new_nm.replace(rep_str, new_str)
                # print(new_nm)
                new_nm = root + '/' + new_nm
                if not old_nm == new_nm:
                    os.rename(old_nm, new_nm)
                    print(new_nm)
            except:
                print(no_iter)

    print('End')


startRename(dirname, rep_str, new_str)
