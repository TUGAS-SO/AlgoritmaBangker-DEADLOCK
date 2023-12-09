
# a = allocation, m = max, av = available, n = need
proses,a,m,av,n=[],[],[],[],[]

# Menghitung jumlah isi character di list x yang di print pada tabel
# Param x : list dimensi yang ke-2
def clip(x):
    return len(str(x[0]))+len(str(x[1]))+len(str(x[2]))+4

def inputNum(echo):
    try:
        num = int(input(echo))
        return num
    except:
        print('Format salah')
        return inputNum(echo)

# Print character isi list x pada tabel
# Param x : list dimensi yang ke-2
def isi(x):
    print('|',end='')
    for k in x:
        print(k,end='|')

# Mengukang pemilihan Max
# Param i : indeks Max yang ingin diisi ulang
def ulangMax(i):
    print('Tidak sesuai karena Max kurang dari allocation coba lagi')
    temp=input('Masukan Nilai Max '+str(i+1)+' (a,b,c): ')
    temp=temp.split(',')
    for j in range(len(temp)) :
            temp[j]=int(temp[j])
    for j in range(len(temp)) :
        # Jika max lebih besar dari allocation(memenuhi syarat)
        if(temp[j]>a[i][j]):
            m.append(temp)
            return None
    ulangMax(i)

# Membuat tabel
def table():
    
    print('Sumber daya : ',sd)
    print('_'*53+'\n| Process | Allocation |  Max  | Available |  Need  |')
    for baris in range(len(a)+1):
        kolom=0
        for i in range(49):
            # Pembatas(|) untuk setiap kolom
            if(kolom==0 or kolom==10 or kolom==23 or kolom==31 or kolom==43 or kolom==52):
                print('|', end='')

            # Barisan terakhir (n+1)
            elif(baris==(len(a))):
                # Print kolom available
                if (kolom==33) and (len(av)==(len(a)+1)):
                    kolom=kolom+clip(av[baris])-1
                    isi(av[baris])

                # Print kolom yang lain kosong
                else:
                    print(' ',end='')
            
            # Barisan 1 sampe n
            else:
                # Print kolom proses
                if kolom==4:
                    kolom=kolom+len(proses[baris])-1
                    print(proses[baris],end='')
                
                # Print kolom allocation
                elif kolom==13:
                    kolom=kolom+clip(a[baris])-1
                    isi(a[baris])
                
                # Print kolom max
                elif kolom==24:
                    kolom=kolom+clip(m[baris])-1
                    isi(m[baris])

                # Print kolom available
                elif (kolom==33) and (baris<len(av)):
                    kolom=kolom+clip(av[baris])-1
                    isi(av[baris])
                
                # Print kolom need
                elif kolom==44:
                    kolom=kolom+clip(n[baris])-1
                    isi(n[baris])
                else:
                    print(' ',end='')
            kolom=kolom+1
        print('')

def main():
    global sd # Sumber Daya
    sd =[]
    while len(sd) != 3:
        sd=input('Masukan Jumlah Sumber Daya (a,b,c): ')
        sd = sd.split(',')

        if(len(sd) != 3):
            print('Sumber daya harus 3 (a,b,c)')
    
    for i in range(len(sd)):
        sd[i]=int(sd[i])

    temp = inputNum('\nMasukan Jumlah Proses    : ')

    # masukan allocation
    for i in range(temp):
        a.append(input('Masukan Nilai Allocation '+str(i+1)+' (a,b,c): '))
        a[i]=a[i].split(',')
        for j in range(len(a[i])) :
            a[i][j]=int(a[i][j])

    print('')
    # masukan max
    for i in range(temp):
        temp=input('Masukan Nilai Max '+str(i+1)+' (a,b,c): ')
        temp=temp.split(',')
        for j in range(len(temp)) :
            temp[j]=int(temp[j])
        for j in range(len(temp)) :
            # Jika max lebih besar dari allocation(memenuhi syarat)
            if(temp[j]<a[i][j]):
                ulangMax(i)
                break
        
        if(i+1>len(m)):
            m.append(temp)
    
    # jumlah proses
    for i in range(len(a)):
        proses.append('P'+str(i))

    # kalkulasi need
    for i in range(len(a)):
        n.append([])
        for j in range(len(a[i])):
            temp= m[i][j]-a[i][j]
            n[i].append(temp)

    # total jumlah allocation
    temp= [0,0,0]
    for i in range(len(a)):
        for j in range(len(a[i])):
            temp[j] = temp[j]+a[i][j]

    # algoritma banker available
    av.append([sd[0]-temp[0],sd[1]-temp[1],sd[2]-temp[2]])

    temp.clear()
    save_point=[0]*len(a) # flag proses
    i=0 # Proses yang dijalankan
    c=0 # Proses yang telah berhasil dijalankan

    # len(temp) <= len(a) == proses telah berhasil dijalankan semua
    # save_point.count(2)<1 == proses telah deadlock
    while((len(temp) <= len(a)) and (save_point.count(2)<1)):

        # temp.count(i)<1 == proses belum pernah berhasil dijalankan
        # n[i][0]<=av[c][0] == membandingkan need dengan available
        if (temp.count(i)<1) and (n[i][0]<=av[c][0]) and (n[i][1]<=av[c][1]) and (n[i][2]<=av[c][2]):
            c=c+1
            temp.append(i) # Menambah proses i ke temp untuk proses yang telah dijalankan
            save_point=[0]*len(a) # reset save point

            av.append([])
            for j in range(len(a[i])):
                av[c].append(av[c-1][j]+a[i][j])

        # ulang i dari proses 0
        save_point[i]=save_point[i]+1
        i=i+1
        if i >= len(a) :
            i=0

    # Membuat tabel
    table()

    # Jika allocation kurang dari sama dengan available == DEADLOCK
    if(len(a) >= len(av)):
        print('DEADLOCK')

    # Print proses urutan yang dijalankan lebih dahulu
    print('Proses urutan :',temp)

main()
