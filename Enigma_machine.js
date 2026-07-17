function rotor_encode(char, wiring, offset){
    let ascii = char.charCodeAt(0);
    let index = (((((ascii - 65) + offset)% 26)+ 26) % 26);
    let substituted = wiring.charAt(index);
    let result = (((((substituted.charCodeAt(0) -65) - offset)%26)+26)%26);
    let finalCharacter = result +65;
    return String.fromCharCode(finalCharacter);

}

let first = rotor_encode('A', "EKMFLGDQVZNTOWYHXUSPAIBRCJ", 0) 
let second = rotor_encode('A', "EKMFLGDQVZNTOWYHXUSPAIBRCJ", 1) 
let third = rotor_encode('B', "EKMFLGDQVZNTOWYHXUSPAIBRCJ", 0)

console.log(first,second,third);