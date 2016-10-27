
from Ord import Ord
from vd import VerbDetektiv

def skapa_indatalista(textfil):
    tmpfil = open(textfil, 'r')
    ind = tmpfil.readlines()
    indatalista = []
    
    for rad in ind:
        try:
            verb_med_anotering = rad.split('\t')
            verb_med_anotering[1] = verb_med_anotering[1].strip('\n')
            indatalista.append(verb_med_anotering)
        except(IndexError):
            pass

    tmpfil.close()
    return indatalista

def koera(verbdetektiv, lista_med_indata):
    
    nollor = ettor = tvaaor = sexor = missar = totalmissar = okurrenser = 0
    
    for par in lista_med_indata:
        o = Ord(par[0].lower())
        raettning = verbdetektiv.raetta(o)
        try:
            okurrenser += 1
            if raettning == par[1].lower():
                if o.kraanglighet == 0:
                    nollor += 1
                elif o.kraanglighet == 1:
                    ettor += 1
                    #print(par[0] + '\t' + raettning.lower() + '\t' + par[1].lower())
                elif o.kraanglighet == 6:
                    sexor += 1
                else:
                    tvaaor += 1
                    #print(par[0] + '\t' + raettning.lower() + '\t' + par[1].lower())
            elif raettning == '00' and o.kraanglighet == 7:
                totalmissar += 1
                #print(par[0] + '\t' + raettning + '\t' + par[1].lower())
            else:
                missar += 1
                #print(par[0] + '\t' + raettning + '\t' + par[1].lower())
        except (IndexError):
            pass

    print ("nollor: " + str(nollor))
    print ("ettor: " + str(ettor))
    print ("tvaa-femmor: " + str(tvaaor))
    print ("sexor: " + str(sexor))
    print ("missar: " + str(missar))
    print ("totalmissar: " + str(totalmissar))

    procent_raett = (float(nollor + ettor + tvaaor + sexor) / okurrenser) * 100

    return(procent_raett)

if __name__ == "__main__":
    print ("Vänligen vänta...")
    vd = VerbDetektiv('verben.txt', 'SWE.dict.txt')

    lista_med_indata = skapa_indatalista("Indata_klar.txt")

    print( str(koera(vd, lista_med_indata) ) + "% har blivit rätt")
    
    """nollor = ettor = tvaaor = sexor = missar = totalmissar = okurrenser = 0
    
    for par in lista_med_indata:
        o = Ord(par[0].lower())
        raettning = vd.raetta(o)
        try:
            okurrenser += 1
            if raettning == par[1].lower():
                if o.kraanglighet == 0:
                    nollor += 1
                elif o.kraanglighet == 1:
                    ettor += 1
                    #print(par[0] + '\t' + raettning.lower() + '\t' + par[1].lower())
                elif o.kraanglighet == 6:
                    sexor += 1
                else:
                    tvaaor += 1
                    #print(par[0] + '\t' + raettning.lower() + '\t' + par[1].lower())
            elif raettning == '00' and o.kraanglighet == 7:
                totalmissar += 1
                print(par[0] + '\t' + raettning + '\t' + par[1].lower())
            else:
                missar += 1
                print(par[0] + '\t' + raettning + '\t' + par[1].lower())
        except (IndexError):
            pass

    
    print ("nollor: " + str(nollor))
    print ("ettor: " + str(ettor))
    print ("tvaa-femmor: " + str(tvaaor))
    print ("sexor: " + str(sexor))
    print ("missar: " + str(missar))
    print ("totalmissar: " + str(totalmissar))"""
