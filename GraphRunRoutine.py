from rdflib import Graph,BNode,Literal,URIRef
from rdflib.namespace import RDF,RDFS,OWL,DC,FOAF,XSD,Namespace
from mtgsdk import Card

g = Graph()
node = BNode()
fileFormat = 'txt'
fileExt = '.txt'
fileName = 'test'
filePath = 'C:/Users/victor.c.tassinari/Desktop/'

def serializeXml():
    print(fileFormat)
    if(fileFormat=="xml"):
        g.serialize(filePath+fileName+'.xml'
                    ,format='pretty-xml')
    else:
        g.serialize(filePath+fileName+'.n3'
                    ,format='n3')

def buildCardClass():
    g.bind('dc',DC)
    g.bind("owl",OWL)
    global mtg
    mtg = Namespace('Magic/')
    g.add((mtg.card,RDF.type,OWL.Class))
    g.add((mtg.manaCost,OWL.ObjectProperty,mtg.card))
    g.add((mtg.manaCost,RDFS.domain,mtg.card))
    g.add((mtg.manaConvertion,OWL.ObjectProperty,mtg.card))
    g.add((mtg.manaConvertion,RDFS.domain,mtg.card))
    g.add((mtg.name,OWL.ObjectProperty,mtg.card))
    g.add((mtg.name,RDFS.domain,mtg.card))
    g.add((mtg.manaCost,OWL.ObjectProperty,mtg.card))
    g.add((mtg.manaCost,RDFS.domain,mtg.card))
    
def fetchCards(pageNum,size):
    global cards
    cards = Card.where(page=pageNum).where(pageSize=size).all()

def buildFile():
    buildCardClass()
    fetchCards(1,100)
    for card in cards:
        cardUri = mtg.mana+card.id
        cardProperty = URIRef(cardUri)
        g.add((cardProperty,RDF.type,OWL.Class))
        g.add((cardProperty,RDFS.label,Literal(card.mana_cost)))
        g.add((mtg.manaCost,RDFS.range,cardProperty))
        cardUri = mtg.manaConverted+card.id
        cardProperty = URIRef(cardUri)
        g.add((cardProperty,RDF.type,OWL.Class))
        g.add((cardProperty,RDFS.label,Literal(card.cmc)))
        g.add((mtg.manaConvertion,RDFS.range,cardProperty))
        cardUri = mtg.name+card.id
        cardProperty = URIRef(cardUri)
        g.add((cardProperty,RDF.type,OWL.Class))
        g.add((cardProperty,RDFS.label,Literal(card.name)))
        g.add((mtg.name,RDFS.range,cardProperty))

    serializeXml()
        
buildFile()
