
# -*- coding: utf-8 -*-

#21oktober


class VerbDetektiv:
    def __init__(self, verbfil, ordboksfil):
        self.verbl = self.skapa_verblista(verbfil)
        self.ordbok = self.skapa_ordbok(ordboksfil)        

    def skapa_verblista(self, fil):
        verben_paa_fil = open(fil, 'r')
        rad = verben_paa_fil.readline().split()
        verbl = {rad[0]: (rad[1], rad[2], rad[3])}
        while True:
            try:
                rad = verben_paa_fil.readline().split()
                verbl[rad[0]] = (rad[1], rad[2], rad[3])
            except IndexError:
                print(rad)
                break                
    
        verben_paa_fil.close()
        return verbl

    def skapa_ordbok(self, fil):
        ordbok_paa_fil = open(fil, 'r')
        ordlista = ordbok_paa_fil.readlines()
        x = 0
        while x< len(ordlista):
            ordlista[x] = ordlista[x].strip('\n')
            x += 1
        ordbok_paa_fil.close()
        return ordlista
        
    def raetta(self, felboejt_verb):

        if felboejt_verb.specialpassiv == False:
            raettad_form = self.slaa_upp(felboejt_verb)
        else:
            raettad_form = None

        if raettad_form != None:
            print ("Inget fel!")
            felboejt_verb.raettning = raettad_form
            return felboejt_verb.raettning
        else:
            felboejt_verb.kraanglighet += 1
            raettad_form = self.aendelseanalys(felboejt_verb)

        if raettad_form == None:
            felboejt_verb.kraanglighet += 1
            raettad_form = self.vokalfel(felboejt_verb) # kollar vokalfel

        if raettad_form == None:
            felboejt_verb.kraanglighet += 2
            raettad_form = self.dblkonsfel(felboejt_verb) # kollar dubbelkonsonantfel

        if raettad_form != None:
            if felboejt_verb.passiv == True:
                if felboejt_verb.raettning[len(felboejt_verb.raettning) - 1:] == 'r':
                    felboejt_verb.raettning = felboejt_verb.raettning[:len(felboejt_verb.raettning) - 1]
                felboejt_verb.raettning = felboejt_verb.raettning + 's'
            #print("felboejt_verb.kraanglighet: " + str(felboejt_verb.kraanglighet))
            return felboejt_verb.raettning
        else:
            raettad_form = (self.sista_koll(felboejt_verb))
            if raettad_form:
                return raettad_form
        return "Inget hittat\n\n"

    def slaa_upp(self, felboejt_verb):

        print("inne i slå upp-metoden!")
        print("kraanglighet: " + str(felboejt_verb.kraanglighet))
        for infinitiv in self.verbl.keys():
            if felboejt_verb.raettning == infinitiv:
                felboejt_verb.saetta_tempus(-1)
                return infinitiv
            elif felboejt_verb.kraanglighet != 1:
                tempusindx = 0
                for boejning in self.verbl[infinitiv]:
                    if felboejt_verb.raettning == boejning:
                        felboejt_verb.saetta_tempus(tempusindx)
                        return boejning
                    tempusindx += 1
        return None

    def aendelseanalys(self, felboejt_verb):
        print("felboejt_verb.raettning: " + felboejt_verb.raettning)
        ordets_laengd = len(felboejt_verb.raettning)
        raettad_form = None
        
        if felboejt_verb.raettning[ordets_laengd - 2:] == "ar":
            felboejt_verb.saetta_tempus(0)
            raettad_form = self.grupp1(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd - 3:] == "ade":
            felboejt_verb.saetta_tempus(1)
            raettad_form = self.grupp1(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd - 2:] == "at":
            felboejt_verb.saetta_tempus(2)
            raettad_form = self.grupp1(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd - 3:] == "dde":
            felboejt_verb.saetta_tempus(1)
            raettad_form = self.grupp2(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd - 3:] == "tt":
            felboejt_verb.saetta_tempus(2)
            raettad_form = self.grupp2(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd - 3:] == "ede":
            felboejt_verb.saetta_tempus(1)
            raettad_form = self.slut_ede(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd - 2:] == "er":
            felboejt_verb.saetta_tempus(0)
            raettad_form = self.grupp3(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd - 2:] == "de" or felboejt_verb.raettning[ordets_laengd - 2:] == "te":
            felboejt_verb.saetta_tempus(1)
            raettad_form = self.grupp3(felboejt_verb)
            if (raettad_form == None) and (felboejt_verb.raettning[ordets_laengd - 3:] == 'rde'):
                raettad_form = self.slut_rde(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd - 2:] == "it":
            felboejt_verb.saetta_tempus(2)
            raettad_form = self.grupp3(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd-1:] == "t":
            felboejt_verb.saetta_tempus(2)
            raettad_form = self.grupp3(felboejt_verb)
            if raettad_form == None:
                raettad_form = self.laegg_till_er(felboejt_verb)

        elif felboejt_verb.raettning[ordets_laengd - 1] == 'e':
            raettad_form = self.slut_e(felboejt_verb)
        else:
            print("ingen aendelse identifierad")
            if (felboejt_verb.raettning[len(felboejt_verb.raettning)-1:]) not in ('a', 'i', 'o', 'u', 'y', 'å', 'ä', 'ö'):
                raettad_form = self.laegg_till_er(felboejt_verb)

        if raettad_form:
            felboejt_verb.kraanglighet += 1
            felboejt_verb.raettning = raettad_form
                    
        return raettad_form

    def kolla_med_stavningsjustering(self, felboejt_verb):
        if (self.slaa_upp(felboejt_verb)):
            felboejt_verb.kraanglighet += 1
            return felboejt_verb.raettning
        elif (self.aendelseanalys(felboejt_verb)):
            felboejt_verb.kraanglighet += 2
            return felboejt_verb.raettning
        else:
            return None

    def grupp1(self, felboejt_verb):
        print ("grupp1-metoden")
        aendelselaengd = 1
        if felboejt_verb.tempus == 1:
            aendelselaengd += 1

        rot = felboejt_verb.raettning[:len(felboejt_verb.raettning) - aendelselaengd]

        if rot in self.verbl.keys():
            return (self.verbl[rot][felboejt_verb.tempus])
        else:
            return None

    def grupp2(self, felboejt_verb):
        print ("grupp2-metoden")
        aendelselaengd = 2
        if felboejt_verb.tempus == 1:
            aendelselaengd += 1
        rot = felboejt_verb.raettning[:len(felboejt_verb.raettning) - aendelselaengd]
        if rot in self.verbl.keys():
            return (self.verbl[rot][felboejt_verb.tempus])
        else:
            return None

    def grupp3(self, felboejt_verb):
        aendelselaengd = 2
        if felboejt_verb.tempus == 2:
            aendelselaengd -= 1
        rot = felboejt_verb.raettning[:len(felboejt_verb.raettning) - aendelselaengd] + 'a'  # vikte - vika
        
        if rot in self.verbl.keys():
            return (self.verbl[rot][felboejt_verb.tempus])
        else:
            if rot[:len(rot) - 1] in self.verbl.keys():  # gåde - gå
                rot = rot[:len(rot) - 1]
            else:  # brinde - brinna
                konsonant_att_dubblas = felboejt_verb.raettning[
                                        len(felboejt_verb.raettning) - (aendelselaengd+1):len(felboejt_verb.raettning) - aendelselaengd]
                konsonantdubblad_rot = (felboejt_verb.raettning[:len(felboejt_verb.raettning) - aendelselaengd] + konsonant_att_dubblas + 'a')
                if konsonantdubblad_rot in self.verbl.keys():
                    rot = konsonantdubblad_rot
                else:
                    tonande_konsonanter = ('b', 'g', 'j', 'l', 'm', 'n', 'r', 'v')
                    tonloesa_konsonanter = ('f', 'k', 'p', 's', 'x')
                    if rot[len(rot)-2] in tonande_konsonanter:
                        rot_med_tillaegg = rot[:len(rot)-1] + 'd' + 'a'
                        if rot_med_tillaegg in self.verbl.keys():
                            rot = rot_med_tillaegg
                        else:
                            return None
                    elif rot[len(rot)-2] in tonloesa_konsonanter:
                        rot_med_tillaegg = rot[:len(rot)-1] + 't' + 'a'
                        if rot_med_tillaegg in self.verbl.keys():
                            rot = rot_med_tillaegg
                        else:
                            return None
                    else:                   
                        return None
        return None

    def slut_rde(self, felboejt_verb):
        print ("rde-metoden")
        uo = felboejt_verb.raettning
        felboejt_verb.raettning = felboejt_verb.raettning[:len(felboejt_verb.raettning)-3] + felboejt_verb.raettning[len(felboejt_verb.raettning)-2:]
        print(felboejt_verb.raettning)
        #behöverde -> behövede
        
        if (self.kolla_med_stavningsjustering(felboejt_verb)):
            return felboejt_verb.raettning
        else:
            felboejt_verb.raettning = uo
            return None
       
    def slut_e(self, felboejt_verb):
        uo = felboejt_verb.raettning

        felboejt_verb.raettning += 'r'
        print("i slut_e-metoden, är uo just nu: " + uo)
        if (self.kolla_med_stavningsjustering(felboejt_verb)):
            felboejt_verb.saetta_tempus(0)
            return felboejt_verb.raettning
        felboejt_verb.tempus = -1
        felboejt_verb.raettning = uo[:len(uo)-1]
        if (self.kolla_med_stavningsjustering(felboejt_verb)):
            return felboejt_verb.raettning
        felboejt_verb.raettning = uo[:len(uo) - 1] + 'a'
        felboejt_verb.saetta_tempus(0)
        if (self.kolla_med_stavningsjustering(felboejt_verb)):
            felboejt_verb.saetta_tempus(-1)
            return felboejt_verb.raettning
        return None

    def slut_ede(self, felboejt_verb):
        felboejt_verb.raettning = felboejt_verb.raettning[:len(felboejt_verb.raettning) - 3] + "ade"
        raettat_ord = self.grupp1(felboejt_verb)
        return raettat_ord

    def laegg_till_er(self, felboejt_verb):
        uo = felboejt_verb.raettning
        felboejt_verb.raettning = felboejt_verb.raettning + 'er'
        felboejt_verb.saetta_tempus(0)
        raettad_form = self.grupp3(felboejt_verb)
        if (raettad_form):
            return raettad_form
        else:
            felboejt_verb.raettning = uo
            felboejt_verb.saetta_tempus(None)
            return None
        

    def vokalfel(self, felboejt_verb):
        provvokaler = []
        uo = felboejt_verb.raettning  # sparar ursprungliga raettningsattributet i variabel uo (ursprungligt ord)
        indx = 0
        for bokstav in uo:
            provvokaler = self.generera_provvokaler(bokstav)
            if provvokaler == None:
                indx += 1
                continue
            for vokal in provvokaler:
                felboejt_verb.raettning = uo[:indx] + vokal + uo[indx + 1:]
                #print("felboejt_verbs rättning med vokaljustering: " + felboejt_verb.raettning)
                if self.kolla_med_stavningsjustering(felboejt_verb) != None:
                    return felboejt_verb.raettning
                
            indx += 1

        felboejt_verb.raettning = uo
        return None

    def generera_provvokaler(self, bokstav):
        provvokaler = []
        if bokstav == 'a':
            provvokaler = ['å', 'ä', 'ö']
        elif bokstav == 'e':
            provvokaler = ['u', 'ä', 'i']
        elif bokstav == 'i':
            provvokaler = ['y', 'e']
        elif bokstav == 'o':
            provvokaler = ['ö', 'å', 'u']
        elif bokstav == 'u':
            provvokaler = ['ö', 'o', 'y', 'e']
        elif bokstav == 'y':
            provvokaler = ['i', 'e']
        elif bokstav == 'å':
            provvokaler = ['a', 'o', 'ä', 'ö']
        elif bokstav == 'ä':
            provvokaler = ['a', 'e', 'å', 'u']
        elif bokstav == 'ö':
            provvokaler = ['a', 'o', 'u', 'å']
        else:
            provvokaler = None
        return provvokaler

    def dblkonsfel(self, felboejt_verb):
        # kollar dubbelkonsonantfel
        vokaler = ('a', 'e', 'i', 'o', 'u', 'y', 'å', 'ä', 'ö')

        uo = felboejt_verb.raettning
        indx = 1
        while indx < len(uo):
            if uo[indx] not in vokaler:
                if uo[indx] == 'k':
                    felboejt_verb.raettning = uo[:indx] + 'c' + uo[indx:]
                else:
                    felboejt_verb.raettning = uo[:indx] + uo[indx] + uo[indx:]
                if self.kolla_med_stavningsjustering(felboejt_verb) != None:
                    return felboejt_verb.raettning
            if indx < len(uo):
                indx += 1

        indx = 0
        while indx < len(uo)-1:
            if uo[indx] not in vokaler:
                if (uo[indx] == uo[indx+1]) or (uo[indx] == 'c' and uo[indx+1] == 'k'):
                    felboejt_verb.raettning = uo[:indx] + uo[indx+1:]
                    if self.kolla_med_stavningsjustering(felboejt_verb) != None:
                        return felboejt_verb.raettning
            if indx < len(uo):
                indx += 1

        felboejt_verb.raettning = uo
        return None

    def sista_koll(self, felboejt_verb):
        for glosa in self.ordbok:
            if felboejt_verb.fbv == glosa.lower():
                print("ditt ord finns, men vi kunde inte rätta det...")
                return felboejt_verb.fbv
        else:
            print("nepp")
            return None
        

class Ord:
    def __init__(self, felboejt_verb):
        self.fbv = felboejt_verb
        self.tempus = None
        self.passiv = False
        self.specialpassiv = False
        self.raettning = None
        self.kraanglighet = 0

        if (self.fbv[len(self.fbv)-1:] == 's'):
            self.raettning = self.fbv[:len(self.fbv) - 1]
            self.passiv = True
        else:
            self.raettning = self.fbv
            if (self.fbv[:3] == 'umg') or (self.fbv[:4] == 'triv') or (self.fbv[:4] == 'lyck') or (self.fbv[:6] == 'missly') or (self.fbv[:6] == 'handsk') or (self.fbv[:3] == 'min') or (self.fbv[:3] == 'väs'):
                self.passiv = True
                self.specialpassiv = True
            else:
                self.passiv = False
        
        """
        krånglighetsbarometer:
        0 = det skrivna ordet finns i verblistan, bara att hämta ut
        1 = endast ändelsen behövde korrigeras med hjälp av en enkelt identifierbar rot
        2 = en vokal var fel
        3 = 1 + 2
        4 = en konsonant behövde dubbleras eller en dubblad konsonant behövde tas bort
        5 = 4 + 1
        """

        # pratade -> Passiv False + raettning = fbv
        # pratades -> Passiv True + raettning = fbv-s
        # umgådde -> Passiv True + raettning = fbv
        # umgåddes -> Passiv False + raettning = fbv-s
        
    def saetta_tempus(self, tempus):
        # infinitiv: -1
        # presens:0
        # imperfekt: 1
        # particip: 2
        self.tempus = tempus

if __name__ == "__main__":

    vd = VerbDetektiv('verben.txt', 'SWE.dict.txt')

    ord_foer_analys = str(input('\nSkriv ett verb!\n\n'))
    
    while ord_foer_analys != '00':
        o = Ord(ord_foer_analys.lower())
        print(vd.raetta(o))
        print (o.kraanglighet)
        ord_foer_analys = str(input('\n\nSkriv ett verb till!\n(00 för att avsluta)\n'))

