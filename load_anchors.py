import os

#Wrapper class to hold anchors.
class AnchorList:
    def __init__(self):
        self.p = []
        self.name = ""
        self.score = 0

#Wrapper class to hold lists of anchors.
class QueryList:
    def __init__(self):
        self.l = []
    
    def merge(self, ql):
        self.l += ql

    #Get all of the anchors from all of the queries
    def anchors(self):
        for l in self.l:
            for p in l.p:
                yield p

#Parse a directory full of FASTQ query files containing quality scores
#Decode the ASCII quality scores and compute an average quality for each read (query)
#This may be used as metadata to assist with alignment in later stages
# filedir: full path to a directory to scan through
def read_quality(filedir):
    q_scores = {}
    for fn in os.listdir(filedir):
        fp = os.path.join(filedir, fn)
        try:
            with open(fp) as f:
                is_qs = False
                name = ''
                for line in f.readlines():
                    if is_qs:
                        q_scores[name] = sum([ord(c) for c in line.strip()]) / len(line.strip())
                        is_qs = False
                    elif line.startswith('+'):
                        is_qs = True #Next line is a quality score
                    elif line.startswith('@'):
                        name = line.split(' ')[0][1:]
                        is_qs = False

        except IOError as e:
            print(e)
            exit()
    return q_scores

#Reads all of the anchors exported by minimap2 and loads them, by query
#filepath specifies the full file path to the file in question
#This function currently only handles anchors for one reference
# filepath: Full path to a FASTQ file
# readall: Boolean, consider all reads in the file?
# max_quers: If readall=False, then specify a max number of queries
# q_scores: Consider quality score data output from read_quality 
def load_anchors(filepath, readall=True, max_quers=0):
    try:
        with open(filepath) as f:
            q_cnt = 0
            queries = QueryList()
            header_last = False
            while True:
                line = f.readline()
                if line.startswith("@") or line == "": #If this line is a header line
                    if q_cnt != 0 and not header_last:
                        queries.l.append(q) #Add the query that was last built, if it exists
                    if line == "" or (not readall and q_cnt == max_quers):
                        break
                    q = AnchorList()  
                    q_cnt = q_cnt + 1
                    q.name = line[1:].strip()
                    if q_scores != None:
                        q.score = q_scores[q.name]
                    header_last = True
                else: #Otherwisem it is a data line, so add it to the current query
                    ls = line.split(',')
                    q.p.append((int(ls[0], 16), int(ls[1], 16)))
                    header_last = False
    except IOError as e:
        print(e)
        exit()
    return queries