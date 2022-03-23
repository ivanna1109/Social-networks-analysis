import networkx as nx
from os import path
import os

from implementacija.ucitavanje_grafa import ucitaj_jednostavan_graf, ucitaj_rucno_graf, \
    ucitaj_neklasterabilan, ucitaj_epinions, ucitaj_wiki, ucitaj_slashdot

from implementacija.detektovanje_klastera import detektovanje_klastera, \
    napravi_klastere, detektovanje_koalicija, detekcija_losih_veza, napravi_mrezu_klastera

from implementacija.nacrtaj_graf import nacrtaj_mali, nacrtaj_veliki

from implementacija.analiza_klastera import analiza_mreze_klastera, analiza_koalicija_i_antikoalicija

def main():
    GRAF = ucitaj()
    if GRAF is not None:
        print(f"\nGraf je ucitan i sadrzi {len(list(GRAF.nodes))} cvorova i {len(list(GRAF.edges))} linkova")
        broj_komponenti_povezanosti = nx.number_connected_components(GRAF)
        print(f"Broj povezanih komponenti u grafu: {broj_komponenti_povezanosti}")
        if len(GRAF.nodes) > 3000:
            print("Graf je preveliki, pa se za pocetak izbegava racunanje dijametra...")
        else:
            if broj_komponenti_povezanosti == 1:
                print(f"Duzina dijametra u grafu iznosi: {nx.diameter(GRAF)}")
            else:
                gcc = sorted(nx.connected_components(GRAF), key=len, reverse=True)
                G0 = GRAF.subgraph(gcc[0]);
                print(f"Graf cini {len(list(gcc))} komponente/i, pa je dijametar neizracunljiv (gigantsku komponentu cini "
                      f"{round(len(G0.nodes)*100.0/len(GRAF.nodes), 2)}% ukupnog broja cvorova)")
        print("\nProvera klasterabilnosti grafa...")
        skup_klastera = None
        if len(GRAF.nodes) < 500:
            skup_klastera = detektovanje_klastera(GRAF)
            print("Broj klastera u grafu: {}.".format(len(skup_klastera)))
            naziv = input("Uneti naziv za graficki prikaz grafa ---> ")
            if len(GRAF.nodes) > 100:
                nacrtaj_veliki(GRAF, naziv)
            else:
                nacrtaj_mali(GRAF, naziv)
        else:
            skup_klastera = detektovanje_klastera(GRAF)
            print("Broj klastera u grafu: {}".format(len(skup_klastera)))
            print("Obzirom da posmatrani graf ima vise od 500 cvorova, nije ga moguce graficki prikazati.")
            
        if skup_klastera is not None:
            print("Pravljenje klastera..\n")
            klasteri = napravi_klastere(skup_klastera,list(GRAF.edges.data()))
            
            if klasteri is not None:
                print("Klasteri su napravljeni.")
            
            set_klastera = detektovanje_koalicija(klasteri)
            detektovane_koalicije = set_klastera[0]
            detektovane_antikoalicije = set_klastera[1]
            
            print("\nU grafu se nalazi {} koalicija.".format(len(detektovane_koalicije)))
            print("U grafu se nalazi {} antikoalicija.".format(len(detektovane_antikoalicije)))
            
            if len(detektovane_antikoalicije) == 0:
                print("\nObzirom da nema antikoalicija, mreza je klasterabilna i balansirana (u grafu ne postoje linkovi koji narusavaju klasterabilnost).")
            else:
                print("\nObzirom da je broj antikoalcija u mrezi {0}, mreza nije klasterabilna.".format(len(detektovane_antikoalicije)))
        
        #ispisivanje antikoalicija i koalicija
        izbor = input("\nPrikazati sadrzaj klastera (Y/N) -> ")
        if izbor == "Y" or izbor == "y":
            if (len(detektovane_koalicije) > 0):
                print(f"Klasteri koalicije (broj koalicija: {len(detektovane_koalicije)}):")
                for k in detektovane_koalicije:
                    print(k.nodes)
            else:
                print("Nema klastera koalicija u mrezi.")
            if (len(detektovane_antikoalicije) > 0):
                print(f"Klasteri antikoalicije (broj antikoalicija: {len(detektovane_antikoalicije)}):")
                for k in detektovane_antikoalicije:
                    print(k.nodes)
            else:
                print("Nema klastera antikoalicija u mrezi.")
                    
        # Detektovanje linkova koji narusavaju klasterabilnost
        if len(detektovane_antikoalicije) > 0:
                lose_veze = detekcija_losih_veza(detektovane_antikoalicije)
                print(f"Linkova koji narusavaju klasterabilnost ima: {len(lose_veze)} (njih treba ukloniti da bi mreza bila klasterabilna)")
                izaberi = input("Prikazi lose veze? (Y/N) -> ")
                if izaberi == "Y" or izaberi == "y":
                    brojac = 1;
                    if (len(lose_veze)) < 200:
                        for veza in lose_veze:
                            print("Veza {0}: {1}".format(brojac, veza))
                            brojac+=1
                    else:
                        brojac = 1
                        for i in range (0, 200):
                            print("Veza {0}: {1}".format(brojac, lose_veze[i]))
                            brojac += 1
                        print("....")
                            
        
        #Analiza koalicija i antikoalicija
        analiza_koalicija_i_antikoalicija(detektovane_koalicije, detektovane_antikoalicije)                
        # Analiza mreze klastera
        print("\nPravljenje mreze klastera...")
        mreza_klastera = napravi_mrezu_klastera(GRAF, klasteri)
        print("Analiziranje mreze klastera...")
        analiza_mreze_klastera(mreza_klastera)
        print("Zavrsena analiza mreze klastera.")
        
        print("-" * 33 +'KRAJ PROGRAMA'+"-" * 33)
    

def ucitaj():
    print("=" * 80 + "\n*                           Analiza socijalnih mreza                           *\n" + "=" * 80)
    print("\nIzaberite graf za ucitavanje: ")
    print("1) Ucitaj rucno napravljen klasterabilan graf")
    print("2) Ucitaj rucno napravljen neklasterabilan graf")
    print("3) Ucitaj graf sa random oznacenim pozitivnim i negativnim vezama")
    print("4) Ucitaj graf iz fajla")
    print("5) Zavrsi program")
    
    izabranaOpcija = "0"
    while int(izabranaOpcija) < 1 or int(izabranaOpcija) > 4:
        izabranaOpcija = input("Unesite jednu od ponudjenih opcija -> ")
    switcher = {
        1: prva_opcija,
        2: druga_opcija,
        3: treca_opcija,
        4: cetvrta_opcija, 
        5: peta_opcija
    }
    izabranaFunkcija = switcher.get(int(izabranaOpcija))
    return izabranaFunkcija()
    
    
def prva_opcija():
    return ucitaj_rucno_graf();

def druga_opcija():
    return ucitaj_neklasterabilan()
    
def treca_opcija():
    return ucitaj_jednostavan_graf();

def cetvrta_opcija():
    print("Izaberite koji od ponudjenih grafova zelite ucitati:")
    print("1) Graf iz fajla 'bitcoin-epinions.csv' sa 'Stanforda'")
    print("2) Graf iz fajla 'wiki-RfA.txt' sa 'Stanforda'")
    print("3) Graf iz fajla 'soc-sign-slashdot.txt' sa 'Stanforda'")
    opcija = "0"
    while int(opcija) < 1 or int(opcija) > 3:
        opcija = input("Unesite jednu od ponudjenih opcija -> ")
    if opcija == "1":
        parent = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
        return ucitaj_epinions(path.join(parent, "fajlovi", "bitcoin-epinions.csv"))
    if opcija == "2":
        parent = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
        return ucitaj_wiki(path.join(parent, "fajlovi", "wiki-RfA.txt"))
    parent = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
    return ucitaj_slashdot(path.join(parent, "fajlovi", "soc-sign-slashdot.txt"))

def peta_opcija():
    zavrsi_program()
    
def zavrsi_program():
    print()
    print("-" * 33 +'KRAJ PROGRAMA'+"-" * 33)
    return None;        
    
if __name__ == '__main__':
    main()
    
