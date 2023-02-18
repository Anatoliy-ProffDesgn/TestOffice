import xlrd as xl

# name_book = 'newPrice1.xls'
wb_name = 'newPrice1.xls'

# def fun_bk(wb_name):
wb = xl.open_workbook("newPrice1.xls",ignore_workbook_corruption=True, encoding_override='koi8_r')
# wb = xl.open_workbook_xls(wb_name)
print(wb_name)
print("The number of worksheets is {0}".format(wb.nsheets))
print("Worksheet name(s): {0}".format(wb.sheet_names()))
sh = wb.sheet_by_index(0)
print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
for rx in range(sh.nrows):
    print(sh.row(rx))


# fun_bk(name_book)
