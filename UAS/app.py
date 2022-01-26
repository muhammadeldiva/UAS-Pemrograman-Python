import requests
from mysql import connector
from texttable import Texttable

db = cursor = None

base_url =  "https://api.abcfdab.cfd"

def openDb():
    global db, cursor
    db = connector.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "db_akademik_0474" 
    )    

    cursor = db.cursor()	

def closeDb():
    global db, cursor
    cursor.close()
    db.close()


def input_data_to_database():    
    endpoint = '/students'
    endpoint2 = '/students/1'
    req = requests.get(base_url+endpoint)
    if req.status_code == requests.codes.ok:
        text = 'sedang menginput data ke database....'
        print(text)
        data = req.json()       

        openDb()
        for post in data['data']:
            nim = post['nim']
            nama = post['nama']
            jenis_kelamin = post['jk']
            jurusan = post['jurusan']
            alamat = post['alamat']
            
            sql = 'insert into tbl_students_0474 (nim, nama, jenis_kelamin, jurusan, alamat) values (%s, %s, %s, %s, %s)'
            val = (nim, nama, jenis_kelamin, jurusan, alamat)
            cursor.execute(sql, val)
            db.commit()
    else:
        print('Gagal mendapat respon')
    
    req2 = requests.get(base_url+endpoint2)
    if req2.status_code == requests.codes.ok:
        data2 = req2.json()       

        openDb()
        for posting in data2:
            nim2 = posting['nim']
            nama2 = posting['nama']
            jenis_kelamin2 = posting['jk']
            jurusan2 = posting['jurusan']
            alamat2 = posting['alamat']
            
            sql = 'insert into tbl_students_0474 (nim, nama, jenis_kelamin, jurusan, alamat) values (%s, %s, %s, %s, %s)'
            val = (nim2, nama2, jenis_kelamin2, jurusan2, alamat2)
            cursor.execute(sql, val)
            db.commit()
    else:
        print('Gagal mendapat respon')
        
    

# Menu Utama
def show_data_mahasiswa():
    table = Texttable()
    openDb()
    sql = 'select * from tbl_students_0474'
    cursor.execute(sql)
    result = cursor.fetchall()
    closeDb()

    no = 0
    dbnim = []
    dbnama = []
    dbjk = []
    dbjurusan = []
    dbalamat = []

    for data in result:       
        dbnim.append(data[1])
        dbnama.append(data[2])
        dbjk.append(data[3])
        dbjurusan.append(data[4])
        dbalamat.append(data[5])
        no += 1
    
    for i in range(no):
        nim = dbnim
        nama = dbnama
        jk = dbjk
        jurusan = dbjurusan
        alamat = dbalamat      
    
        table.add_rows([['No.', 'NIM', 'Nama', 'JK', 'Jurusan', 'Alamat'],[i+1, nim[i], nama[i], jk[i], jurusan[i], alamat[i]]])
    print(table.draw())
    
    

def show_data_mahasiswa_by_limit():
    table = Texttable()
    limit = int(input("Masukkan Limit: "))
    openDb()
    sql = 'select * from tbl_students_0474'
    cursor.execute(sql)
    result = cursor.fetchmany(limit)
    
    if limit < 1:
        table.add_rows([['No.', 'NIM', 'Nama', 'JK', 'Jurusan', 'Alamat'],['', '', '', '', '', '']])
        print(table.draw())

    else:
        no = 0
        dbnim = []
        dbnama = []
        dbjk = []
        dbjurusan = []
        dbalamat = []

        for data in result:       
            dbnim.append(data[1])
            dbnama.append(data[2])
            dbjk.append(data[3])
            dbjurusan.append(data[4])
            dbalamat.append(data[5])
            no += 1
        
        for i in range(no):
            nim = dbnim
            nama = dbnama
            jk = dbjk
            jurusan = dbjurusan
            alamat = dbalamat

            table.add_rows([['No.', 'NIM', 'Nama', 'JK', 'Jurusan', 'Alamat'],[i+1, nim[i], nama[i], jk[i], jurusan[i], alamat[i]]])
        print(table.draw())

    

def show_data_mahasiswa_by_nim():
    
    table = Texttable()
    input_nim = str(input("Masukkan NIM: "))
    openDb()
    cursor.execute('select * from tbl_students_0474 where nim=%s',(input_nim,))
    result = cursor.fetchall()
    
    no = 0
    dbnim = []
    dbnama = []
    dbjk = []
    dbjurusan = []
    dbalamat = []

    for data in result:       
        dbnim.append(data[1])
        dbnama.append(data[2])
        dbjk.append(data[3])
        dbjurusan.append(data[4])
        dbalamat.append(data[5])
        no += 1
    
    for i in range(no):
        nim = dbnim
        nama = dbnama
        jk = dbjk
        jurusan = dbjurusan
        alamat = dbalamat

    if input_nim in dbnim:
        print('Data NIM %s ditemukan!' % (input_nim))
        table.add_rows([['No.', 'NIM', 'Nama', 'JK', 'Jurusan', 'Alamat'],[i+1, nim[i], nama[i], jk[i], jurusan[i], alamat[i]]])
        print(table.draw())
        show_menu()
    
    if input_nim not in dbnim:
        print('Data NIM %s tidak ditemukan!' % (input_nim))
        table.add_rows([['No.', 'NIM', 'Nama', 'JK', 'Jurusan', 'Alamat'],['NA', 'NA', 'NA', 'NA', 'NA', 'NA']])
        print(table.draw())
        show_menu()
    


def show_menu():
    print('''
------Menu------
1. Tampilkan Semua Data
2. Tampilkan Data Berdasarkan Limit
3. Cari Data Berdasarkan NIM
0. Exit
    ''')

    menu = int(input("Pilih menu> "))
    print('\n')
    if menu == 1:
        show_data_mahasiswa()
    if menu == 2:
        show_data_mahasiswa_by_limit()
    if menu == 3:
        show_data_mahasiswa_by_nim()
    if menu == 0:
        exit()

if __name__ == '__main__':
    input_data_to_database()
    while True:    
        show_menu()