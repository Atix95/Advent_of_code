import os


def create_file_path(file_name):
    # Create the file path to a file, which is in the same folder as the program
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)


def load_hexa_decode_dict(file_name):
    # Load the dict, which decodes the hexadecimal string into four bits of binary
    decode_dict = {}

    with open(create_file_path(file_name), "r", encoding="utf-8") as file_decode:
        for line in file_decode.read().split("\n"):
            key, value = line.split(" = ")
            decode_dict[key] = value

    return decode_dict


def load_hexa_transmission(file_name):
    # Load the hexadecimal transmission into a single string
    hexa_message = ""

    with open(create_file_path(file_name), "r", encoding="utf-8") as file_hexa:
        hexa_message = file_hexa.readline()

    return hexa_message


def decode_hexa_into_binary(hexa_message):
    # Decode the hexadecimal string into a binary code
    decode_dict = load_hexa_decode_dict("day_16_hexadecimal_decode.txt")
    binary_string = ""

    for hexa_char in hexa_message:
        binary_string += decode_dict[hexa_char]

    return binary_string


def decode_literal_value(binary_string):
    # Packet represents literal value. While the five bit packet, which is stored in
    # packet_literal, starts with a 1, the four bits after the 1 are added to the
    # binary_literal string. Then the binary_string is stripped of the first 5 bits
    # and the next five bits are added to packet_literal. If the first bit is a 0,
    # this procedure is done one last time and the final literal value can be converted
    # into a decimal number (literal_value).
    binary_literal = ""
    packet_literal = binary_string[:5]

    while packet_literal[0] == "1":
        binary_literal += packet_literal[1:5]
        binary_string = binary_string[5:]
        packet_literal = binary_string[:5]

    # Intercept case literal_packet start with 0
    binary_literal += packet_literal[1:5]
    binary_string = binary_string[5:]

    literal_value = int(binary_literal, 2)

    return binary_string, literal_value


def decode_binary(binary_string, sum_of_version_numbers=0):
    # Since the packet at its outermost layer can only contain tailing 0s, the hexa-
    # decimal message in binary is searched for packets, as long as the binary string
    # contains 1s. To keep track of the current position in the binary string, the neces-
    # sary bits are sliced from the string. If the type ID of the packet is 4, the packet
    # contains a literal value and the function for it is called. Otherwise its an operator,
    # which then means the length type ID has to be checked. Depending on the value this
    # function is called recursively at least once. As soon as a packet version is identified
    # it is added to sum_of_version_numbers.

    while "1" in set(binary_string):
        packet_version, type_id = int(binary_string[:3], 2), int(binary_string[3:6], 2)
        binary_string = binary_string[6:]
        sum_of_version_numbers += packet_version

        if type_id == 4:
            # Packet represents a literal value. Since the literal value is not needed in
            # this part, the assignment of it can be ignored but is kept for completeness.
            binary_string, literal_value = decode_literal_value(binary_string)

        else:
            # Packet represents an operator
            length_type_id = int(binary_string[0], 2)
            binary_string = binary_string[1:]

            if length_type_id == 0:
                # Next 15 bits represent the total length in bits of sub-packets. Since
                # the end of each sub-packet, that is part of these bits, can be identified
                # without tracking the total length in bits, the first line in this statement
                # can actually be ignored. This function then is called recursively.
                total_length_int = int(binary_string[:15], 2)
                binary_string = binary_string[15:]

                binary_string, sum_of_version_numbers = decode_binary(
                    binary_string, sum_of_version_numbers
                )

            elif length_type_id == 1:
                # Next 11 bits represent the number of sub-packets contained in this packet.
                # Since this function does not distinguish between a sub-packet or a regular
                # packet, one recursive call of this function would be sufficient. Still, the
                # for-loop is maintained for completeness.
                num_sub_packets_int = int(binary_string[:11], 2)
                binary_string = binary_string[11:]

                for sub_packets in range(num_sub_packets_int):
                    binary_string, sum_of_version_numbers = decode_binary(
                        binary_string, sum_of_version_numbers
                    )

    return binary_string, sum_of_version_numbers


if __name__ == "__main__":
    hexa_message = load_hexa_transmission("day_16_input.txt")
    binary_string = decode_hexa_into_binary(hexa_message)
    binary_string, sum_of_version_numbers = decode_binary(binary_string)

    print(f"The total sum of all packet version numbers is: {sum_of_version_numbers}")
