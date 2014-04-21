import sys, os
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

def init():
    path = []
    with open("config.exp0", "r") as f:
        path = f.readlines()
    home = path[0].rstrip("\n")
    out  = path[1].rstrip("\n")
    home_map = {"doc"     : "doc",
                "topics"  : "topics",
                "qrels"   : "qrels",
                "treceval": "trec_eval.9.0",
                "lucene"  : "lucene.TREC",
                "terrier" : "terrier-3.5",
                "indri"   : "indri-5.6",
                "utils"   : "utils"}
    out_map = {"index" : "index",
               "runs"  : "runs",
               "evals" : "evals",
               "attic" : "attic"}
    env = {}
    for k in home_map.keys():
        env[k] = os.path.join(home, home_map[k])
    for k in out_map.keys():
        env[k] = os.path.join(out, out_map[k])
    return env

def exp0(opt):

    env = init();

    models = ["bm25","dfi0", "dirichletlm", "lemurtf_idf", "tf_idf"]

    stems  = ["n", "p"]

    doc    = {"t678": os.path.join(env["doc"], "trec678"),
              "t678-fr": os.path.join(env["doc"], "trec678-fr"),
              "fr94": os.path.join(env["doc"], "cd4/fr94"),
              "ziff": os.path.join(env["doc"], "ziff")}

    topics = {"t678": os.path.join(env["topics"], "topics.301-450"),
              "t123": os.path.join(env["topics"], "topics.1-150")}

    qrels  = {"t678": os.path.join(env["qrels"], "qrels.trec678.adhoc"),
              "t6": os.path.join(env["qrels"], "qrels.trec6.adhoc"),
              "t7": os.path.join(env["qrels"], "qrels.trec7.adhoc"),
              "t8": os.path.join(env["qrels"], "qrels.trec8.adhoc"),
              "ziff": os.path.join(env["qrels"], "qrels.trec12.adhoc")}

    s = SysTerrier(env)

    # {"runid": "index topic qrel"}
    tag = {"t6": "t678 t678 t6",
           "t7": "t678 t678 t7",
           "t8": "t678 t678 t8",
           "t678-fr": "t678-fr t678 t678",
           "fr94": "fr94 t678 t678",
           "ziff1": "ziff t123 ziff",
           "ziff2": "ziff t123 ziff"}

    if opt == "i":
        # pull out the index names
        a = []
        for i in tag.values():
            a.append(i.split()[0])
        index = list(set(a))
        for i in index:
            for j in stems:
                s.index(i+"."+j,  doc[i], ["stop", j])
    elif opt == "r":
        for i in tag.keys():
            i_ = tag[i].split()
            t = Topics(topics[i_[1]])
            qid = open(os.path.join(env["topics"],  i+".qid"), "r").read().splitlines()
            q = t.query("terrier", "d", qid)
            for j in stems:
                for k in models:
                    s.retrieve(i_[0]+"."+j,  i+"."+j+"."+k, ["stop", j], k, q)
    elif opt == "e":
        for i in tag.keys():
            i_ = tag[i].split()
            for j in stems:
                for k in models:
                    s.evaluate(i+"."+j+"."+k, qrels[i_[2]])

def main(argv):
    if len(argv) != 2:
        print "usage: python setup.py <i|r|e>"
        sys.exit(0)
    if not (os.path.exists(env["index"]) 
            and os.path.exists(env["runs"]) 
            and os.path.exists(env["evals"])):
        print "Either one of index, runs or evals directory doesn't exist."
        sys.exit(0)

    exp0(argv[1])
    
if __name__ == "__main__":
   main(sys.argv)
