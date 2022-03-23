import networkx as nx

class Komponente:
    
    poseceni = None
    komponente = None
    
    mapa_klastera = None
    broj_klastera = None
    
    def __init__(self, g):
        self.mali_graf = g
        self.poseceni = set()
        self.komponente = set()
        self.mapa_klastera = dict()
        self.broj_klastera = 1
    
    def detektuj_komponente(self):
        for cvor in self.mali_graf.nodes:
            if cvor not in self.poseceni:
                self.komponente.add(self.bfs(cvor))
                self.broj_klastera += 1;
        return frozenset(self.komponente)
        
    
    def bfs(self, c):
        komp = set()
        queue = []
        komp.add(c)
        self.poseceni.add(c)
        self.mapa_klastera[c] = self.broj_klastera;
        queue.append(c)

        while len(queue) > 0:
            tmp = queue.pop(0)
            susedi = list(nx.neighbors(self.mali_graf, tmp))
            for s in susedi[:]:
                d1 = self.mali_graf.get_edge_data(tmp, s)
                d2 = self.mali_graf.get_edge_data(s, tmp)
                if d1['oznaka'] == "-" or d2['oznaka'] == '-':
                    continue
                if s not in self.poseceni:
                    komp.add(s)
                    self.poseceni.add(s)
                    self.mapa_klastera[s] = self.broj_klastera;
                    queue.append(s)
        graf_tmp = nx.Graph()
        graf_tmp.add_nodes_from(komp)
        return graf_tmp
    
    def get_mapa(self):
        return self.mapa_klastera;

mapa_klastera = dict() 
       
def detektovanje_klastera(graf):
    klasteri = Komponente(graf)
    povratne_komponente = klasteri.detektuj_komponente()
    dobavi_mapu(klasteri)
    return povratne_komponente

def dobavi_mapu(klasteri):
    global mapa_klastera
    mapa_klastera = klasteri.get_mapa();
    
#    Metoda od prosledjenog skupa skupova cvorova, koji predstavljaju klastere, pravi
#    klastere kao grafove same za sebe, a na osnovu grafa 'g' koji je polazni graf
def napravi_klastere(skup_klastera, grane_grafa):
    global mapa_klastera
    klasteri = set()
    i = 1
    lista_klastera = list(skup_klastera)
    for g in grane_grafa:
        cvor1 = g[0]
        cvor2 = g[1];
        ozn = g[2].get('oznaka')
        broj_klastera1 = mapa_klastera[cvor1];
        broj_klastera2 = mapa_klastera[cvor2];
        if broj_klastera1 == broj_klastera2:
            brojac = -1
            while brojac < len(lista_klastera):
                brojac+=1
                lista_cvorova = list(lista_klastera[brojac].nodes)
                if cvor1 in lista_cvorova and cvor2 in lista_cvorova:
                    lista_klastera[brojac].add_edge(cvor1, cvor2, oznaka=ozn)
                    break
    i = 0
    while i < len(lista_klastera):
        klasteri.add(lista_klastera[i])
        i +=1
    return klasteri;

def detektovanje_koalicija(klasteri):
    print("Detektovanje koalicija i antikoalicija...")
    set_klastera = []
    koalicije = set()
    antikoalicije = set()
    
    for k in klasteri:
        lose_grane = [(u, v) for (u, v, d) in k.edges(data=True) if d['oznaka'] == '-']
        if (len(lose_grane)) == 0:
            koalicije.add(k)
        else:
            antikoalicije.add(k)
    
    set_klastera.append(koalicije)
    set_klastera.append(antikoalicije)
    print('...detektovane su.')
    return set_klastera;

def napravi_mrezu_klastera(graf, klasteri):
    novi_graf = nx.Graph()
    brojac = 1
    for k in klasteri:
        k.graph['ime'] = str(brojac)
        brojac += 1
        novi_graf.add_node(k)
        
    for k1 in klasteri:
        for k2 in klasteri:
            if k1 == k2:
                continue
            povezani = False
            br = 0
            while not povezani and br < len(k1.nodes):
                n1 = list(k1.nodes)[br]
                br += 1
                for n2 in k2:
                    if n1 in nx.neighbors(graf, n2):
                        povezani = True
            if povezani:
                novi_graf.add_edge(k1, k2)
    nx.set_edge_attributes(novi_graf, "-", "oznaka")
    return novi_graf

#Detektovanje grana koje narusavaju klasterabilnost - negativne grane u antikoalicijama
def detekcija_losih_veza(antikoalicije):
    lista_grana = []
    for g in antikoalicije:
        lose_grane = [(u, v) for (u, v, d) in g.edges(data=True) if d['oznaka'] == "-"]
        lista_grana.append(lose_grane)
    return [item for sublist in lista_grana for item in sublist]
