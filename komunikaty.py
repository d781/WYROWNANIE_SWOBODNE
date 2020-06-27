from funkcje import *
import os

def printt(lista):
    for i in lista:
        print(i)

#Wyświetlanie punktów
def wyswietlanie_pkt(wsp,dok):
    print('*' * 78)
    print('{:<6s} {:<10s} {:<10s} {:<10s}'.format('Numer', 'X', 'Y', 'Nawiązanie'))
    for i in wsp:
        if i[3] == 1:
            st = 'brak'
        elif i[3] == 0:
            st = '2D'
        if dok == 0:
            print('{:<6s} {:<10.0f} {:<10.0f} {:<10s}'.format(i[0], i[1], i[2], st))
        elif dok == 1:
            print('{:<6s} {:<10.1f} {:<10.1f} {:<10s}'.format(i[0], i[1], i[2], st))
        elif dok == 2:
            print('{:<6s} {:<10.2f} {:<10.2f} {:<10s}'.format(i[0], i[1], i[2], st))
        elif dok == 3:
            print('{:<6s} {:<10.3f} {:<10.3f} {:<10s}'.format(i[0], i[1], i[2], st))
        elif dok == 4:
            print('{:<6s} {:<10.4f} {:<10.4f} {:<10s}'.format(i[0], i[1], i[2], st))
        elif dok == 5:
            print('{:<6s} {:<10.5f} {:<10.5f} {:<10s}'.format(i[0], i[1], i[2], st))

#Wybór punktów stałych
def stale(wsp,dok):
    while True:
        os.system("cls")
        print('')
        wyswietlanie_pkt(wsp,dok)
        nazwa = str(input('Aby wybrać punkt wpisz numer, aby wyjść wpisz X: '))
        if nazwa == 'x' or nazwa == 'X':
            break
        else:
            tmp = szukaj(nazwa,wsp)
            if tmp =='brak':
                print('Brak punktu o takim numerze')
            else:
                zmienna = (input('Wybrano punkt {} aby ustawić go jako stały wpisz T: '.format(tmp[0])).upper())
                if zmienna == 'T':
                    tmp[3] = 0
                else:
                    tmp[3] = 1
    return wsp

#Ustalenie dokładności
def dokladnosc(dok, dok_bledow):
    while True:
        print('Aktualna dokadność współrzędnych [m]: {}'.format(dok))
        print('Aktualna dokadność błędów [mm]: {}'.format(dok_bledow))
        print('1.Zmiana dokładności')
        print('2.Powrót')
        tt = int(input('Wybierz opcję: '))
        if tt == 1:
            os.system("cls")
            while True:
                dok = int(input('Podaj dokładność współrzędnych w [m] od 0 do 6 miejsc po przecinku: '))
                if dok>=0 and dok <=6:
                    break
            while True:
                dok_bledow = int(input('Podaj dokładność błędów w [mm] od 0 do 4 miejsc po przecinku: '))
                if  dok_bledow>=0 and dok_bledow <=4:
                    break
        elif tt == 2:
            break
    return dok , dok_bledow

#Ustalenie błędów obserwacji
def apriori(mk, mda, mdb, ma):
    while True:
        print('')
        print('*' * 78)
        print('Aktualna błędy apriori:\nBłąd kąta = {:.6f} [grad]\nBłąd długości:\na = {:.5f} [m]'
              '\nb = {:.5f} [m\km]\nBłąd azymutu = {:.6f} [grad] '.format(mk,mda,mdb,ma))
        print('_' * 78)
        print('1.Zmiana błędu kąta')
        print('2.Zmiana błędu długości')
        print('3.Zmiana błędu azymutu')
        print('4.Powrót')
        print('*' * 78)

        tt = int(input('Wybierz opcję: '))
        if tt == 1:
            os.system("cls")
            mk = float(input('Podaj błąd kąta [grad]: '))
        elif tt == 2:
            os.system("cls")
            mda = float(input('Podaj błąd długości a [m]: '))
            mdb = float(input('Podaj błąd długości b [m/km]: '))
        elif tt == 3:
            os.system("cls")
            ma = float(input('Podaj błąd azymutu [grad]: '))
        elif tt == 4:
            break
    return mk, mda, mdb, ma

#Ustalenie danych wejsciowych
def wejscie(dane, WS):
    while   True:
        print('')
        print('*' * 78)
        print('1.Folder z danymi wejściowymi: {}'.format(dane[4]))
        print('2.Folder z danymi wyjściowymi: {}'.format(dane[5]))
        print('3.Wczytywanie odległości( T / N ): {}\n\t Nazwa pliku z odległościami: {}'.format(dane[0][0], dane[0][1]))
        print('4.Wczytywanie katów( T / N ): {}\n\t Nazwa pliku z kątami: {}'.format(dane[1][0], dane[1][1]))
        print('5.Wczytywanie kierunków( T / N ): {}\n\t Nazwa pliku z kierunkami: {}'.format(dane[2][0], dane[2][1]))
        print('6.Wczytywanie azymutów( T / N ): {}\n\t Nazwa pliku z azymutami: {}'.format(dane[3][0], dane[3][1]))
        print('7.Nazwa pliku z współrzędnymi przybliżonymi: {}'.format(dane[6]))
        print('8.Powrót')
        print('*' * 78)
        t = int(input('Wybierz opcje: '))
        if t == 1:
            os.system("cls")
            print('Jeżeli dane wejsciowe znajdują się w folderze głównym scieżkę należy zostawić pustą.')
            dane[4] = input('Ścieżka folderu z danymi wejsciowymi: ')
        elif t == 2:
            os.system("cls")
            print('Jeżeli dane wyjściowe mają znajdywaćsię w folderze głównym scieżkę należy zostawić pustą.')
            dane[5] = input('Ścieżka folderu z danymi wyjściowymi: ')
        elif t == 3:
            os.system("cls")

            dane[0][0] = input('Wczytywać odległości( T / N ): ').upper()
            dane[0][1] = input('Nazwa pliku z odległościami: ')
        elif t == 4:
            os.system("cls")
            dane[1][0] = input('Wczytywać kątów( T / N ): ').upper()
            dane[1][1] = input('Nazwa pliku z kątami: ')
        elif t == 5:
            os.system("cls")
            dane[2][0] = input('Wczytywać kierunków( T / N ): ').upper()
            dane[2][1] = input('Nazwa pliku z kierunkami: ')
        elif t == 6:
            os.system("cls")
            dane[2][0] = input('Wczytywać azymuty( T / N ): ').upper()
            dane[2][1] = input('Nazwa pliku z azymutami: ')
        elif t == 7:
            dane[6] = input('Nazwa pliku z współrzędnymi przybliżonymi: ')
            os.system("cls")
            try:
                WS = wczytaj(dane[4] + '/' + dane[6])
                for i in WS:
                    i[1] = float(i[1])
                    i[2] = float(i[2])
                    if len(i) < 4:
                        i.append(1)
                    else:
                        i[3] = int(i[3])
            except:
                    print('Brak pliku o takiej nazwie lub ścieżce dostępu')
        elif t == 8:
            break
    return dane, WS

#Komunikat główny
def komunikat_glowny(mk,mda,mdb,ma,dok, dok_bledow, dane, WS):
    while True:
        os.system("cls")
        print('*'*78)
        print('1.Ustalenie błędów bserwacji')
        print('2.Wybór punktów nawiązania')
        print('3.Wybór dokładności')
        print('4.Wyrównanie MNK')
        print('5.Wyrównanie swobodne')
        print('6.Dane wejsciowe')
        print('7.Wyjście')
        print('*' * 78)
        t = int(input('Uruchom opcje: '))

        if t == 1:
            os.system("cls")
            mk,mda,mdb,ma = apriori(mk, mda, mdb, ma)
        elif t == 2:
            os.system("cls")
            WS = stale(WS, dok)
        elif t == 3:
            os.system("cls")
            dok, dok_bledow = dokladnosc(dok, dok_bledow)
        elif t == 4:
            os.system("cls")
            wyrownanie = 'MNK'
            break
        elif t == 5:
            os.system("cls")
            wyrownanie = 'swobodne'
            break
        elif t == 6:
            os.system("cls")
            dane, WS = wejscie(dane, WS)
        elif t == 7:
            break
    return wyrownanie, dok, dok_bledow, mk, mda, mdb, ma, dane, WS

#Nagłówek programu
def naglowek():
    print('<>' * 39)
    print('{:^78}'.format('Loża Szyderców and Company'))
    print('{:^78}'.format('PRZEDSTAWIA'))
    print('{:^78}'.format('Wyrównanie sieci poziomej metodą najmniejszych kwadratów'))
    print('Wykonali:\ninż. Damian Ozga\ninż. Kamil Olko\ninż. Maria Słowiak')
    print('{:^78}'.format('AGH 2020'))
    print('<>' * 39)
    print('')

#Stopka programu
def stopka(teraz):

    print('')
    print('<>' * 39)
    print('')
    print('{:>78s}'.format('Obliczył........................'))
    print('')
    print('{:22}Data wykonania {:02}.{:02}.{:04} {:02}:{:02}:{:02}'.format(' ',teraz.day,
                                                teraz.month,teraz.year, teraz.hour, teraz.minute, teraz.second ))
    print('<>' * 39)

#Wyświetlanie raportu z procesu iteracyjnego
def wyswietlanie_proces(proces_iteracyjny):
    print('\n{:^78}'.format('CHARAKTERYSTYKA PROCESU ITERACYJNEGO'))
    for i in proces_iteracyjny:
        print('Iteracja {} dx_sr = {:<10.5f} dx_max = {:<10.5f} '
              'pvv = {:<10.5f} m0 = {:<10.5f}'.format(i[0], i[1], i[2], i[3],i[4]))

#Wyświetlanie raportu współrzędnych
def wyswietlanie_wsp(wsp,dok,dok_bledow):
    print('\n{:^78}'.format('WSPÓŁRZĘDNE WYRÓWNANE'))
    print('{:<6s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t'.format('Nr', 'X', 'Y','mx[mm]', 'my[mm]', 'mp[mm]'))
    for i in wsp:
        if dok == 0:
            print('{:<6s}\t{:<10.0f}\t{:<10.0f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 1:
            print('{:<6s}\t{:<10.1f}\t{:<10.1f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 2:
            print('{:<6s}\t{:<10.2f}\t{:<10.2f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 3:
            print('{:<6s}\t{:<10.3f}\t{:<10.3f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 4:
            print('{:<6s}\t{:<10.4f}\t{:<10.4f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 5:
            print('{:<6s}\t{:<10.5f}\t{:<10.5f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 6:
            print('{:<6s}\t{:<10.6f}\t{:<10.6f}\t'.format(i[0], i[1], i[2]), end='')

        if dok_bledow == 0:
            print('{:<10.0f}\t{:<10.0f}\t{:<10.0f}'.format(i[3] * 1000,i[4] * 1000, i[5] * 1000))
        elif dok_bledow == 1:
            print('{:<10.1f}\t{:<10.1f}\t{:<10.1f}'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bledow == 2:
            print('{:<10.2f}\t{:<10.2f}\t{:<10.2f}'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bledow == 3:
            print('{:<10.3f}\t{:<10.3f}\t{:<10.3f}'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
        elif dok_bledow == 4:
            print('{:<10.4f}\t{:<10.4f}\t{:<10.4f}'.format(i[3] * 1000, i[4] * 1000, i[5] * 1000))
#Wyświetlanie parametrów elips błędów
def wyswietlanie_elips(wsp,dok,dok_bledow):
    print('\n{:^78}'.format('ELIPSY BŁĘDU'))
    print('{:<6s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t'.format('Nr', 'X[m]', 'Y[m]', 'A[mm]',
                                                                                  'B[mm]', 'Azymut [g]'))
    for i in wsp:
        if dok == 0:
            print('{:<6s}\t{:<10.0f}\t{:<10.0f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 1:
            print('{:<6s}\t{:<10.1f}\t{:<10.1f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 2:
            print('{:<6s}\t{:<10.2f}\t{:<10.2f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 3:
            print('{:<6s}\t{:<10.3f}\t{:<10.3f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 4:
            print('{:<6s}\t{:<10.4f}\t{:<10.4f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 5:
            print('{:<6s}\t{:<10.5f}\t{:<10.5f}\t'.format(i[0], i[1], i[2]), end='')
        elif dok == 6:
            print('{:<6s}\t{:<10.6f}\t{:<10.6f}\t'.format(i[0], i[1], i[2]), end='')

        if dok_bledow == 0:
            print('{:<11.0f}\t{:<11.0f}\t{:<10.4f}'.format(i[6] * 1000, i[7] * 1000, i[8]))
        elif dok_bledow == 1:
            print('{:<11.1f}\t{:<11.1f}\t{:<10.4f}'.format(i[6] * 1000, i[7] * 1000, i[8]))
        elif dok_bledow == 2:
            print('{:<11.2f}\t{:<11.2f}\t{:<10.4f}'.format(i[6] * 1000, i[7] * 1000, i[8]))
        elif dok_bledow == 3:
            print('{:<11.3f}\t{:<11.3f}\t{:<10.4f}'.format(i[6] * 1000, i[7] * 1000, i[8]))
        elif dok_bledow == 4:
            print('{:<11.4f}\t{:<11.4f}\t{:<10.4f}'.format(i[6] * 1000, i[7] * 1000, i[8]))

#Wyświetlanie raportu z wyrównanych odległości
def wyswietlanie_dlugosci(dlugosci,v_dlugosci,m_dlugosci,dok,dok_bledow):
    if len(dlugosci) > 0:
        print('Odległości')
        print('{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t'.format('Początek', 'Koniec', 'Odleg pom',
                                                                                'Odleg wyr', 'v[mm]', 'mv[mm]', 'v/mv'))
        for i, ind in enumerate(dlugosci):
            if dok == 0:
                print('{:<10s}\t{:<10s}\t{:<10.0f}\t{:<10.0f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]),
                      end='')
            elif dok == 1:
                print('{:<10s}\t{:<10s}\t{:<10.1f}\t{:<10.1f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]),
                      end='')
            elif dok == 2:
                print('{:<10s}\t{:<10s}\t{:<10.2f}\t{:<10.2f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]),
                      end='')
            elif dok == 3:
                print('{:<10s}\t{:<10s}\t{:<10.3f}\t{:<10.3f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]),
                      end='')
            elif dok == 4:
                print('{:<10s}\t{:<10s}\t{:<10.4f}\t{:<10.4f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]),
                      end='')
            elif dok == 5:
                print('{:<10s}\t{:<10s}\t{:<10.5f}\t{:<10.5f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]),
                      end='')
            elif dok == 6:
                print('{:<10s}\t{:<10s}\t{:<10.6f}\t{:<10.6f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_dlugosci[i]),
                      end='')
            if dok_bledow == 0:
                print('{:<10.0f}\t{:<10.0f}\t{:<10.0f}\t'.format(
                    v_dlugosci[i] * 1000, m_dlugosci[i] * 1000, np.abs(v_dlugosci[i] / m_dlugosci[i])))
            elif dok_bledow == 1:
                print('{:<10.1f}\t{:<10.1f}\t{:<10.1f}\t'.format(
                    v_dlugosci[i]*1000,m_dlugosci[i]*1000,np.abs(v_dlugosci[i]/m_dlugosci[i])))
            elif dok_bledow == 2:
                print('{:<10.2f}\t{:<10.2f}\t{:<10.2f}\t'.format(
                    v_dlugosci[i] * 1000, m_dlugosci[i] * 1000, np.abs(v_dlugosci[i] / m_dlugosci[i])))
            elif dok_bledow == 3:
                print('{:<10.3f}\t{:<10.3f}\t{:<10.3f}\t'.format(
                    v_dlugosci[i] * 1000, m_dlugosci[i] * 1000, np.abs(v_dlugosci[i] / m_dlugosci[i])))
            elif dok_bledow == 4:
                print('{:<10.4f}\t{:<10.4f}\t{:<10.4f}\t'.format(
                    v_dlugosci[i] * 1000, m_dlugosci[i] * 1000, np.abs(v_dlugosci[i] / m_dlugosci[i])))

#Wyświetlanie raportu z wyrównanych katów
def wyswietlanie_katy(katy,v_katy,m_katy,dok_bledow):
    if len(katy) > 0:
        print('Kąty')
        print('{:<6s}\t{:<6s}\t{:<6s}\t{:<10s}\t{:<10s}\t{:<10s}\t'
              '{:<10s}\t{:<10s}\t'.format('L', 'C', 'P', 'Kąt pom', 'Kąt wyr', 'v[cc]', 'mv[cc]', 'v/mv'))
        for i, ind in enumerate(katy):
            print('{:<6s}\t{:<6s}\t{:<6s}\t{:<10.5f}\t{:<10.5f}\t'.format(ind[0], ind[1],
                                                                             ind[2], ind[3], ind[3] + v_katy[i]),end='')
            if dok_bledow == 0:
                print('{:<10.0f}\t{:<10.0f}\t{:<10.0f}\t'.format(v_katy[i] * 10000,
                                                                 m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))
            elif dok_bledow == 1:
                print('{:<10.1f}\t{:<10.1f}\t{:<10.1f}\t'.format(v_katy[i] * 10000,
                                                                 m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))
            elif dok_bledow == 2:
                print('{:<10.2f}\t{:<10.2f}\t{:<10.2f}\t'.format(v_katy[i] * 10000,
                                                                 m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))
            elif dok_bledow == 3:
                print('{:<10.3f}\t{:<10.3f}\t{:<10.3f}\t'.format(v_katy[i] * 10000,
                                                                 m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))
            elif dok_bledow == 4:
                print('{:<10.4f}\t{:<10.4f}\t{:<10.4f}\t'.format(v_katy[i] * 10000,
                                                                 m_katy[i] * 10000, np.abs(v_katy[i] / m_katy[i])))

#Wyświetlanie raportu z wyrównanych katów
def wyswietlanie_azymuty(azymuty,v_azymuty,m_azymuty,dok_bledow):
    if len(azymuty) > 0:
        print('Azymuty')
        print('{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}\t'
              '{:<10s}\t{:<10s}\t'.format('Początek', 'Koniec', 'Az pom', 'Az wyr', 'v[cc]', 'mv[cc]', 'v/mv'))
        for i, ind in enumerate(azymuty):
            print('{:<10s}\t{:<10s}\t{:<10.5f}\t{:<10.5f}\t'.format(ind[0], ind[1], ind[2], ind[2] + v_azymuty[i]),end='')
            if dok_bledow == 0:
                print('{:<10.0f}\t{:<10.0f}\t{:<10.0f}\t'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                                 np.abs(v_azymuty[i] / m_azymuty[i])))
            elif dok_bledow == 1:
                print('{:<10.1f}\t{:<10.1f}\t{:<10.1f}\t'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                                 np.abs(v_azymuty[i] / m_azymuty[i])))
            elif dok_bledow == 2:
                print('{:<10.2f}\t{:<10.2f}\t{:<10.2f}\t'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                                 np.abs(v_azymuty[i] / m_azymuty[i])))
            elif dok_bledow == 3:
                print('{:<10.3f}\t{:<10.3f}\t{:<10.3f}\t'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                                 np.abs(v_azymuty[i] / m_azymuty[i])))
            elif dok_bledow == 4:
                print('{:<10.4f}\t{:<10.4f}\t{:<10.4f}\t'.format(v_azymuty[i] * 10000, m_azymuty[i] * 10000,
                                                             np.abs(v_azymuty[i] / m_azymuty[i])))