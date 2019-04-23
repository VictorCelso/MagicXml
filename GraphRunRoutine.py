from rdflib import Graph,BNode,Literal,URIRef
from rdflib.namespace import RDF,RDFS,OWL,DC,FOAF,XSD,Namespace
from mtgsdk import Card

g = Graph()
node = BNode()
cardClass = '/Card/'
fileFormat = 'turtle'
fileExt = '.txt'
fileName = 'test'
filePath = 'C:/Users/victor.c.tassinari/Desktop/'

def serializeXml():
    g.serialize(filePath+fileName+fileExt
                ,format=fileFormat)

def buildCardClass():
    g.bind('dc',DC)
    global mtg
    mtg = Namespace('Magic/')
    g.add((mtg.card,RDF.type,RDFS.Class))
    g.add((mtg.card,RDF.Property,mtg.manaCost))
    g.add((mtg.card,RDF.Property,DC.title))
    g.add((mtg.card,RDF.Property,DC.description))
    g.bind('magic',mtg)
    g.add((mtg.manaCost,RDF.type,RDF.Property))
    g.add((mtg.manaCost,RDFS.domain,mtg.card))
    g.add((mtg.manaCost,RDFS.range,XSD.double))
    g.add((DC.title,RDFS.domain,mtg.card))
    g.add((DC.description,RDFS.domain,mtg.card))
    

def fetchCards(pageNum,size):
    global cards
    cards = Card.where(page=pageNum).where(pageSize=size).all()

def buildFile():
    buildCardClass()
    fetchCards(1,100)
    for card in cards:
        cardId = cardClass+card.id
        newCard = URIRef(cardId)
        g.add((newCard,RDF.resource,mtg.card))
        g.add((newCard,mtg.manaCost,Literal(card.cmc)))
        g.add((newCard,DC.title,Literal(card.name)))
        g.add((newCard,DC.description,Literal(card.text)))
        g.add((newCard,RDFS.label,Literal('card')))
    serializeXml()
