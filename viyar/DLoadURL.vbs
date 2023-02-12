Dim avFiles
Dim oShell
Dim sUrl As String
sub Main()
    call DownloadFile
End sub

public function DownloadFile() As Boolean
    If MsgBox("Загрузить файл .csv с сайта viyar.ua?" & Chr(13) & "Нет - если у вас уже есть ранее скачаный файл.", vbQuestion + vbYesNo) = vbYes Then
    sUrl = "https://viyar.ua/excel_export/?id=1981&lang=ru"
    Set oShell = CreateObject("Wscript.Shell")
    oShell.Run (sUrl)
    End If
    avFiles = Application.GetOpenFilename("Excel files(*.csv*),*.csv*", 1, "Выбрать CSV файлы", , True)
    If VarType(avFiles) = vbBoolean Then Exit Sub 'была нажата кнопка отмены - выход из процедуры
end function