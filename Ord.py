class Ord:
    def __init__(self, felboejt_verb):
        self.fbv = felboejt_verb
        self.tempus = None
        self.passiv = False
        self.raettning = None
        self.kraanglighet = 0

        if (self.fbv[len(self.fbv)-1:] == 's'):
            self.raettning = self.fbv[:len(self.fbv) - 1]
            self.passiv = True
        else:
            self.raettning = self.fbv
            if (self.fbv[:3] == 'umg') or (self.fbv[:4] == 'triv') or (self.fbv[:4] == 'lyck') or (self.fbv[:6] == 'missly') or (self.fbv[:6] == 'handsk') or (self.fbv[:3] == 'min') or (self.fbv[:3] == 'väs'):
                self.passiv = True
            else:
                self.passiv = False
        
        """
        krånglighetsbarometer:
        0 = ordet finns i verblistan, bara att hämta ut
        1 = endast ändelsen behövde korrigeras med hjälp av en enkelt identifierbar rot
        2 = en vokal var fel
        3 = 1 + 2
        4 = en konsonant behövde dubbleras eller en dubblad konsonant behövde tas bort
        5 = 4 + 1
        6 = ordet finns inte i verblistan, kunde inte korrigeras men finns i den stora ordlistan
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
