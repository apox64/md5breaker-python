import redis
import hashlib
import os
import re

r = redis.Redis(host='redis', port=6379, db=0)

def check_redis_connection():
    try:
        response = r.client_list()
        print "Connection to database successful."
    except redis.ConnectionError:
        print "Could not establish connection to redis database."

def md5hash(cleartext):
    return hashlib.md5(cleartext).hexdigest()

def add_to_database(cleartext):
    r.set(md5hash(cleartext), cleartext)
    #print "added: %s : %s" % (md5hash(cleartext), cleartext)

def flushdb(self):
    self.execute_command('FLUSHALL')
    print "database flushed. all keys cleared."

def dbsize(self):
    return self.execute_command('DBSIZE')

def doFlushDB():
    flushdb(r)

def getdbsize():
    print "current number of elements in the db: %d" % dbsize(r)
    return dbsize(r)

# some error handling
def isMD5(string):
    if len(string) != 32:
        return False
    elif re.findall(r'([a-fA-F\d]{32})', string):
        return True
    else:
        return False

# read from wordlist and populate database
def pumpwordlistintodb(wordlist):
    with open(wordlist, 'r') as file:
        for i, line in enumerate(file):
            cleartext = line.strip()
            add_to_database(cleartext)
        print "added %d entries to the database." % (i+1)

def breakhash(md5hashstring):
    if isMD5(md5hashstring):
        finding = r.get(md5hashstring)
        if (finding == None):
            return "not found"
        else:
            return finding
    else:
        return "not an md5 hash"

def initDB():
    wordlist_dir = os.path.dirname(__file__)+'/../wordlists'
    print wordlist_dir
    for f in os.listdir(wordlist_dir):
        pumpwordlistintodb(os.path.join(wordlist_dir, f))
    print "done adding wordlists to the database."
    getdbsize()

check_redis_connection()
