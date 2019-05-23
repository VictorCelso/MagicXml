import dis
import re
import os

from mtgsdk import Card
from rdflib import Graph, BNode, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, DC, Namespace

g = Graph()
node = BNode()
fileName = "magic"
file_path_linux = os.environ.get("HOME")+"/Desktop/"


def serialize_xml(file_format) -> None:
    """
    Generate file in the parameter format

    :type file_format: str
    :param file_format: str
    :return:
    """
    print(file_format)
    if file_format == "xml":
        g.serialize(file_path_linux + fileName + '.xml'
                    , format='pretty-xml')
    elif file_format == "n3":
        g.serialize(file_path_linux + fileName + '.n3'
                    , format='n3')
    elif file_format == "turtle":
        g.serialize(file_path_linux + fileName + '.txt'
                    , format='turtle')


def build_card_class() -> None:
    """
    Build the card class and bases

    :return:
    """
    g.bind('dc', DC)
    g.bind("owl", OWL)
    global mtg
    mtg = Namespace('Magic/')
    g.add((mtg.card, RDF.type, OWL.Class))
    att_getter()
    for att in att_list:
        print(att)
        att = att.replace("'", "")
        if att == "multiverseid":
            result = "multiverse_id"
        else:
            result = re.sub('([A-Z]{1})', r'_\1',att).lower()
        uri = URIRef(mtg.card + "/" + result)
        g.add((uri, OWL.ObjeProperty, mtg.card))
        g.add((uri,RDFS.domain,mtg.card))
    """
    g.add((mtg.manaCost, OWL.ObjectProperty, mtg.card))
    g.add((mtg.manaCost, RDFS.domain, mtg.card))
    g.add((mtg.manaConvertion, OWL.ObjectProperty, mtg.card))
    g.add((mtg.manaConvertion, RDFS.domain, mtg.card))
    g.add((mtg.name, OWL.ObjectProperty, mtg.card))
    g.add((mtg.name, RDFS.domain, mtg.card))
    g.add((mtg.manaCost, OWL.ObjectProperty, mtg.card))
    g.add((mtg.manaCost, RDFS.domain, mtg.card))
    """


def fetch_cards(page_num, size) -> None:
    """
    Fetch a list of cards

    :type page_num: int
    :type size: int
    :param page_num: int
    :param size: int
    :return:
    """
    global cards
    try:
        cards = Card.where(page=page_num).where(pageSize=size).all()
    except MtgException:
        print("Serviço indisponivel.")
    

def build_file(file_format) -> None:
    """
    Create RDF file

    :type file_format: str
    :param file_format: str
    :return:
    """
    build_card_class()
    fetch_cards(1, 100)
    for card in cards:
        for att in att_list:
            att = att.replace("'", "")
            if att == "multiverseid":
                result = "multiverse_id"
            else:
                result = re.sub('([A-Z]{1})', r'_\1',att).lower()
            #print(result)
            uri = mtg.card + "/" + result
            card_uri = mtg.card + "/" + result+ "/" + card.id
            card_property = URIRef(card_uri)
            uri_property = URIRef(uri)
            if att == "id":
                card_id = URIRef(mtg.card+"/id/"+card.id)
                g.add((card_id,RDF.type,mtg.card))
                g.add((card_id,RDFS.label,Literal("card")))
            else:
                g.add((card_property, RDF.type, OWL.Class))
                g.add((card_property, RDFS.label, Literal(getattr(card, result))))
                g.add((uri_property, RDFS.range, card_property))
            """card_uri = mtg.manaConverted + card.id
            card_property = URIRef(card_uri)
            g.add((card_property, RDF.type, OWL.Class))
            g.add((card_property, RDFS.label, Literal(card.cmc)))
            g.add((mtg.manaConvertion, RDFS.range, card_property))
            card_uri = mtg.name + card.id
            card_property = URIRef(card_uri)
            g.add((card_property, RDF.type, OWL.Class))
            g.add((card_property, RDFS.label, Literal(card.name)))
            g.add((mtg.name, RDFS.range, card_property))
            """
        #print(getattr(card, "name"))

    serialize_xml(file_format)


def att_getter():
    global att_list
    att_list = []
    class_init = dis.code_info(Card.__init__)
    for att in class_init.split("\n"):
        try:
            result = re.search("'(.*)'", att)
            att_list.append(result.group())
        except AttributeError:
            ""


build_file("xml")
