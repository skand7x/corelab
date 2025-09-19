import string


# Statistical Moments (mean as example for key)
def statistical_moments(data):
    # Takes a list of integers, returns the mean
    return sum(data) / len(data)


# Playfair Cipher Implementation
def create_playfair_square(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # I/J are merged
    key_string = ""
    for char in key.upper():
        if char not in key_string and char in alphabet:
            key_string += char
    for char in alphabet:
        if char not in key_string:
            key_string += char
    square = [list(key_string[i * 5 : (i + 1) * 5]) for i in range(5)]
    return square


def pair_message(msg):
    msg = msg.upper().replace("J", "I")
    pairs = []
    i = 0
    while i < len(msg):
        a = msg[i]
        b = ""
        if i + 1 < len(msg):
            b = msg[i + 1]
            if a == b:
                b = "X"
                i += 1
            else:
                i += 2
        else:
            b = "X"
            i += 1
        pairs.append(a + b)
    return pairs


def find_position(square, letter):
    for row_idx, row in enumerate(square):
        if letter in row:
            return (row_idx, row.index(letter))
    return None


def playfair_encrypt(msg, key):
    square = create_playfair_square(key)
    pairs = pair_message(msg)
    encrypted = ""
    for pair in pairs:
        a_pos = find_position(square, pair[0])
        b_pos = find_position(square, pair[1])
        if a_pos[0] == b_pos[0]:  # Same row
            encrypted += square[a_pos[0]][(a_pos[1] + 1) % 5]
            encrypted += square[b_pos[0]][(b_pos[1] + 1) % 5]
        elif a_pos[1] == b_pos[1]:  # Same column
            encrypted += square[(a_pos[0] + 1) % 5][a_pos[1]]
            encrypted += square[(b_pos[0] + 1) % 5][b_pos[1]]
        else:
            encrypted += square[a_pos[0]][b_pos[1]]
            encrypted += square[b_pos[0]][a_pos[1]]
    return encrypted


def playfair_decrypt(cipher, key):
    square = create_playfair_square(key)
    pairs = pair_message(cipher)
    decrypted = ""
    for pair in pairs:
        a_pos = find_position(square, pair[0])
        b_pos = find_position(square, pair[1])
        if a_pos[0] == b_pos[0]:  # Same row
            decrypted += square[a_pos[0]][(a_pos[1] - 1) % 5]
            decrypted += square[b_pos[0]][(b_pos[1] - 1) % 5]
        elif a_pos[1] == b_pos[1]:  # Same column
            decrypted += square[(a_pos[0] - 1) % 5][a_pos[1]]
            decrypted += square[(b_pos[0] - 1) % 5][b_pos[1]]
        else:
            decrypted += square[a_pos[0]][b_pos[1]]
            decrypted += square[b_pos[0]][a_pos[1]]
    return decrypted


# Mixed Alphabet Cipher
def mixed_alphabet_encrypt(text, key):
    alphabet = string.ascii_uppercase
    key_nodup = "".join(sorted(set(key.upper()), key=lambda x: key.upper().index(x)))
    full_key = key_nodup + "".join([c for c in alphabet if c not in key_nodup])
    table = str.maketrans(alphabet, full_key)
    return text.upper().translate(table)


def mixed_alphabet_decrypt(cipher, key):
    alphabet = string.ascii_uppercase
    key_nodup = "".join(sorted(set(key.upper()), key=lambda x: key.upper().index(x)))
    full_key = key_nodup + "".join([c for c in alphabet if c not in key_nodup])
    table = str.maketrans(full_key, alphabet)
    return cipher.upper().translate(table)


# XOR for Key Generation
def split_data(data):
    midpoint = len(data) // 2
    return data[:midpoint], data[midpoint:]


def xor_key(p1, p2):
    return bytes([a ^ b for a, b in zip(p1, p2)])


# Example usage
if __name__ == "__main__":
    # Plaintext and key setup
    plaintext = "HELLODRILLSCENE"
    key = "KINGVON"

    # Playfair encryption
    playfair_cipher = playfair_encrypt(plaintext, key)
    print("Playfair Encrypted:", playfair_cipher)

    # Playfair decryption
    playfair_decrypt_text = playfair_decrypt(playfair_cipher, key)
    print("Playfair Decrypted:", playfair_decrypt_text)

    # Mixed alphabet encryption
    mixed_encrypted = mixed_alphabet_encrypt(plaintext, key)
    print("Mixed Alphabet Encrypted:", mixed_encrypted)

    # Mixed alphabet decryption
    mixed_decrypted = mixed_alphabet_decrypt(mixed_encrypted, key)
    print("Mixed Alphabet Decrypted:", mixed_decrypted)

    # Using statistical moments for key (example over ASCII values of key chars)
    ascii_values = [ord(c) for c in key]
    stat_key = statistical_moments(ascii_values)
    print("Statistical Moment Key (Mean):", stat_key)

    # Split data and XOR (using image/data in bytes)
    image_data = b"\x01\x23\x45\x67\x89\xab\xcd\xef"  # Example binary data
    p1, p2 = split_data(image_data)
    print("P1:", p1)
    print("P2:", p2)
    xor_result = xor_key(p1, p2)
    print("XOR Key:", xor_result)
