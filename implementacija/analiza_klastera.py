import matplotlib.pyplot as plt
import networkx as nx
import math

def analiza_koalicija_i_antikoalicija(koalicije, antikoalicije):
    print("\nAnaliziranje sličnosti i razlike u strukturi koalicija i antikoalicija...\n")

    metrike_koalicije = izracunaj_metrike(koalicije)
    metrike_antikoalicije = izracunaj_metrike(antikoalicije)

    koalicije_kohezivnije = provera(metrike_koalicije['prosecan_stepen'], metrike_antikoalicije['prosecan_stepen'])
    antikoalicije_kohezivnije = provera(metrike_antikoalicije['prosecan_stepen'], metrike_koalicije['prosecan_stepen'])

    antikoalicije_manji_dijametar = provera(metrike_koalicije['dijametar'], metrike_antikoalicije['dijametar'])
    koalicije_manji_dijametar = provera(metrike_antikoalicije['dijametar'], metrike_koalicije['dijametar'])

    koalicije_udaljenost_cvorova = provera(metrike_koalicije['prosecna_distanca'], metrike_antikoalicije['prosecna_distanca'])
    antikoalicije_udaljenost_cvorova = provera(metrike_antikoalicije['prosecna_distanca'], metrike_koalicije['prosecna_distanca'])

    print("Prilikom analize koalicija i antikoalicija dobili smo sledece rezultate:\n")
    if not koalicije_kohezivnije and not antikoalicije_kohezivnije:
        print("Koalicije i anti-koalicije se ne razlikuju po kohezivnosti.")
    elif koalicije_kohezivnije:
        print("Koalicije su kohezivnije mreze u odnosu na antikoalicije.")
    else:
        print("Antikoalicije su kohezivnije mreze u odnosu na koalicije.")

    if not koalicije_manji_dijametar and not antikoalicije_manji_dijametar:
        print("Koalicije i antikoalicije se ne razlikuju po duzini dijametra.")
    elif koalicije_manji_dijametar:
        if len(metrike_koalicije['dijametar']) > 0:
            print("Koalicije imaju manji dijametar nego antikoalicije. Prosecan dijametar koalicija: {}.".format(round(sum(metrike_koalicije['dijametar'])/len(metrike_koalicije['dijametar']), 2)))
        else:
            print("Koalicije imaju manji dijametar nego antikoalicije.")
    else:
        if len(metrike_antikoalicije['dijametar']) > 0:
            print("Antikoalicije imaju manji dijametar nego koalicije. Prosecan dijametar antikoalicija: {}.".format(round(sum(metrike_antikoalicije['dijametar'])/len(metrike_antikoalicije['dijametar']), 2)))
        else:
            print("Antikoalicije imaju manji dijametar nego koalicije.")
    if not koalicije_udaljenost_cvorova and not antikoalicije_udaljenost_cvorova:
        print("Koalicije i antikoalicije se ne razlikuju po udaljenosti cvorova.")
    elif koalicije_udaljenost_cvorova:
        if len(metrike_koalicije['prosecna_distanca']) > 0:
            print("Cvorovi koalicija su vise distancirani u odnosu na cvorove antikoalicija. Prosecna distanca cvorova u koalicijama: {}".format(round(sum(metrike_koalicije['prosecna_distanca'])/len(metrike_koalicije['prosecna_distanca']), 2)))
        else:
            print("Cvorovi koalicija su vise distancirani u odnosu na cvorove antikoalicija. ")
    else:
        if len(metrike_antikoalicije['prosecna_distanca']) > 0:
            print("Cvorovi antkoalicija su vise distancirani u odnosu na cvorove koalicija. Prosecna distanca cvorova u antikoalicijama: {}".format(round(sum(metrike_antikoalicije['prosecna_distanca'])/len(metrike_antikoalicije['prosecna_distanca']), 2)))
        else:
            print("Cvorovi antkoalicija su vise distancirani u odnosu na cvorove koalicija.")

def provera(niz1, niz2):
    for vrednost1 in niz1:
        for vrednost2 in niz2:
            if vrednost1 < vrednost2:
                return False
    return True


def izracunaj_metrike(skup_klastera):
    niz_metrika = {'prosecan_stepen': [], 'dijametar': [], 'prosecna_distanca': []}
    for klaster in skup_klastera:
        tmp = prosecan_stepen(klaster)
        if tmp != 0:
            tmp = math.log10(tmp)
        niz_metrika['prosecan_stepen'].append(tmp)
        tmp = dijametar(klaster)
        if tmp != 0:
            tmp = math.log10(tmp)
        niz_metrika['dijametar'].append(tmp)
        tmp = prosecna_distanca(klaster)
        if tmp != 0:
            tmp = math.log10(tmp)
        niz_metrika['prosecna_distanca'].append(tmp)
    return niz_metrika


def prosecan_stepen(klaster = nx.Graph()):
    sum = 0
    for cvor in klaster.nodes:
        sum += klaster.degree(cvor)
    return sum*1.0/len(klaster.nodes)

def dijametar(klaster):
    return nx.diameter(klaster)

def prosecna_distanca(klaster):
    return nx.average_shortest_path_length(klaster)


#za formiranu mrezu klastera pravimo grafik raspodele stepeni
def analiza_mreze_klastera(novi_g):
    broj_cvorova_mreze = len(novi_g.nodes)
    broj_grana_mreze = len(novi_g.edges)
    broj_komponenti_povezanosti = nx.number_connected_components(novi_g)
    if broj_komponenti_povezanosti == 1:
        dijametar_mreze = nx.diameter(novi_g)
    else:
        dijametar_mreze = "beskonacno"

    sekvenca_stepeni = sorted([d for n, d in novi_g.degree()], reverse=True)

    fig = plt.figure()
    fig.suptitle('Grafik raspodele stepeni cvorova u novonastalom grafu klastera', fontsize=12, fontweight='bold')

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_title(f"Broj cvorova: {broj_cvorova_mreze}, broj linkova: {broj_grana_mreze}, "
                 f"broj povezanih komponenti: {broj_komponenti_povezanosti}, dijametar: {dijametar_mreze}", fontsize=8, fontweight='bold')

    ax.set_xlabel('rang')
    ax.set_ylabel('stepen')

    plt.loglog(sekvenca_stepeni, 'b-', marker='o')
    plt.axes([0.60, 0.60, 0.30, 0.25])
    if len(novi_g.nodes) < 100:
        pos = nx.spring_layout(novi_g)
    else:
        pos = nx.circular_layout(novi_g)
    plt.axis('off')
    nx.draw_networkx_nodes(novi_g, pos, node_size=30, node_color='r',)
    nx.draw_networkx_edges(novi_g, pos, width=3.0, edge_color='k', alpha=0.4)
    plt.show()


