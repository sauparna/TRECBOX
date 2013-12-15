import sys
from Sys import *
from bs4 import BeautifulSoup

#indri-5.0/buildindex/IndriBuildIndex parameter_file
#-corpus.path=/path/to/file_or_directory
#-corpus.class=trectext
#-index=/path/to/repository
#-memory 100M
#-stopper.word=stopword
#-stemmer.name=stemmername
#-field.name=fieldname

#field : a complex element specifying the fields to index as data, eg
#TITLE. This parameter can appear multiple times in a parameter
#file. If provided on the command line, only the first field specified
#will be indexed.

#indri-5.0/runquery/IndriRunQuery query_parameter_file -count=1000 -index=/path/to/index -trecFormat=true > result_file
#-query="apple juice" or -query="#combine(apple juice)"

#TREC queries cannot be fed into Indri directly, punctuations need to
#be removed. One simple strategy is to replace everything that's not a
#number (0x30-0x39) or letter with a space (0x20). However,
#tokenization should be performed similar to how the indexer indexes
#texts. And in Indri, "U.S." will be translated into "us" in the
#indexer.

class SysIndri(Sys):

    def __init__(self, env, doc, topic, model, qrel):
        Sys.__init__(self, env, doc, topic, model, qrel)
        self.sys_id = "I"
        self.index_id = ".".join([self.sys_id, self.doc.name])
        self.run_id = ".".join([self.sys_id, self.doc.name, 
                                self.model.name, self.topic.query])
        self.iparam_f = ".".join(["param", "i", self.index_id])
        self.qparam_f = ".".join(["param", "q", self.run_id])
        self.param = {
            "iparam": os.path.join(self.env["index"], self.iparam_f),
            "index": os.path.join(self.env["index"], self.index_id),
            "topics": os.path.join(self.env["topics"], self.topic.file),
            "qparam": os.path.join(self.env["runs"], self.qparam_f),
            "runs": os.path.join(self.env["runs"], self.run_id),
            "evals": os.path.join(self.env["evals"], self.run_id)
            }

    def index(self):
        # create index dir
        # consider backing up an existing one with a stamp in stead of
        # deleting it
        if os.path.exists(self.param["index"]):
            os.removedirs(self.param["index"])
        os.mkdir(self.param["index"])

        # build and write Indri's index param file

        soup = BeautifulSoup("<parameters></parameters>", "xml")

        T_corpus = soup.new_tag("corpus")
        soup.parameters.append(T_corpus)

        T_path = soup.new_tag("path")
        T_path.string = self.doc.path
        soup.parameters.corpus.append(T_path)

        T_class = soup.new_tag("class")
        T_class.string = "trectext"
        soup.parameters.corpus.append(T_class)

        T_index = soup.new_tag("index")
        T_index.string = self.param["index"]
        soup.parameters.append(T_index)

        # Build the 5 <field> tags

        T_field = soup.new_tag("field")
        soup.parameters.append(T_field)

        T_field = soup.new_tag("field")
        soup.parameters.append(T_field)

        T_field = soup.new_tag("field")
        soup.parameters.append(T_field)

        T_field = soup.new_tag("field")
        soup.parameters.append(T_field)

        T_field = soup.new_tag("field")
        soup.parameters.append(T_field)

        # iterate over 5 <field> tags adding the <name> tag to each

        f_ = soup.parameters.field
        T_name = soup.new_tag("name")
        T_name.string = "TEXT"
        f_.append(T_name)
        
        f_ = f_.find_next_sibling("field")
        T_name = soup.new_tag("name")
        T_name.string = "H3"
        f_.append(T_name)

        f_ = f_.find_next_sibling("field")
        T_name = soup.new_tag("name")
        T_name.string = "DOCTITLE"
        f_.append(T_name)

        f_ = f_.find_next_sibling("field")
        T_name = soup.new_tag("name")
        T_name.string = "HEADLINE"
        f_.append(T_name)

        f_ = f_.find_next_sibling("field")
        T_name = soup.new_tag("name")
        T_name.string = "TTL"
        f_.append(T_name)

        # get rid of the first line of the xml introduced by BeautifulSoup
        with open(self.param["iparam"], "w") as f:
            f.write("\n".join(soup.prettify().split("\n")[1:]))

        sys.exit(0)

        args = {
            "exec": "/home/rup/indri-5.5/buildindex/IndriBuildIndex",
            "param_file": self.param["iparam"]
            }

        subprocess.check_output([args["exec"], args["param_file"]])