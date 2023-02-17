import os

dirname = 'C:/Users/natol_ba3j6nf/OneDrive/RFlesh/Pro100-5.20-GIV/Библиотека/Материалы/[anatolij]/Столешницы Мрамор, Гранит, Камень, Крошка, Дерево/LuxeForm Viyar/'
rep_str = 'Viyar Стільниця Luxform '
new_str = ''
for filename in os.listdir(dirname):  # Separate the base name and the extension name,
    ext = os.path.splitext(filename)  # Create the new file name
    old_nm = dirname + ext[0] + ext[1]
    new_nm = ext[0].replace(rep_str, new_str) + ext[1]
    print(new_nm)
    new_nm = dirname + new_nm
    os.rename(old_nm, new_nm)
