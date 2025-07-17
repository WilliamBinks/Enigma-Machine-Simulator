class Plugboard:
    def __init__(self, wiring_pairs):
        self.mapping = {chr(i + ord("A")): chr(i + ord("A")) for i in range(26)}
        for a, b in wiring_pairs:
            self.mapping[a] = b
            self.mapping[b] = a
    
    def swap(self, letter):
        return self.mapping[letter]


class Rotor:
    def __init__(self, wiring, notch, position=0):
        self.wiring = wiring
        self.position = position 
        self.notch = notch
        self.inverse_wiring = [None] * 26
        for i, c in enumerate(wiring):
            self.inverse_wiring[ord(c) - ord("A")] = chr(i + ord("A"))

    def encode_Forward(self, letter):
        offset = (ord(letter) - ord("A") + self.position) % 26
        encoded_Letter = self.wiring[offset]
        encoded_Offset = (ord(encoded_Letter) - ord("A") - self.position + 26) % 26
        return chr(encoded_Offset + ord("A"))

    def encode_Backward(self, letter):
        offset = (ord(letter) - ord("A") + self.position) % 26
        encoded_Letter = self.inverse_wiring[offset]
        encoded_Offset = (ord(encoded_Letter) - ord("A") - self.position+26) % 26
        return chr(encoded_Offset + ord("A"))

    def step(self):
        self.position = (self.position + 1) % 26
        return chr(self.position + ord("A")) in self.notch


class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, letter):
        return self.wiring[ord(letter) - ord("A")]

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def step_rotors(self):
        rotate_Next = self.rotors[2].step()
        if rotate_Next:
            rotate_Next = self.rotors[1].step()
            if rotate_Next:
                self.rotors[0].step()

    def encrypt_char(self, letter):
        if not letter.isalpha():
            return letter
        
        letter = letter.upper()
        self.step_rotors()
        letter = self.plugboard.swap(letter)

        for rotor in reversed(self.rotors):
            letter = rotor.encode_Forward(letter)

        letter = self.reflector.reflect(letter)

        for rotor in self.rotors:
            letter = rotor.encode_Backward(letter)

        letter = self.plugboard.swap(letter)
        return letter

    def encrypt_message(self, message):
        return "".join(self.encrypt_char(c) for c in message)


rotor_I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch='Q', position=0)
rotor_II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", notch='E', position=0)
rotor_III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", notch='V', position=0)
reflector_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
plugboard = Plugboard([("A","B"),("C","D")])

enigma = EnigmaMachine([rotor_I, rotor_II, rotor_III], reflector_B, plugboard)

ciphertext = enigma.encrypt_message("HELLOWORLD")
print(ciphertext)
