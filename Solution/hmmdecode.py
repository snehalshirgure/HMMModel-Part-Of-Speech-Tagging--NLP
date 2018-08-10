import json

def main():

    f1 = open("hmmmodel.txt", "r" , encoding="utf-8")
    f2 = open("en_dev_raw.txt", "r", encoding="utf-8")
    f3 = open("hmmoutput.txt", "w+" , encoding="utf-8")

    d_start={}
    d_trans={}
    d_emis = {}

    if f1.mode=="r":
        ff = f1.readlines()
        for lines in ff:
            jfile = json.loads(lines,encoding="utf-8")
            d_start = jfile["start_prob"]
            d_trans = jfile["trans_prob"]
            d_emis = jfile["emis_prob"]

    if f2.mode=="r":
        fl = f2.readlines()
        for line in fl:
            #print(line)
            totagline = line
            totagwords = totagline.split()
            wordcount = len(totagwords)
            taglist = []

            for i,nw in enumerate(totagwords):
                #print(" word : " + nw)
                if(i==0):     
                    if(nw in d_emis):
                        d_word_to_tag = d_emis[nw]
                        d_entry = {}
                        for tagkey in d_word_to_tag:
                            if(tagkey in d_start):
                                prob = d_start[tagkey] * d_word_to_tag[tagkey]
                            else:
                                prob = 0
                            d_entry [tagkey] = [ "start" , prob ]
                        
                        taglist.append(d_entry)
                    
                    else:
                        print("handle smoothing here")
                else:
                    if(nw in d_emis):
                        d_word_to_tag = d_emis[nw]
                        d_entry = {}
                        for tagkey in d_word_to_tag:
                            d_prev = taglist[i-1]
                            
                            for prevtag in d_prev:

                                if(tagkey in d_trans[prevtag]):
                                    prob =  d_prev[prevtag][1]* d_trans[prevtag][tagkey]*d_word_to_tag[tagkey]
                                else:
                                    prob =0
                                #print(prob)
                                if tagkey not in d_entry:
                                   d_entry[tagkey] = [ prevtag , prob ]
                                else:
                                    t = d_entry[tagkey]
                                    if t[1] < prob:
                                        d_entry[tagkey] = [ prevtag , prob ]
                        
                        taglist.append(d_entry)                                
                                    
                    else:
                        print("handle smoothing here")

        
            l = len(taglist)

            for tk in taglist[l-1]:
                t = taglist[l-1][tk]
                maxprob = t[1]
                lasttag = tk

            for tk in taglist[l-1]:
                t = taglist[l-1][tk]
                if t[1] < maxprob:
                    maxprob = t[1]
                    lasttag = tk
        
        
            linetag = []

            for x in range(1,l+1):
               #print(str(taglist[l - i]))
               linetag.append(str( totagwords[ l  - x ] +"/" +lasttag ))
               lasttag = taglist[l-x][lasttag][0]
                #lasttag = taglist[l-i-1][lasttag][0]

            string = ""
            for y in range(1,l):
                string+=linetag[l-y]+" "
            
            string+=linetag[0] + "\n"
            f3.write(string)
        

    
    


        


if  __name__ ==  "__main__":
    main()