usage:
awk -f ../x/analysis/select.awk t678.* | awk -f ../x/analysis/gather.awk | sort -k1,1 >file

The above line selects measures and gathers them by test collection
and writes files in viz. Run it from within evals directory for neater
output.

awk -f table.awk will work on *.measures in viz to write out a tab
commenting on / off some lines controls prettyprinting, and jumbling
up the positions of the test collection columns.

awk -f table1.awk produces a rearranged output of the above
commenting on / off some printf()'s controls prettyprinting.

tab in viz is the entire results table without headers (output of table.awk)
tab.1 has the same data as tab, but laid out differently (output of table1.awk)
*.rand.* has the test collection columns randomly ordered
*.pretty are readable versions of tab*
*.pretty-hide is the readable version of *.rand.* with test collection names replaced by alphabets

awk -f tab.1.pretty.awk ../../viz/tab.1 hide to pretty print tab.1
with test collection names hidden (substituted by alphabets)

single-measure tables from tab.1 types
sort -k2,2d tab.1 | grep map | grep -v gm_map >tab.1.map


awk '{if($4==1)n[$1]++;if($4==0)r[$1]++}END{for(t in n)print t " " n[t] " " r[t]}' qrels.trec678.adhoc  | sort -nk1,1 >../topics/t678.qid

awk '$4 == 1 && $3 ~ /^FR/{a[$1]++}END{for(t in a)print t " " a[t]}' qrels.trec678.adhoc | sort -nk1,1 >../topics/fr94.qid