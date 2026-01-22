def extract_exact_bit_sequence():

    doc = Document('test_04.docx')

    bit_sequence = []

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            for char in run.text:
                if char == '\n':
                    continue

                if run.font.size:
                    if run.font.size == 152400:
                        bit_sequence.append('0')
                    elif run.font.size == 158750:
                        bit_sequence.append('1')

    bit_string = ''.join(bit_sequence)

    print("основная последовательность битов")
    print(bit_string)

    with open('full_bit_sequence.txt', 'w') as f:
        f.write(bit_string)

    return bit_string

def extract_inverted_bit_sequence():
    doc = Document('test_04.docx')

    bit_sequence = []

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            for char in run.text:
                if char == '\n':
                    continue

                if run.font.size:
                    if run.font.size == 152400:
                        bit_sequence.append('1')
                    elif run.font.size == 158750:
                        bit_sequence.append('0')

    bit_string = ''.join(bit_sequence)

    print("инвертированная последовательность битов")
    print(bit_string)

    with open('inverted_bit_sequence.txt', 'w') as f:
        f.write(bit_string)

    return bit_string

def decode_bit_sequence(bit_string, encoding_name):
    try:
        binary_data = bytearray()
        for i in range(0, len(bit_string), 8):
            byte = bit_string[i:i+8]
            if len(byte) == 8:
                binary_data.append(int(byte, 2))

        decoded_text = binary_data.decode(encoding_name, errors='replace')
        return decoded_text
    except Exception as e:
        return None

def try_all_encodings(bit_string, sequence_name):
    print("декодирование " + sequence_name + " последовательности")

    encodings = ['UTF-8', 'UTF-16', 'ISO-8859-5', 'Windows-1251', 'KOI8-R', 'KOI8-U']

    for encoding in encodings:
        result = decode_bit_sequence(bit_string, encoding)
        if result:
            print(encoding + ":")
            print(result)
            print("")

print("извлечение битовых последовательностей")

main_bits = extract_exact_bit_sequence()
try_all_encodings(main_bits, "основной")

inverted_bits = extract_inverted_bit_sequence()
try_all_encodings(inverted_bits, "инвертированной")