import csv
import networkx as nx
import random

def ucitaj_rucno_graf():
    graf = nx.Graph();
    nx.set_edge_attributes(graf, "+", "oznaka")
    for i in range(1, 16):
        graf.add_node(i)
    graf.add_edge(1, 2, oznaka="+")
    graf.add_edge(1, 3, oznaka="+")   
    graf.add_edge(2, 3, oznaka="+")  
    
    graf.add_edge(2, 5, oznaka="+")
    graf.add_edge(3, 6, oznaka="-")
    graf.add_edge(5, 6, oznaka="-")
    
    graf.add_edge(6, 8, oznaka="+")
    graf.add_edge(6, 11, oznaka="-")
    graf.add_edge(8, 11, oznaka="-")
    
    graf.add_edge(11, 13, oznaka="-")
    graf.add_edge(11, 14, oznaka="-")
    graf.add_edge(13, 15, oznaka="-")
    graf.add_edge(14, 15, oznaka="-")
    
    graf.add_edge(10, 11, oznaka="-")
    graf.add_edge(10, 12, oznaka="+")
    graf.add_edge(12, 13, oznaka="+")
    
    graf.add_edge(7, 12, oznaka="+")
    graf.add_edge(9, 12, oznaka="+")
    graf.add_edge(4, 7, oznaka="-")
    
    return graf;

def ucitaj_neklasterabilan():
    graf = nx.Graph();
    nx.set_edge_attributes(graf, "+", "oznaka")
    for i in range(1, 21):
        graf.add_node(i)
        
    graf.add_edge(1, 2, oznaka="+")
    graf.add_edge(2, 3, oznaka="+")
    graf.add_edge(3, 4, oznaka="+")
    graf.add_edge(4, 5, oznaka="+")
    graf.add_edge(5, 6, oznaka="+")
    graf.add_edge(6, 7, oznaka="-")
    graf.add_edge(6, 8, oznaka="+")
    graf.add_edge(7, 8, oznaka="-")
    graf.add_edge(1, 4, oznaka="-")

    graf.add_edge(9, 10, oznaka="+")
    graf.add_edge(10, 11, oznaka="+")
    graf.add_edge(11, 12, oznaka="+")
    graf.add_edge(12, 13, oznaka="+")
    graf.add_edge(13, 14, oznaka="+")
    graf.add_edge(14, 15, oznaka="+")
    graf.add_edge(14, 16, oznaka="+")
    graf.add_edge(14, 11, oznaka="+")
    graf.add_edge(14, 12, oznaka="+")
    
    graf.add_edge(17, 18, oznaka="+")
    graf.add_edge(18, 19, oznaka="+")
    graf.add_edge(19, 20, oznaka="+")
    graf.add_edge(20, 17, oznaka="+")
    graf.add_edge(20, 18, oznaka="+")
    
    graf.add_edge(1, 20, oznaka="-")
    graf.add_edge(2, 20, oznaka="-")
    graf.add_edge(7, 20, oznaka="-")
    graf.add_edge(4, 14, oznaka="-")
    graf.add_edge(5, 14, oznaka="-")
    graf.add_edge(4, 14, oznaka="-")
    graf.add_edge(14, 20, oznaka="-")
    graf.add_edge(15, 20, oznaka="-")
    
    return graf;

#ukoliko je izabrana opcija da se random generise graf, uzimamo graf iz networkX biblioteke tutte_graph      
def ucitaj_jednostavan_graf(): 
    jednostavan_graf = nx.tutte_graph();
    oznaci_grane_grafa(jednostavan_graf)
    return jednostavan_graf;

#generise se oznacen graf od neoznacenog grafa random sistemom i to sa verovatnocom 33% da su dva cvora povezana negativnom granom  
def oznaci_grane_grafa(g):
    g.edges(data=True)
    nx.set_edge_attributes(g, "+", "oznaka")
    epsilon = 0.33
    for (u, v) in g.edges():
        if random.uniform(0, 1) < epsilon:
            g.add_edge(u, v, oznaka="-")

def ucitaj_epinions(putanja):
    graf_epinions = nx.DiGraph()
    with open(putanja, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if int(row[2]) > 0:
                znak = "+"
            else:
                znak = "-"
            graf_epinions.add_edge(row[0], row[1], oznaka=znak)
    csv_file.close()
    return pretvori_u_neusmeren(graf_epinions)


def ucitaj_wiki(putanja):
    file = open(putanja, "r", encoding="utf8")
    graf_wiki= nx.DiGraph()
    linije = file.read().splitlines()
    cvor_A = None
    cvor_B = None
    for line in linije:
        if line.startswith("SRC"):
            cvor_A = line.split(":")[1]
        if line.startswith("TGT"):
            cvor_B = line.split(":")[1]
        if line.startswith("RES"):
            znak = line.split(":")[1]
            if znak == "1":
                znak = "+"
            else:
                znak = "-"
            graf_wiki.add_edge(cvor_A, cvor_B, oznaka=znak)
    return pretvori_u_neusmeren(graf_wiki)

def ucitaj_slashdot(putanja):
    file = open(putanja, "r")
    linije = file.read().splitlines()
    lista_linkova = []
    for line in linije:
        if line.startswith("#"):
            continue
        line = line.split("\t")
        if "-1" in line[2]:
            znak = "-"
        else:
            znak = "+"
        element = (line[0].strip(), line[1].strip(), {'oznaka': znak})
        lista_linkova.append(element)
    graf = nx.DiGraph()
    graf.add_edges_from(lista_linkova)
    return pretvori_u_neusmeren(graf)
    
    
def pretvori_u_neusmeren(graf):
    usmeren_graf = nx.Graph()
    usmeren_graf.add_edges_from(graf.edges(), oznaka="")
    for u, v, d in graf.edges(data=True):
        znak1 = graf[u][v]['oznaka']
        znak2 = ""
        if (v, u) in graf.edges:
            znak2 = graf[v][u]['oznaka']
        if znak1 == "-" or znak2 == "-":
            usmeren_graf[u][v]['oznaka'] = "-"
        else:
            usmeren_graf[u][v]['oznaka'] = "+"
    print("Zavrseno ucitavanje!")
    return usmeren_graf
