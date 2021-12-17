import csv
import itertools
import heapq
import numpy as np
import pandas as pd

from typing import List, Tuple, Dict
class Problem16b:
    def parse_string(self, s):
        print(s)
        bits = self.get_bits_from_string(s)
        ver, typ, val, bits = self.parse_bits(bits)
        return ver, val

    def get_bits_from_string(self, s):
        bits = ""
        for c in s:
            bits += bin(int(c, 16))[2:].zfill(4)
        return bits

    def parse_bits(self, bits) -> (int, int, int, str):
        ver = int(bits[0:3], 2)
        typ = int(bits[3:6], 2)

        if typ == 4:
            bits = bits[6:]
            val_bits = ""
            while True:
                temp_bits = bits[0:5]
                val_bits += temp_bits[1:]
                bits = bits[5:]
                if int(temp_bits[0], 2) == 0:
                    print(ver, typ, int(val_bits, 2))
                    return ver, typ, int(val_bits, 2), bits

        else:
            len_typ = int(bits[6], 2)
            bits = bits[7:]
            if len_typ == 0:
                bit_len = int(bits[:15], 2)
                bits = bits[15:]
                tmp_bits = bits[:bit_len]
                vers = ver
                vals = []
                while len(tmp_bits) > 7:
                    tmp_vers, tmp_typ, tmp_val, tmp_bits = self.parse_bits(tmp_bits)
                    vers += tmp_vers
                    vals.append(tmp_val)
                print(vals)
                val = self.handle_vals(typ, vals)
                print(ver, typ, val)
                return vers, typ, val, bits[bit_len:]
            elif len_typ == 1:
                n_sub_packets = int(bits[:11], 2)
                bits = bits[11:]
                vers = ver
                vals = []
                for i in range(n_sub_packets):
                    tmp_vers, tmp_typ, tmp_val, bits = self.parse_bits(bits)
                    vers += tmp_vers
                    vals.append(tmp_val)
                print(vals)
                val = self.handle_vals(typ, vals)
                print(ver, typ, val)
                return vers, typ, val, bits
        raise Exception("???")

    def handle_vals(self, typ, vals):

        if typ == 0:
            return sum(vals)
        if typ == 1:
            v = 1
            for val in vals:
                v *= val
            v2 = np.product(vals)
            assert v2 == v
            return int(v)
        if typ == 2:
            return min(vals)
        if typ == 3:
            return max(vals)
        if typ == 5:
            return int(vals[0] > vals[1])
        if typ == 6:
            return int(vals[0] < vals[1])
        if typ == 7:
            return int(vals[0] == vals[1])

        raise Exception("???")

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        line = lines[0].strip()

        ver, val = self.parse_string(line)

        print(f"Solution to 16b: {val}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem16b()

    # print(problem.parse_string("D2FE28")[1])
    # print(problem.parse_string("38006F45291200")[1])
    # print(problem.parse_string("EE00D40C823060")[1])
    # print(problem.parse_string("8A004A801A8002F478")[1])
    # print(problem.parse_string("620080001611562C8802118E34")[1])
    # print(problem.parse_string("C0015000016115A2E0802F182340")[1])
    # print(problem.parse_string("A0016C880162017C3686B18A3D4780")[1])
    #
    # assert problem.parse_string("C200B40A82")[1] == 3
    # assert problem.parse_string("04005AC33890")[1] == 54
    # assert problem.parse_string("880086C3E88112")[1] == 7
    # assert problem.parse_string("CE00C43D881120")[1] == 9
    # assert problem.parse_string("D8005AC2A8F0")[1] == 1
    # assert problem.parse_string("F600BC2D8F")[1] == 0
    # assert problem.parse_string("9C005AC2F8F0")[1] == 0
    # assert problem.parse_string("9C0141080250320F1802104A08")[1] == 1

    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
