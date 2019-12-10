from rdflib import Graph,BNode,Literal,URIRef
from rdflib.namespace import RDF,RDFS,OWL,DC,FOAF,XSD,Namespace
from mtgsdk import Card
from mtgsdk.restclient import MtgException

g = Graph()
node = BNode()
fileName = "/magic"
file_path_linux = os.environ.get("USERPROFILE")


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
                    , format='xml')
        print(file_path_linux + fileName + '.owl')
    elif file_format == "n3":
        g.serialize(file_path_linux + fileName + '.n3'
                    , format='n3')
        print(file_path_linux + fileName + '.n3')
    elif file_format == "turtle":
        g.serialize(file_path_linux + fileName + '.rdf'
                    , format='turtle')
        print(file_path_linux + fileName + '.rdf')


def build_card_class() -> None:
    """
    Build the card class and bases

    :return:
    """
    g.bind('dc', DC)
    g.bind("owl", OWL)
    global mtg
    mtg = Namespace('file:/C:/Users/victo/')
    g.bind("magic",mtg)
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
        g.add((uri, OWL.ObjectProperty, mtg.card))
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
        print("Serviço indisponivel. \n", MtgException.__str__)
    

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
                cardN = Namespace('file:/Users/victo/card')
                card_id = URIRef(mtg.id+"/"+card.id)
                g.add((card_id,RDF.type,mtg.card))
                g.add((uri_property, RDFS.range, card_property))
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
result = g.query(""" PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX magic: <file:/Users/victo/>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?x ?property ?z ?y
    WHERE {?property owl:ObjectProperty ?x .
    FILTER regex(str(?property),"/mana") .
    ?property rdfs:range ?y .
    ?y rdfs:label ?z}""")

for r in result:
    print("%s %s %s %s" % r)
