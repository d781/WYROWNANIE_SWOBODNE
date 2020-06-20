import numpy as np

# Wczytywanie danych z pliku tekstowego
def wczytaj(plik):
    tmp = []
    with open(plik, 'r+') as pl:
        linie = pl.readlines()
        for ln in linie:
            li = ln.rstrip().lstrip().split()
            tmp.append(li)
    return  tmp

# Obliczanie długości ze współrzędnych
def dlugosc(p, k):
    dx = k[1] - p[1]
    dy = k[2] - p[2]
    dl = np.sqrt(dx ** 2 + dy ** 2)
    return dl

# Obliczanie azymutu ze współrzędnych
def azymut(p, k, jednostka='g'):
    dx = k[1] - p[1]
    dy = k[2] - p[2]
    if dy == 0:
        if dx > 0:
            az = 0
        elif dx < 0:
            az = 200
    elif dx == 0:
        if dy > 0:
            az = 100
        elif dy < 0:
            az = 300
    else:
        if dx < 0:
            az = 200 + np.arctan(dy / dx) * 200 / np.pi
        elif dx > 0:
            if dy > 0:
                az = np.arctan(dy / dx) * 200 / np.pi
            elif dy < 0:
                az = 400 + np.arctan(dy / dx) * 200 / np.pi
    if az >= 400:
        az = az - 400

    if jednostka == 'r':
        az = az * np.pi /200
    elif jednostka == 's':
        az = az * 9 / 10
    return az

# Funkcja szukająca danego punktu w zbiorze
def szukaj(nr,wsp):
    tmp = 'brak'
    for i in wsp:
        if str(i[0]) == str(nr):
            tmp = i
    return tmp

#Przeliczanie kierunków na katy
def kie2katy(kier):
    stan = []
    st = kier[0][0]
    tmp = []
    for i in kier:
        if i[0] == st:
            tmp.append(i)
        else:
            st = i[0]
            stan.append(tmp)
            tmp = []
            tmp.append(i)
    stan.append(tmp)
    tmp = []
    for st in stan:
        for i, nr in enumerate(st):
            if i == 0:
                zerowy = nr[2]
                lewe = nr[1]
            else:
                nr[2] = nr[2] - zerowy
                if nr[2] < 0:
                    nr[2] += 400
                nr.insert(0,lewe)
                tmp.append(nr)
    return tmp


# Tworzenie równania obserwacyjnego dla kątów
def rownanie_katy(kat, wsp):
    ro = 63.6620
    l = szukaj(kat[0], wsp)
    c = szukaj(kat[1], wsp)
    p = szukaj(kat[2], wsp)
    rl = azymut(c, l, 'g')
    rp = azymut(c, p, 'g')
    kat_przy = rp - rl
    if kat_przy < 0:
        kat_przy += 400
    dl_lewa = dlugosc(l, c)
    dl_prawa = dlugosc(c, p)
    Al = (l[1] - c[1]) * ro / (dl_lewa ** 2)
    Bl = (l[2] - c[2]) * ro / (dl_lewa ** 2)
    Ap = (p[1] - c[1]) * ro / (dl_prawa ** 2)
    Bp = (p[2] - c[2]) * ro / (dl_prawa ** 2)
    dK = (kat[3] - kat_przy)
    row = [[] for i in range(6)]
    row[0].append('dx_' + l[0])
    row[0].append(Bl)
    row[1].append('dy_' + l[0])
    row[1].append(-Al)
    row[2].append('dx_' + p[0])
    row[2].append(-Bp)
    row[3].append('dy_' + p[0])
    row[3].append(Ap)
    row[4].append('dx_' + c[0])
    row[4].append(- ( Bl - Bp ))
    row[5].append('dy_' + c[0])
    row[5].append(Al - Ap)
    return row , dK

#Tworzenie równania obserwacyjnego dla azymutu
def rownanie_azymut(az, wsp):
    ro = 63.6620
    p = szukaj(az[1], wsp)
    c = szukaj(az[0], wsp)
    l = ['a.q',c[1] + 2000, c[2] ]
    rl = azymut(c, l, 'g')
    rp = azymut(c, p, 'g')
    kat_przy = rp - rl
    if kat_przy < 0:
        kat_przy += 400
    dl_lewa = dlugosc(l, c)
    dl_prawa = dlugosc(c, p)
    Al = (l[1] - c[1]) * ro / (dl_lewa ** 2)
    Bl = (l[2] - c[2]) * ro / (dl_lewa ** 2)
    Ap = (p[1] - c[1]) * ro / (dl_prawa ** 2)
    Bp = (p[2] - c[2]) * ro / (dl_prawa ** 2)
    dK = (az[2] - rp)
    row = [[] for i in range(4)]
    row[0].append('dx_' + c[0])
    row[0].append(-(Bl-Bp))
    row[1].append('dy_' + c[0])
    row[1].append(Al - Ap)
    row[2].append('dx_' + p[0])
    row[2].append(-Bp)
    row[3].append('dy_' + p[0])
    row[3].append(Ap)
    return row , dK

#Tworzenie równania obserwacyjnego dla azymutu2
def rownanie_azymut2(az, wsp):
    ro = 63.6620
    k = szukaj(az[1], wsp)
    p = szukaj(az[0], wsp)
    rl = azymut(p, k, 'g')
    dl_lewa = dlugosc(p, k)
    A = (k[1] - p[1]) * ro / (dl_lewa ** 2)
    B = (k[2] - p[2]) * ro / (dl_lewa ** 2)
    dK = (az[2] - rl)
    row = [[] for i in range(4)]
    row[0].append('dx_' + p[0])
    row[0].append(B)
    row[1].append('dy_' + p[0])
    row[1].append(-A)
    row[2].append('dx_' + k[0])
    row[2].append(-B)
    row[3].append('dy_' + k[0])
    row[3].append(A)
    return row , dK

#Tworzenie równania obserwacyjnego dla długości:
def rownanie_dlugosc(dl, wsp):
    k = szukaj(dl[1], wsp)
    p = szukaj(dl[0], wsp)
    d = dlugosc(k, p)
    cos = (k[1] - p[1]) / d
    sin = (k[2] - p[2]) / d
    dK = (dl[2] - d)
    row = [[] for i in range(4)]
    row[0].append('dx_' + p[0])
    row[0].append(-cos)
    row[1].append('dy_' + p[0])
    row[1].append(-sin)
    row[2].append('dx_' + k[0])
    row[2].append(cos)
    row[3].append('dy_' + k[0])
    row[3].append(sin)
    return row , dK

#Wyznaczenie współczynników dla wszystkich kątów
def wspolczynniki_katy(katy, wsp):
    A = []
    L = []
    for i in katy:
        tmpA, tmpL = rownanie_katy(i, wsp)
        A.append(tmpA)
        L.append(tmpL)
    return A, L

#Wyznaczenie współczynników dla wszystkich dlugosci
def wspolczynniki_dlugosci(dl, wsp):
    A = []
    L = []
    for i in dl:
        tmpA, tmpL = rownanie_dlugosc(i, wsp)
        A.append(tmpA)
        L.append(tmpL)
    return A, L

#Wyznaczenie współczynników dla wszystkich azymutów
def wspolczynniki_azymuty(az, wsp):
    A = []
    L = []
    for i in az:
        tmpA, tmpL = rownanie_azymut2(i, wsp)
        A.append(tmpA)
        L.append(tmpL)
    return A, L

# Utworzenie opisu macierzy A
def opisA(wsp):
    opis_A = []
    for i in wsp:
        if i[3] == 1:
            opis_A.append('dx_' + i[0])
            opis_A.append('dy_' + i[0])
    return opis_A

#Tworzenie macierzy A i L
def macierzA(A,obs,opis):
    for obserwacja in obs:
        tmp = [0 for i in opis]
        for i, ind in enumerate(opis):
            for ob in obserwacja:
                if ob[0] == ind:
                    tmp[i] = ob[1]
        A.append(tmp)
    return A

#Wyznaczenie parametrów elips błędów
def elipsy(pkt,opis_A, cov):
    for pt in pkt:
        if pt[3] !=0:
            for i, id in enumerate(opis_A):
                naz = id.split('_')[1]
                xy = id.split('_')[0]
                if naz == pt[0] and xy == 'dx':
                    VX = cov[i][i]
                    wx = i
                elif naz == pt[0] and xy == 'dy':
                    VY = cov[i][i]
                    wy = i
            covXY = cov[wx,wy]
            elipsaA = np.sqrt(((VX+VY)/2) + np.sqrt((((VX-VY)/2) ** 2) + covXY ** 2 ))
            elipsaB = np.sqrt(((VX + VY) / 2) - np.sqrt((((VX - VY) / 2) ** 2) + covXY ** 2))
            elipsaFi = azymut(['', 0, 0], ['', VX-VY, 2*covXY])/2
        else:
            elipsaA = 0
            elipsaB = 0
            elipsaFi = 0
        pt.append(elipsaA)
        pt.append(elipsaB)
        pt.append(elipsaFi)
    return pkt

#Zapis do pliku współrzędnych
def zapis_wsp(sciezka, dok, dok_bl, wsp):
    pl = open(sciezka + '/WSP_WYRÓWNANE.txt', 'w+')
    pl.write('Nr\tX [m]\tY[m]\tmx[mm]\tmy[mm]\tmp[mm]\n')
    for i in wsp:
        if dok == 0:
            pl.write('{:s}\t{:.0f}\t{:.0f}\t'.format(i[0], i[1], i[2]))
        elif dok == 1:
            pl.write('{:s}\t{:.1f}\t{:.1f}\t'.format(i[0], i[1], i[2]))
        elif dok == 2:
            pl.write('{:s}\t{:.2f}\t{:.2f}\t'.format(i[0], i[1], i[2]))
        elif dok == 3:
            pl.write('{:s}\t{:.3f}\t{:.3f}\t'.format(i[0], i[1], i[2]))
        elif dok == 4:
            pl.write('{:s}\t{:.4f}\t{:.4f}\t'.format(i[0], i[1], i[2]))
        elif dok == 5:
            pl.write('{:s}\t{:.5f}\t{:.5f}\t'.format(i[0], i[1], i[2]))
        elif dok == 6:
            pl.write('{:s}\t{:.6f}\t{:.6f}\t'.format(i[0], i[1], i[2]))

        if dok_bl == 0:
            pl.write('{:.0f}\t{:.0f}\t{:.0f}\n'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bl == 1:
            pl.write('{:.1f}\t{:.1f}\t{:.1f}\n'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bl == 2:
            pl.write('{:.2f}\t{:.2f}\t{:.2f}\n'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bl == 3:
            pl.write('{:.3f}\t{:.3f}\t{:.3f}\n'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bl == 4:
            pl.write('{:.4f}\t{:.4f}\t{:.4f}\n'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
    pl.close()

#Zapis macierzy kowariancji niewiadomych do pliku
def zapis_covx(sciezka, cov, opisA):
    pl = open(sciezka + '/COV_NIEWIADOME.txt', 'w+')
    pl.write('Macierz kowariancji dla wyrównanych współrzędnych [m]\n\n')
    for i in opisA:
        pl.write('{}\t'.format(i))
    wiersze, kolumny = np.shape(cov)
    pl.write('\n')
    for w in range(wiersze):
        for k in range(kolumny):
            pl.write('{:.12f}\t'.format(cov[w][k]))
        pl.write('\n')

#Zapis macierzy kowariancji obserwacji do pliku
def zapis_covd(sciezka, cov, katy, dlugosci, azymuty):
    pl = open(sciezka + '/COV_OBSERWACJE.txt', 'w+')
    pl.write('Macierz kowariancji dla wyrównanych współrzędnych [m]\n\n')
    if len(katy) > 0:
        for i in katy:
            pl.write('kat({}-{}-{})\t'.format(i[0],i[1],i[2]))
    if len(dlugosci) > 0:
        for i in dlugosci:
            pl.write('dl({}-{})\t'.format(i[0],i[1]))
    if len(azymuty) > 0:
        for i in azymuty:
            pl.write('Az({}-{})\t'.format(i[0],i[1]))
    wiersze, kolumny = np.shape(cov)
    pl.write('\n')
    for w in range(wiersze):
        for k in range(kolumny):
            pl.write('{:.12f}\t'.format(cov[w][k]))
        pl.write('\n')

#Zapis raportu do pliku tekstowego
def zapis_raportu(sciezka, wsp, dok, dok_bledow, metoda,
                  proces_iteracyjny,dlugosci,v_dlugosci,m_dlugosci,katy,v_katy,m_katy,azymuty,
                  v_azymuty,m_azymuty,mda,mdb,mk,ma,teraz):
    pl = open(sciezka + '/RAPORT_OBLICZEN.txt', 'w+')
    pl.write('<>' * 39)
    pl.write('\n')
    pl.write('{:^78}\n'.format('Loża Szyderców and Company'))
    pl.write('{:^78}\n'.format('PRZEDSTAWIA'))
    pl.write('{:^78}\n'.format('Wyrównanie sieci poziomej metodą najmniejszych kwadratów'))
    pl.write('Wykonali:\nDamian Ozga\nKamil Olko\nMaria Słowiak\n')
    pl.write('{:^78}\n'.format('AGH 2020'))
    pl.write('<>' * 39)
    pl.write('\n')
    pl.write('*' *78)
    pl.write('\n\n{:^78}\n'.format('RAPORT OBLICZEŃ'))
    if metoda == 'MNK':
        pl.write('{:^78}\n\n'.format('KLASYCZNE WYRÓWNANIE ŚCISŁE'))
    else:
        pl.write('{:^78}\n\n'.format('WYRÓWNANIE SWOBODNE'))
    pl.write('*' * 78 )
    pl.write('\n{:^78}\n'.format('Współrzędne wyrównane'))
    pl.write('*' * 78)
    #Zapis współrzędnych wyrównanych
    pl.write('\n\n{:<6s}\t{:<15s}\t{:<15s}\t{:<10s}\t{:<10s}\t{:<10s}\t\n'.format('Nr', 'X[m]', 'Y[m]', 'mx[mm]',
                                                                              'my[mm]', 'mp[mm]'))
    for i in wsp:
        if dok == 0:
            pl.write('{:<6s}\t{:<15.0f}\t{:<15.0f}\t'.format(i[0], i[1], i[2]))
        elif dok == 1:
            pl.write('{:<6s}\t{:<15.1f}\t{:<15.1f}\t'.format(i[0], i[1], i[2]))
        elif dok == 2:
            pl.write('{:<6s}\t{:<15.2f}\t{:<15.2f}\t'.format(i[0], i[1], i[2]))
        elif dok == 3:
            pl.write('{:<6s}\t{:<15.3f}\t{:<15.3f}\t'.format(i[0], i[1], i[2]))
        elif dok == 4:
            pl.write('{:<6s}\t{:<15.4f}\t{:<15.4f}\t'.format(i[0], i[1], i[2]))
        elif dok == 5:
            pl.write('{:<6s}\t{:<15.5f}\t{:<15.5f}\t'.format(i[0], i[1], i[2]))
        elif dok == 6:
            pl.write('{:<6s}\t{:<15.6f}\t{:<15.6f}\t'.format(i[0], i[1], i[2]))

        if dok_bledow == 0:
            pl.write('{:<10.0f}\t{:<10.0f}\t{:<10.0f}\n'.format(i[3] * 1000,i[4] * 1000, i[5] * 1000))
        elif dok_bledow == 1:
            pl.write('{:<10.1f}\t{:<10.1f}\t{:<10.1f}\n'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bledow == 2:
            pl.write('{:<10.2f}\t{:<10.2f}\t{:<10.2f}\n'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bledow == 3:
            pl.write('{:<10.3f}\t{:<10.3f}\t{:<10.3f}\n'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bledow == 4:
            pl.write('{:<10.4f}\t{:<10.4f}\t{:<10.4f}\n'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
    pl.write('\n')
    pl.write('*' * 78)
    #Zapis elips bledu do pliku
    pl.write('\n{:^78}\n'.format('Elipsy błędu '))
    pl.write('*' * 78)
    pl.write('\n\n{:<6s}\t{:<15s}\t{:<15s}\t{:<11s}\t{:<11s}\t{:<10s}\t\n'.format('Nr', 'X[m]', 'Y[m]', 'A[mm]',
                                                                                  'B[mm]', 'Azymut [g]'))
    for i in wsp:
        if dok == 0:
            pl.write('{:<6s}\t{:<15.0f}\t{:<15.0f}\t'.format(i[0], i[1], i[2]))
        elif dok == 1:
            pl.write('{:<6s}\t{:<15.1f}\t{:<15.1f}\t'.format(i[0], i[1], i[2]))
        elif dok == 2:
            pl.write('{:<6s}\t{:<15.2f}\t{:<15.2f}\t'.format(i[0], i[1], i[2]))
        elif dok == 3:
            pl.write('{:<6s}\t{:<15.3f}\t{:<15.3f}\t'.format(i[0], i[1], i[2]))
        elif dok == 4:
            pl.write('{:<6s}\t{:<15.4f}\t{:<15.4f}\t'.format(i[0], i[1], i[2]))
        elif dok == 5:
            pl.write('{:<6s}\t{:<15.5f}\t{:<15.5f}\t'.format(i[0], i[1], i[2]))
        elif dok == 6:
            pl.write('{:<6s}\t{:<15.6f}\t{:<15.6f}\t'.format(i[0], i[1], i[2]))

        if dok_bledow == 0:
            pl.write('{:<11.0f}\t{:<11.0f}\t{:<10.4f}\n'.format(i[6] * 1000, i[7] * 1000, i[8]))
        elif dok_bledow == 1:
            pl.write('{:<11.1f}\t{:<11.1f}\t{:<10.4f}\n'.format(i[6] * 1000, i[7] * 1000, i[8]))
        elif dok_bledow == 2:
            pl.write('{:<11.2f}\t{:<11.2f}\t{:<10.4f}\n'.format(i[6] * 1000, i[7] * 1000, i[8]))
        elif dok_bledow == 3:
            pl.write('{:<11.3f}\t{:<11.3f}\t{:<10.4f}\n'.format(i[6] * 1000, i[7] * 1000, i[8]))
        elif dok_bledow == 4:
            pl.write('{:<11.4f}\t{:<11.4f}\t{:<10.4f}\n'.format(i[6] * 1000, i[7] * 1000, i[8]))
    pl.write('\n')
    pl.write('*' * 78)
    #Zapis charakterystyki procesu iteracyjnego
    pl.write('\n{:^78}\n'.format('CHARAKTERYSTYKA PROCESU ITERACYJNEGO'))
    pl.write('*' * 78)
    pl.write('\n\n')
    pl.write('m0 = {:<10.5f}\n\n'.format(proces_iteracyjny[-1][4]))
    for i in proces_iteracyjny:
        pl.write('Iteracja {} dx_sr = {:<10.5f} dx_max = {:<10.5f} '
              'pvv = {:<10.5f} m0 = {:<10.5f}\n'.format(i[0], i[1], i[2], i[3],i[4]))
    pl.write('\n')
    pl.write('*' * 78)
    #Zapis obserwacji wyrównanych
    pl.write('\n{:^78}\n'.format('OBSERWACJE WYRÓWNANE'))
    pl.write('*' * 78)
    pl.write('\n\n')
    #Zapis długości
    if len(dlugosci) > 0:
        pl.write('ODLEGŁOŚCI\n')
        pl.write('{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t'
                 '{:<10s}\t\n'.format('Początek', 'Koniec', 'Odleg pom','Odleg wyr', 'v[mm]', 'mv[mm]', 'v/mv'))
        for i, ind in enumerate(dlugosci):
            if dok == 0:
                pl.write('{:<10s}\t{:<10s}\t{:<10.0f}\t{:<10.0f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]))
            elif dok == 1:
                pl.write('{:<10s}\t{:<10s}\t{:<10.1f}\t{:<10.1f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]))
            elif dok == 2:
                pl.write('{:<10s}\t{:<10s}\t{:<10.2f}\t{:<10.2f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]))
            elif dok == 3:
                pl.write('{:<10s}\t{:<10s}\t{:<10.3f}\t{:<10.3f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]))
            elif dok == 4:
                pl.write('{:<10s}\t{:<10s}\t{:<10.4f}\t{:<10.4f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]))
            elif dok == 5:
                pl.write('{:<10s}\t{:<10s}\t{:<10.5f}\t{:<10.5f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]))
            elif dok == 6:
                pl.write('{:<10s}\t{:<10s}\t{:<10.6f}\t{:<10.6f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]))
            if dok_bledow == 0:
                pl.write('{:<10.0f}\t{:<10.0f}\t{:<10.0f}\t\n'.format(
                    v_dlugosci[i] * 1000, m_dlugosci[i] * 1000, np.abs(v_dlugosci[i] / m_dlugosci[i])))
            elif dok_bledow == 1:
                pl.write('{:<10.1f}\t{:<10.1f}\t{:<10.1f}\t\n'.format(
                    v_dlugosci[i]*1000,m_dlugosci[i]*1000,np.abs(v_dlugosci[i]/m_dlugosci[i])))
            elif dok_bledow == 2:
                pl.write('{:<10.2f}\t{:<10.2f}\t{:<10.2f}\t\n'.format(
                    v_dlugosci[i] * 1000, m_dlugosci[i] * 1000, np.abs(v_dlugosci[i] / m_dlugosci[i])))
            elif dok_bledow == 3:
                pl.write('{:<10.3f}\t{:<10.3f}\t{:<10.3f}\t\n'.format(
                    v_dlugosci[i] * 1000, m_dlugosci[i] * 1000, np.abs(v_dlugosci[i] / m_dlugosci[i])))
            elif dok_bledow == 4:
                pl.write('{:<10.4f}\t{:<10.4f}\t{:<10.4f}\t\n'.format(
                    v_dlugosci[i] * 1000, m_dlugosci[i] * 1000, np.abs(v_dlugosci[i] / m_dlugosci[i])))
    #Zapis katów
    pl.write('\nKĄTY\n')
    pl.write('{:<6s}\t{:<6s}\t{:<6s}\t{:<10s}\t{:<10s}\t{:<10s}\t'
             '{:<10s}\t{:<10s}\t\n'.format('L', 'C', 'P', 'Kąt pom', 'Kąt wyr', 'v[cc]', 'mv[cc]', 'v/mv'))
    for i, ind in enumerate(katy):
        pl.write('{:<6s}\t{:<6s}\t{:<6s}\t{:<10.5f}\t{:<10.5f}\t'.format(ind[0], ind[1],
                                                                                   ind[2], ind[3], ind[3] + v_katy[i]))
        if dok_bledow == 0:
            pl.write('{:<10.0f}\t{:<10.0f}\t{:<10.0f}\t\n'.format(v_katy[i] * 10000,
                                                                      m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))
        elif dok_bledow == 1:
            pl.write('{:<10.1f}\t{:<10.1f}\t{:<10.1f}\t\n'.format(v_katy[i] * 10000,
                                                                      m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))
        elif dok_bledow == 2:
            pl.write('{:<10.2f}\t{:<10.2f}\t{:<10.2f}\t\n'.format(v_katy[i] * 10000,
                                                                      m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))
        elif dok_bledow == 3:
            pl.write('{:<10.3f}\t{:<10.3f}\t{:<10.3f}\t\n'.format(v_katy[i] * 10000,
                                                                      m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))
        elif dok_bledow == 4:
            pl.write('{:<10.4f}\t{:<10.4f}\t{:<10.4f}\t\n'.format(v_katy[i] * 10000,
                                                                      m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))
    # Zapis azymutów
    if len(azymuty) > 0:
        pl.write('\nAZYMUTY\n')
        pl.write('{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t'
              '{:<10s}\t{:<10s}\t\n'.format('Początek', 'Koniec', 'Az pom', 'Az wyr', 'v[cc]', 'mv[cc]', 'v/mv'))
        for i, ind in enumerate(azymuty):
            pl.write('{:<10s}\t{:<10s}\t{:<10.5f}\t{:<10.5f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_azymuty[i]))
            if dok_bledow == 0:
                pl.write('{:<10.0f}\t{:<10.0f}\t{:<10.0f}\t\n'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                                 np.abs(v_azymuty[i] / m_azymuty[i])))
            elif dok_bledow == 1:
                pl.write('{:<10.1f}\t{:<10.1f}\t{:<10.1f}\t\n'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                                 np.abs(v_azymuty[i] / m_azymuty[i])))
            elif dok_bledow == 2:
                pl.write('{:<10.2f}\t{:<10.2f}\t{:<10.2f}\t\n'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                                 np.abs(v_azymuty[i] / m_azymuty[i])))
            elif dok_bledow == 3:
                pl.write('{:<10.3f}\t{:<10.3f}\t{:<10.3f}\t\n'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                                 np.abs(v_azymuty[i] / m_azymuty[i])))
            elif dok_bledow == 4:
                pl.write('{:<10.4f}\t{:<10.4f}\t{:<10.4f}\t\n'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                             np.abs(v_azymuty[i] / m_azymuty[i])))
    #Zapis błędów apriori
    pl.write('\n')
    pl.write('*' * 78)
    pl.write('\n{:^78}\n'.format('PRZYJĘTE BŁĘDY A PRIORI'))
    pl.write('*' * 78)
    pl.write('\n\n')
    if dok_bledow == 0:
        pl.write('Błąd pomiaru odległość = {:<.0f} [mm] + {:<.0f} [ppm]\n'.format(mda * 1000, mdb * 1000))
        pl.write('Błąd pomiaru kąta = {:<.0f} [cc]\n'.format(mk * 10000))
        pl.write('Błąd pomiaru azymutów = {:<.0f} [cc]\n'.format(ma * 10000))
    elif dok_bledow == 1:
        pl.write('Błąd pomiaru odległość = {:<.1f} [mm] + {:<.1f} [ppm]\n'.format(mda * 1000, mdb * 1000))
        pl.write('Błąd pomiaru kąta = {:<.1f} [cc]\n'.format(mk * 10000))
        pl.write('Błąd pomiaru azymutów = {:<.1f} [cc]\n'.format(ma * 10000))
    elif dok_bledow == 2:
        pl.write('Błąd pomiaru odległość = {:<.2f} [mm] + {:<.2f} [ppm]\n'.format(mda * 1000, mdb * 1000))
        pl.write('Błąd pomiaru kąta = {:<.2f} [cc]\n'.format(mk * 10000))
        pl.write('Błąd pomiaru azymutów = {:<.2f} [cc]\n'.format(ma * 10000))
    elif dok_bledow == 3:
        pl.write('Błąd pomiaru odległość = {:<.3f} [mm] + {:<.3f} [ppm]\n'.format(mda * 1000, mdb * 1000))
        pl.write('Błąd pomiaru kąta = {:<.3f} [cc]\n'.format(mk * 10000))
        pl.write('Błąd pomiaru azymutów = {:<.3f} [cc]\n'.format(ma * 10000))
    elif dok_bledow == 4:
        pl.write('Błąd pomiaru odległość = {:<.4f} [mm] + {:<.4f} [ppm]\n'.format(mda * 1000, mdb * 1000))
        pl.write('Błąd pomiaru kąta = {:<.4f} [cc]\n'.format(mk * 10000))
        pl.write('Błąd pomiaru azymutów = {:<.4f} [cc]\n'.format(ma * 10000))
    pl.write('\n')
    pl.write('*' * 78)
    #Stopka programu
    pl.write('\n')
    pl.write('<>' * 39)
    pl.write('')
    pl.write('\n\n{:>78s}'.format('Obliczył........................'))
    pl.write('')
    pl.write('\n\n{:22}Data wykonania {:02}.{:02}.{:04} {:02}:{:02}:{:02}\n'.format(' ', teraz.day,
                                                                           teraz.month, teraz.year, teraz.hour,
                                                                           teraz.minute, teraz.second))
    pl.write('<>' * 39)
    