import paho.mqtt.client as mqtt # pip install paho.mqtt

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME


rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
sosa = Namespace("http://www.w3.org/ns/sosa/")
time = Namespace("http://www.w3.org/2006/time#")
qudt_1_1 = Namespace("http://qudt.org/1.1/schema/qudt#")
qudt_unit_1_1 = Namespace("http://qudt.org/1.1/vocab/unit#")
cdt = Namespace("http://w3id.org/lindt/custom_datatypes#")
ex = Namespace("http://example.org/data/")

g = Graph()
g.add((ex['earthAtmosphere'], RDF.type, sosa.FeatureOfInterest))
g.add((ex['earthAtmosphere'], RDFS.label, Literal("Atmosphere of Earth", lang="en")))
g.add((ex['iphone7/35-207306-844818-0'], RDF.type, sosa.Platform))
g.add((ex['iphone7/35-207306-844818-0'], RDFS.label, Literal("IPhone 7 - IMEI 35-207306-844818-0", lang="en")))
g.add((ex['iphone7/35-207306-844818-0'], RDFS.comment, Literal("IPhone 7 - IMEI 35-207306-844818-0 - John Doe", lang="en")))
g.add((ex['iphone7/35-207306-844818-0'], sosa.hosts, ex['sensor/35-207306-844818-0/BMP282']))

g.add((ex['sensor/35-207306-844818-0/BMP282'], RDF.type, sosa.Sensor))
g.add((ex['sensor/35-207306-844818-0/BMP282'], RDFS.label, Literal("Bosch Sensortec BMP282", lang="en")))
g.add((ex['sensor/35-207306-844818-0/BMP282'], sosa.observes, ex['sensor/35-207306-844818-0/BMP282/atmosphericPressure']))


observation_uri = ex['Observation/346345']
g.add((observation_uri, RDF.type, sosa.Observation))
g.add((observation_uri, sosa.observedProperty, ex['sensor/35-207306-844818-0/BMP282/atmosphericPressure']))
g.add((observation_uri, sosa.hasFeatureOfInterest, ex['earthAtmosphere']))
g.add((observation_uri, sosa.madeBySensor, ex['sensor/35-207306-844818-0/BMP282']))
g.add((observation_uri, sosa.hasResult, Literal("101936", datatype=xsd.double)))
g.add((observation_uri, sosa.hasResult, ex['sensor/35-207306-844818-0/BMP282/atmosphericPressure']))
g.add((observation_uri, sosa.resultTime, ex['time_instant']))


def on_message(client, userdata, msg):
    global received_messages, rdf_graph    
    received_messages += 1
    payload = msg.payload.decode()
    reading, dt = payload.split('|')
    observation_uri = ex[f'Observation/{received_messages}']
    g.add((observation_uri, RDF.type, sosa.Observation))
    g.add((observation_uri, sosa.observedProperty, ex['sensor/35-207306-844818-0/BMP282/atmosphericPressure']))
    g.add((observation_uri, sosa.hasFeatureOfInterest, ex['earthAtmosphere']))
    g.add((observation_uri, sosa.madeBySensor, ex['sensor/35-207306-844818-0/BMP282']))
    g.add((observation_uri, sosa.hasSimpleResult, Literal(reading)))
    g.add((observation_uri, sosa.resultTime, Literal(dt, datatype=xsd.dateTime)))
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")
    if received_messages==10:
        client.unsubscribe(topic)
        time.sleep(4)
        client.loop_stop()  # Stop the message loop after unsubscribing
        client.disconnect()  # Disconnect from the MQTT server
        

client = mqtt.Client()
client.on_message = on_message

broker_address = "test.mosquitto.org"
port = 1883

client.connect(broker_address, port, 60)

topic = "teds22/group9/pressure"
client.subscribe(topic)
received_messages = 0
client.loop_start()



while received_messages < 10:
        pass

print("Interrupted by the user. Stopping the MQTT client.")
client.unsubscribe("example/topic")
client.loop_stop()
client.disconnect()
with open("pressure.ttl", "w") as f:
            print(1)
            f.write(g.serialize(format="turtle"))
