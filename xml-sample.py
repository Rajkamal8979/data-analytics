import xml.etree.cElementTree as ET
import pprint as pp
import re
from pymongo import MongoClient as mc

new_list=[]
regex=r"( +)(bank+)( )"

filename=r"D:\Python-Conda\agra_india.osm"
records={}
records['Petha Stores']={}
records['Banks']={}
records['Supermarket']={}
ATMs=[]
#records['Banks']['irrelevant']={}
#print(records)
banklist=['Punjab National Bank',
          'State Bank of India',
          'Allahabad bank',
          'Axis bank',
          'Bank of baroda',
          'bank of India',
          'Central Bank of India',
          'ICICI Bank','IDBI Bank',
          'Industrial Development Bank of India',
          'JILA SAHKARI BANK',
          'Karnataka Bank',
          'OBC BANK',
          'Oriental Bank of Commerce',
          'Overseas Bank',
          'Syndicate Bank',
          'Union Bank',
          'Vijaya Bank',
          'YES BANK',
          'south indian bank'
          ]
		  
#----- Connecting MongoDB Atlas--------#

def get_db():
	client=mc("mongodb://'%s':'%s'@clusterkamal-shard-00-00-henbx.mongodb.net:27017,clusterkamal-shard-00-01-henbx.mongodb.net:27017,clusterkamal-shard-00-02-henbx.mongodb.net:27017/test?ssl=true&replicaSet=clusterkamal-shard-0&authSource=admin%('myname','mypassword')"
	)
	#client=mc()
	db=client.agra_base
	if db:
		print("Connected")
	return db

#---------Inserting Data-----------------#

def add_data(db,records):
	db.agra.insert(records,check_keys=False)
	

#-------Finding Super market list from XML Map file---------------#


def supermarket(file_name,records):
    for event,element in ET.iterparse(file_name,events=("start","end")):
        if element.tag=='node' and event=="end":
            for tag in element.iter('node'):
                new_dict={}
                for inner_tag in element.iter('tag'):
                    new_dict[inner_tag.attrib['k']]=inner_tag.attrib['v']
            for inner_tag in element.iter('tag'):
                v=inner_tag.attrib['v']
                if "supermarket" in v and "supermarket"in new_dict.values():
                    try:
                        records['Supermarket'][new_dict['name']]=tag.attrib['user']
                        #records['Supermarket'].update(new_dict['name'])
                    except KeyError:
                        pass
    return records


#---------Finding Petha Stores from XML Map File---------------------#


def sweet_stores(file_name,records):
    for event,element in ET.iterparse(file_name,events=("start","end")):
        if element.tag=='node':
            for tag in element.iter('node'):
                for inner_tag in element.iter('tag'):
                    v=inner_tag.attrib['v']
                    if "petha" in v.lower():
                        name=tag.attrib['user']
                        #print(name)
                        records['Petha Stores'][v]=name
    return records

#----------Retrieving Banks list from XML map file--------------------#


def banks__(file_name,records):
    #print(records)
    
    for event,element in ET.iterparse(file_name,events=("start","end")):
        if element.tag=='node':
            for tag in element.iter('node'):
                for inner_tag in element.iter('tag'):
                    v=inner_tag.attrib['v']
                    if re.search(regex,v.lower()):
                        name=tag.attrib['user']
                        #print(v)
                        #print(name)
                        records['Banks'][v]=name
    
    return records


#------------Finding ATM's in Bank list as code pulled ATM's and banks.-------------

def find_ATM(records,atm):
    for keys in records['Banks'].keys():
        if 'atm' in keys.lower():
            atm.append(keys)
    records['ATM']=atm
    return records
	
#---------------Main---------------------------------------------#

            
if __name__=='__main__':
	db=get_db()
	record1=supermarket(filename,records)
    #pp.pprint(record)
	record2=sweet_stores(filename,record1)
    #pp.pprint(record)
	record3=banks__(filename,record2)
    #pp.pprint(record3)
	updated=find_ATM(record3,ATMs)
    #pp.pprint(updated)
	add_data(db,updated)

    #pp.pprint(record['Banks'].keys())
    #for key in record['Banks'].keys():
        #if key.lower() not in [x.lower() for x in banklist]:
         #   pass
        #else:
         #   records['Banks']['irrelevant']=key
    #pp.pprint(records)
    #print(len(new_list))
    #print(len(banklist))
    #check_data()


