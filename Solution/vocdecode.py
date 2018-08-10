import json
import sys

fileinput= "en_dev_raw.txt"
  
f1 = open("hmmmodel.txt", "r" , encoding="utf-8")
f2 = open(fileinput, "r", encoding="utf-8")
f3 = open("hmmoutput.txt", "w+" , encoding="utf-8")

d_start={}
d_trans={}
d_emis={}

if f1.mode=="r":
        ff = f1.readlines()
        for lines in ff[:10]:
            jfile = json.loads(lines,encoding="utf-8")
            d_start = jfile["start_prob"]
            d_trans = jfile["trans_prob"]
            d_emis = jfile["emis_prob"]

if f2.mode=="r":
    fl = f2.readlines()
    for line in fl:
        totagline = line
        totagwords = totagline.split()
        wordcount = len(totagwords)
        taglist = []

        for i,nw in enumerate(totagwords):
                
            if(nw in d_emis):
                d_word_to_tag = d_emis[nw]
                d_entry = {}
                if(i==0):     
                        for tagkey in d_word_to_tag:
                            prob = d_start[tagkey] * d_word_to_tag[tagkey]
                            d_entry [tagkey] = [ "start" , prob ]
                        
                        taglist.append(d_entry)

                else:
                        for tagkey in d_word_to_tag:
                            d_prev = taglist[i-1]
                            
                            for prevtag in d_prev:
                                prob =  d_prev[prevtag][1]*d_trans[prevtag][tagkey]*d_word_to_tag[tagkey]
                                if tagkey not in d_entry:
                                   d_entry[tagkey] = [ prevtag , prob ]
                                else:
                                    t = d_entry[tagkey]
                                    if t[1] < prob:
                                        d_entry[tagkey] = [ prevtag , prob ]
                        
                        taglist.append(d_entry)  
            else:
                d_entry = {}
                if(i==0):     
                        for tagkey in d_start:
                            prob = d_start[tagkey] 
                            d_entry [tagkey] = [ "start" , prob ]

                        taglist.append(d_entry)

                else:
                        for tagkey in d_trans:
                            d_prev = taglist[i-1]
                            for prevtag in d_prev:
                                prob =  d_prev[prevtag][1]*d_trans[prevtag][tagkey]
                                if tagkey not in d_entry:
                                   d_entry[tagkey] = [ prevtag , prob ]
                                else:
                                    t = d_entry[tagkey]
                                    if t[1] < prob:
                                        d_entry[tagkey] = [ prevtag , prob ]
                        
                        taglist.append(d_entry)   
           
        l = len(taglist)     

        maxprob = sys.float_info.min
        for tk in taglist[l-1]:
                t = taglist[l-1][tk]
                #print(lasttag+ "  "+str(t[1]))
                if float(t[1]) > maxprob:
                    maxprob = float(t[1])
                    lasttag = tk


        linetag = []
        for x in range(1,l+1):
               linetag.append(str( totagwords[ l  - x ] +"/" +lasttag ))
               lasttag = taglist[l-x][lasttag][0]

        string = ""
        for y in range(1,l):
                string+=linetag[l-y]+" "

        string+=linetag[0] + "\n"
        f3.write(string)
        