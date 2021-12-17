import csv
import itertools
import heapq
import numpy as np
import pandas as pd

from typing import List, Tuple, Dict
class Problem16a:
    def parse_string(self, s):
        print(s)
        bits = self.get_bits_from_string(s)
        ver, typ, val, bits = self.parse_bits(bits)
        print(bits)
        return ver

    def get_bits_from_string(self, s):
        bits = ""
        for c in s:
            bits += bin(int(c, 16))[2:].zfill(4)
        return bits

    def parse_bits(self, bits) -> (int, int, int, str):
        print(bits)
        ver = int(bits[0:3], 2)
        typ = int(bits[3:6], 2)

        print(f"({ver}, {typ})")
        if typ == 4:
            bits = bits[6:]
            val_bits = ""
            while True:
                temp_bits = bits[0:5]
                val_bits += temp_bits[1:]
                bits = bits[5:]
                if int(temp_bits[0], 2) == 0:
                    return ver, typ, int(val_bits, 2), bits

        else:
            len_typ = int(bits[6], 2)
            bits = bits[7:]
            if len_typ == 0:
                bit_len = int(bits[:15], 2)
                bits = bits[15:]
                tmp_bits = bits[:bit_len]
                vers = ver
                vals = 0
                while len(tmp_bits) > 7:
                    tmp_vers, tmp_typ, tmp_val, tmp_bits = self.parse_bits(tmp_bits)
                    vers += tmp_vers
                    vals += tmp_val
                return vers, typ, vals, bits[bit_len:]
            elif len_typ == 1:
                n_sub_packets = int(bits[:11], 2)
                bits = bits[11:]
                vers = ver
                vals = 0
                for i in range(n_sub_packets):
                    tmp_vers, tmp_typ, tmp_val, bits = self.parse_bits(bits)
                    vers += tmp_vers
                    vals += tmp_val
                return vers, typ, vals, bits
        raise Exception("???")

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        line = lines[0].strip()

        result = self.parse_string(line)

        print(f"Solution to 16a: {result}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem16a()

    # print(problem.parse_string("D2FE28"))
    # print(problem.parse_string("38006F45291200"))
    # print(problem.parse_string("EE00D40C823060"))
    # print(problem.parse_string("8A004A801A8002F478"))
    # print(problem.parse_string("620080001611562C8802118E34"))
    # print(problem.parse_string("C0015000016115A2E0802F182340"))
    # print(problem.parse_string("A0016C880162017C3686B18A3D4780"))

    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
