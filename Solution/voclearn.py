import json
import sys

fileinput = "test.txt"   
f = open(fileinput,"r", encoding="utf8")

d_word_tag= { }  #keeps word : tag --> 
d_tag_next_tag = { } #keeps tag to next tag and count --> { tag : { nexttag : count }}
d_tagcount = { } #counts number of tags  --> { tag : count(tag)}

d_trans_count = {} #keeps total tag to nexttags count -- > { tag : count(nexttags) }
starttags = { } # keeps dict of start tags and counts ---> { starttag : count }

if f.mode=="r":
        fl = f.readlines()
        for a in fl:
          
            b = a.split()
            for i,c in enumerate(b):
                d_prev = c.split("/")
                s = ""
                if(len(d_prev)>2):
                    for z in range(0,len(d_prev)-1):
                        if(z == len(d_prev)-2):
                            s += str(d_prev[z])
                        else:
                            s += str(d_prev[z])+"/"
                else:
                    s = d_prev[0]

                word = s
                #print(word)
                tag = d_prev[len(d_prev)-1]

             
                if(i==0):
                 
                    if tag not in starttags:
                        starttags[tag] = 1
                    else:
                        starttags[tag] += 1
                
                if word not in d_word_tag:
                        d_word_tag[word] = { tag : 1 }
                elif word in d_word_tag and tag not in d_word_tag[word]:
                        d_word_tag[word][tag]=  1 
                else:
                        d_word_tag[word][tag] += 1

                if tag not in d_tagcount:
                    d_tagcount[tag] = 1 
                else:
                    d_tagcount[tag] +=1
                

                if(i < len(b)-1 ):
                    d_next = b[i+1].split("/")
                    next_tag = d_next[len(d_next)-1]
                   
                    if tag not in d_tag_next_tag:
                        d_tag_next_tag[tag] = { next_tag : 1 }
                        d_trans_count[tag] = 1
                    elif tag in d_tag_next_tag and next_tag not in d_tag_next_tag[tag]:
                        d_tag_next_tag[tag][next_tag]=  1 
                        d_trans_count[tag] += 1
                    else:
                        d_tag_next_tag[tag][next_tag] += 1
                        d_trans_count[tag] += 1
  
         
total_starttags = 0
for x in starttags:
   total_starttags +=starttags[x] 
    
total_tags = 0
for x in d_tagcount:
   total_tags +=d_tagcount[x] 
       

    #-----------------update probablities for all ------------------------------------------
    
    # start probabilites -----
for x in d_tagcount:
    if x not in starttags:
        starttags[x]=0

for x in starttags:
   starttags[x] = ( starttags[x]+1) / (total_starttags + total_tags)
  # print( x + " " + str(starttags[x]))

    # transmission probabilites -----



for x in d_tagcount:
    if x not in d_tag_next_tag:
            d_tag_next_tag[x] = {}
            d_trans_count[x] = 0

#print(len(d_tag_next_tag))
for x in d_tagcount:
    for y in d_tag_next_tag:
        if x not in d_tag_next_tag[y]:
            d_tag_next_tag[y][x] = 0
    

for tags in d_tag_next_tag:
    for nexttags in d_tag_next_tag[tags]:
        
        #d_tag_next_tag[tags][nexttags] /= d_trans_count[tags]
        d_tag_next_tag[tags][nexttags] = ( d_tag_next_tag[tags][nexttags] + 1 ) / (d_trans_count[tags]+ len(d_tagcount))

    # emission probabilites -----
    
for words in d_word_tag:
    for tags in d_word_tag[words]:
       #d_word_tag[words][tags] = ( d_word_tag[words][tags] + 1 ) / (d_tagcount[tags]+ total_tags )
       d_word_tag[words][tags] /= d_tagcount[tags]

    
data_list = { "start_prob" : starttags , "trans_prob" : d_tag_next_tag , "emis_prob" : d_word_tag  }
    

f2 = open("hmmmodel.txt","w+", encoding="utf8")
    
data = json.dumps(data_list,ensure_ascii=False)
f2.write(data)

