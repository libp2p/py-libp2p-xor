import base64


# bits_in_byte returns a list of bits in a byte, in descending order of significance.
def bits_in_byte(byte):
    return [
        byte & 0x80 != 0,
        byte & 0x40 != 0,
        byte & 0x20 != 0,
        byte & 0x10 != 0,
        byte & 0x8 != 0,
        byte & 0x4 != 0,
        byte & 0x2 != 0,
        byte & 0x1 != 0,
    ]


class Key(bytes):
    def to_float(self):
        f = 0.0
        s = 1.0
        for byte in self:
            for bit in bits_in_byte(byte):
                s /= 2.0
                if bit:
                    f += s
        return f

    def __eq__(self, other):
        if isinstance(other, Key):
            return self.hex() == other.hex()
        else:
            return False

    def __hash__(self):
        return hash(self.hex())

    def __str__(self):
        return self.hex()


def xor_key(x: Key, y: Key):
    return Key(bytes([x[k] ^ y[k] for k in range(len(x))]))


def key_from_base64_kbucket_id_optional(s: str):
    return key_from_base64_kbucket_id(s) if s else None


def key_from_base64_kbucket_id(s: str):
    return Key(base64.b64decode(s))
