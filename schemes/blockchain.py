from hashlib import sha1
import json
def hashf(value):
    return sha1(value.encode('utf-8')).hexdigest() #use hex for encoding simplicty 

class root:
    def __init__(self):
        self.h = hashf("I am the alpha and the omega")
    def digest(self):
        return self.h

class magistrate:
    """Handles adding valid entries to the log and sealing them
    through proof of work.

    difficulty  the number of leading zeros the hash must have
    trustdepth  how bar back we confirm blocks before assumming correctness
    root    the genisis hash block 
    """
    def __init__(self, difficulty = 2, trustdepth = 1, root = root()):
        self.difficulty = difficulty
        self.root = root
        self.current = root
        self.blocks = []
        self.current_block = block(root)
        self.trustdepth = trustdepth

    def doWork(self,bl):
        h = b'\hff' #placeholder initial hash

        while( h[:self.difficulty].count(b'\0') < self.difficulty):
            bl.nonce += 1
            h = bytes.fromhex(bl.digest())
        return h,bl.nonce

    def handleEntry(self,e):
        if self.validateEntry(e):
            self.current_block.addEntry(e)

    def handleNewBlock(block):
        if block.validate:
            self.blocks.append(block)     
            #FIXME need to remove entries from current block that hold entries commited in this block

    def seal(self):
        b = self.current_block
        self.current_block = block(b)
        h,nonce = self.doWork(b)
        self.blocks.append(b)
    
    def validateEntry(self,e):
        for b in self.blocks[:self.trustdepth] + [self.current_block]:
            if not b.validateEntry(e):
                return False
        return True

class block:
    def __init__(self,prev):
        self.entries = []
        self.nonce = 0
        self.prevhash = prev.digest();

    def addEntry(self, e):
        self.entries.append(e)

    def digest(self):
        #FIXME no need to recompute serialization of block each time.
        return hashf(self.toJson())

    def validateEntry(self,e):
        for en in self.entries:
            if not en.validateEntry(e):
                return False 
        return True

    def toJson(self):
        d = {'nonce':self.nonce,'prevhash':self.prevhash,'entries':list(map(lambda e:e.toJson(),self.entries))}
        return json.dumps(d)

class entry:
    def __init__(self,serial_number,data):
        self.data = data
        self.serial_number = serial_number

    def validateEntry(self,e):
        return not self.serial_number == e.serial_number
    
    def toJson(self):
        d = {'serial_number':self.serial_number,'data':self.data}
        return json.dumps(d)

    def __str__():
        return serial_number + "|" + data

if __name__== "__main__":
    m = magistrate()
    m.handleEntry(entry(1,"a"))
    m.handleEntry(entry(2,"b"))
    m.seal()
    for i in m.blocks:
        print(i.digest())
