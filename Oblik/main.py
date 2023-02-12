import FileDragAndDrop as fDr

rez=fDr.main()
for r in rez:
    ''' self.name = os.path.basename(path)
        self.path = path
        self.dir = path.replace(os.path.basename(path),'')[:-1]
        self.date_created = date_created
        self.date_modified = date_modified
        self.size = size'''
    print(r.path, r.name)