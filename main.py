from funkcje import *
from komunikaty import *
import copy
import datetime
if __name__ == '__main__':
    mk = 0.0012
    mda = 0.000001
    mdb = 0.00000
    ma = 0.000001
    dok = 5
    dok_bledow = 2
    dlugosci = []
    katy = []
    kierunki = []
    azymuty = []
    WS = []
    wyrownanie = 'swobodne'
    dane = [['T', 'p1_d.txt'],
            ['N', 'katy.txt'],
            ['T', 'p1_ki.txt'],
            ['N', 'azymut.txt'],
            'p1',
            'dane_wyjsciowe',
            'p1_w.txt']
    #Wyświetlenie nagłówka programu
    naglowek()
    #Dostosowanie opcji programu
    wyrownanie, dok, dok_bledow, mk, mda, mdb, ma, dane, WS = komunikat_glowny(mk, mda,
                                                                          mdb, ma, dok, dok_bledow,dane, WS)
    #Wczytanie długości z pliku
    if dane[0][0] == 'T':
        sciezka_dl = dane[4] + '/' + dane[0][1]
        dlugosci = wczytaj(sciezka_dl)
        for i in dlugosci:
            i[2] = float(i[2])
    #Wczytanie katów z pliku
    if dane[1][0] == 'T':
        sciezka_katy = dane[4] + '/' + dane[1][1]

        katy = wczytaj(sciezka_katy)
        for i in katy:
            i[2] = float(i[3])
    #Wczytanie kierunków z pliku
    if dane[2][0] == 'T':
        sciezka_kier = dane[4] + '/' + dane[2][1]
        kierunki = wczytaj(sciezka_kier)
        for i in kierunki:
            i[2] = float(i[2])
    #Wczytanie azymuty z pliku
    if dane[3][0] == 'T':
        sciezka_az = dane[4] + '/' + dane[3][1]
        azymuty = wczytaj(sciezka_az)
        for i in azymuty:
            i[2] = float(i[2])

    #Wczytanie współrzędnych z pliku
    WS = wczytaj(dane[4] + '/' + dane[6])
    for i in WS:
        i[1] = float(i[1])
        i[2] = float(i[2])
        if len(i) < 4:
            i.append(1)
        else:
            i[3] = int(i[3])
    wsp = copy.deepcopy(WS)
    #Zamiana kierunków na kąty
    katy1 = kie2katy(kierunki)
    katy = katy + katy1

    #Obliczenie rozmiarów macierzy A
    liczba_obs = len(dlugosci) + len(katy) + len(azymuty)
    liczba_niew = 0
    for i in wsp:
        liczba_niew += i[3]
    liczba_niew = liczba_niew * 2
    dx_max = 1
    iteracje = 0
    proces_iteracyjny = []
    defekt = 0
    #Sprawdzenie defektu sieci
    if liczba_niew == len(wsp) * 2:
        defekt = 2
    if dlugosci == []:
        defekt += 1
    if azymuty == []:
        defekt += 1
    #Przebieg procesu iteracyjnego
    while dx_max > (10 ** -(dok + 2)):
        #Sprawdzenie warunków dla MNK
        if wyrownanie == 'MNK':
             if liczba_niew == len(wsp)*2:
                 print('Brak rozwiazania układu')
                 print('Brak punktów stałych')
                 break
             elif liczba_niew == len(wsp)*2 - 2 and ( azymuty == [] or dlugosci == [] ):
                 print('Brak rozwiazania układu')
                 if azymuty == []:
                    print('Brak azymutów ')
                 if dlugosci ==[]:
                    print('Brak długości')
                 break
        #Utworzenie opisu macierzy A
        opis_A = opisA(wsp)
        #Wyznaczenie par dla obserwacji
        par_kat, wol_kat = wspolczynniki_katy(katy, wsp)
        par_dl, wol_dl = wspolczynniki_dlugosci(dlugosci, wsp)
        par_az , wol_az = wspolczynniki_azymuty(azymuty, wsp)
        #Utworzenie macierzy A i L
        A = []
        L = wol_kat
        A = macierzA(A, par_kat, opis_A)
        A = macierzA(A, par_dl, opis_A)
        A = macierzA(A, par_az, opis_A)
        L += wol_dl
        L += wol_az
        A = np.array(A)
        L = np.array(L)
        #Utworzenie macierzy wagowej P
        P = np.zeros([liczba_obs, liczba_obs])
        p = []
        for i in katy:
            p.append(1/( mk ** 2 ))
        for i in dlugosci:
            md = mda + mdb * i[2] / 1000
            p.append(1 / (md ** 2))
        for i in azymuty:
            p.append(1 / (ma ** 2))
        for i, id in enumerate(p):
            P[i,i] = id
        #Rozwiązanie układu równan metodą najmniejszych kwadratów
        #Rozwiązanie klasycznego układu
        if wyrownanie == 'MNK':
            x = np.linalg.inv(A.T @ P @ A) @ A.T @ P @ L
            dx = np.sqrt(x ** 2)
            dx = np.sum(dx)
            dx_sr = np.mean(dx)
            dx_max = np.max(dx)
        #Rozwiązanie układu z defektem
        elif    wyrownanie == 'swobodne':
            x = np.linalg.pinv(A.T @ P @ A) @ A.T @ P @ L
            dx = np.sqrt(x ** 2)
            dx_sr = np.mean(dx)
            dx_max = np.max(dx)
        #Obliczenie współrzędnych wyrównanych
        for i, id in enumerate(opis_A):
            naz = id.split('_')[1]
            xy = id.split('_')[0]
            for nr in wsp:
                if naz == nr[0] and xy == 'dx':
                    nr[1] = nr[1] + x[i]
                elif naz == nr[0] and xy == 'dy':
                    nr[2] = nr[2] + x[i]

        #Parametry procesu wyrównania
        v = A @ x - L
        suV2 = v.T @ P @ v
        #Obliczenie błędu średniokwadratowego i macierzy kowarianci niewiadomych dla sieci bez defektu
        if defekt == 0:
            m02 = suV2 / ( liczba_obs - liczba_niew )
            m0 = np.sqrt(m02)
            covX = m02 * np.linalg.inv(A.T @ P @ A)
        #Obliczenie błędu średniokwadratowego i macierzy kowarianci niewiadomych dla sieci z defektem
        elif defekt > 0:
            m02 = suV2 / (liczba_obs - liczba_niew + defekt)
            m0 = np.sqrt(m02)
            covX = m02 * np.linalg.pinv(A.T @ P @ A)
        #Oblicze macierzy kowariancji dla obserwacji
        covOBS = A @ covX @ A.T
        mOBS = np.sqrt(np.diag(covOBS))
        mOBS = list(mOBS)
        iteracje += 1
        proces_iteracyjny.append([iteracje, dx_sr,dx_max, np.sqrt(suV2), m0])
        #Wyznaczenie poprawek i błędów dla poszczególnych rodzajów obserwacji
        vv = list(v)
        v_katy = vv[0:len(katy)]
        v_dlugosci = vv[len(katy):len(katy)+len(dlugosci)]
        v_azymuty = vv[len(katy) + len(dlugosci):]
        m_katy = mOBS[0:len(katy)]
        m_dlugosci = mOBS[len(katy):len(katy)+len(dlugosci)]
        m_azymuty = mOBS[len(katy) + len(dlugosci):]
    #Wyznaczenie błędów współrzędnych wyrównanych
    bledy_wsp = np.sqrt(np.diag(covX))
    #Przypisanie parametrów do zmiennych
    for i in wsp:
        i[3] = 0
        i.append(0)
        i.append(0)
    for i, id in enumerate(opis_A):
        naz = id.split('_')[1]
        xy = id.split('_')[0]
        for nr in wsp:
            if naz == nr[0] and xy == 'dx':
                nr[3] = bledy_wsp[i]
            elif naz == nr[0] and xy == 'dy':
                nr[4] = bledy_wsp[i]
    for i in wsp:
        i[5] = np.sqrt(i[3] ** 2 + i[4] ** 2 )
    #WYznaczenie elips błędu
    wsp = elipsy(wsp, opis_A , covX)
    #Sprawdzenie czy folder z wynikami istnieje i utworzenie go
    if os.path.exists(dane[5]) == False:
        os.mkdir(dane[5])
    sc = dane[4].split('/')[-1]
    if os.path.exists(dane[5] + '/' + sc) == False:
        os.mkdir(dane[5] + '/' + sc)
    sciezka_zap = dane[5] + '/' + sc
    #Zapis współrzędnych wyrównanych do pliku
    zapis_wsp(sciezka_zap,dok,dok_bledow,wsp)
    #Wyświetlanie raportu z obliczeń
    print('*'*78)
    print('{:^78}'.format('RAPORT OBLICZEŃ'))
    wyswietlanie_wsp(wsp,dok,dok_bledow)
    print('')
    wyswietlanie_elips(wsp,dok,dok_bledow)
    print('\n{:^78}'.format('OBSERWACJE WYRÓWNANIE'))
    wyswietlanie_dlugosci(dlugosci,v_dlugosci,m_dlugosci,dok,dok_bledow)
    print('')
    wyswietlanie_katy(katy,v_katy,m_katy,dok_bledow)
    print('')
    wyswietlanie_azymuty(azymuty,v_azymuty,m_azymuty,dok_bledow)
    print('')
    wyswietlanie_proces(proces_iteracyjny)
    #Wyświetlenie stopki programu
    teraz = datetime.datetime.now()
    stopka(teraz)
    #Zapis wyników do pliku
    zapis_covx(sciezka_zap, covX, opis_A)
    zapis_covd(sciezka_zap, covOBS,katy, dlugosci, azymuty )
    zapis_raportu(sciezka_zap, wsp, dok, dok_bledow, wyrownanie, proces_iteracyjny, dlugosci,
                  v_dlugosci,m_dlugosci,katy,v_katy,m_katy,azymuty,v_azymuty,m_azymuty,mda,mdb,mk,ma,teraz)
    #Opracowali:
    #inż. Damian Ozga
    #inż. Kamil Olko
    #inż. Maria Słowiak