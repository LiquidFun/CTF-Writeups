#!uv run
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "z3-solver",
# ]
# ///
from z3 import *
set_param("parallel.enable", True) # Does not do anything here

class UBitVec:
    """Weird hack to change < > <= >= to their unsigned variants

    Otherwise the input file for ifs would've been needed to change
    """
    def __init__(self, val):
        self.val = val

    # Unsigned comparisons
    def __lt__(self, other): return ULT(self.val, self._unwrap(other))
    def __le__(self, other): return ULE(self.val, self._unwrap(other))
    def __gt__(self, other): return UGT(self.val, self._unwrap(other))
    def __ge__(self, other): return UGE(self.val, self._unwrap(other))

    # Bitwise/logical/math ops — return wrapped result
    def __eq__(self, other): return self.val == self._unwrap(other)
    def __ne__(self, other): return self.val != self._unwrap(other)
    def __add__(self, other): return UBitVec(self.val + self._unwrap(other))
    def __radd__(self, other): return UBitVec(self.val + self._unwrap(other))
    def __sub__(self, other): return UBitVec(self.val - self._unwrap(other))
    def __rsub__(self, other): return UBitVec(self._unwrap(other) - self.val)
    def __mul__(self, other): return UBitVec(self.val * self._unwrap(other))
    def __rmul__(self, other): return UBitVec(self.val * self._unwrap(other))
    def __and__(self, other): return UBitVec(self.val & self._unwrap(other))
    def __rand__(self, other): return UBitVec(self.val & self._unwrap(other))
    def __or__(self, other): return UBitVec(self.val | self._unwrap(other))
    def __ror__(self, other): return UBitVec(self.val | self._unwrap(other))
    def __xor__(self, other): return UBitVec(self.val ^ self._unwrap(other))
    def __rxor__(self, other): return UBitVec(self.val ^ self._unwrap(other))
    def __lshift__(self, other): return UBitVec(self.val << self._unwrap(other))
    def __invert__(self): return UBitVec(~self.val)
    def __neg__(self): return UBitVec(-self.val)

    # Unwrapping
    def _unwrap(self, other):
        return other.val if isinstance(other, UBitVec) else other

    # Interop with Z3
    def __z3__(self): return self.val
    def __str__(self): return str(self.val)
    def __repr__(self): return f"UBitVec({self.val})"

opt = Optimize()
vars = []
for v in range(0x25, 0x5d):
    var_name = f"v{v:02x}"
    var = UBitVec(BitVec(var_name, 8))
    vars.append(var)
    globals()[var_name] = var

    if 0x26 <= v <= 0x57:
        opt.add(
            simplify(Or(
                And(var >= ord("0"), var <= ord("9")),
                And(var >= ord("a"), var <= ord("f"))
            ))
        )
#
opt.add(v5c == ord("P"))
opt.add(v5b == ord("C"))
opt.add(v5a == ord("T"))
opt.add(v59 == ord("F"))
opt.add(v58 == ord("{"))
opt.add(v25 == ord("}"))

ifs = [
    (And(And((v59 + v42 & v3c) < ((v53 + v43) - v40), (v4d - v4c & v4a) < 0x27), (v4e + v45 * v5a) < ((v44 + v43) * v42)), 8, 0),
    (And(And((v59 + v42 & v3c) < ((v53 + v43) - v40), (v4d - v4c & v4a) < 0x27), (v4e + v45 * v5a) < ((v44 + v43) * v42)), 8, 0),
    (And(And((v5a * v37 - v31) < 200, 0x3c < ((v2d - v33) + v51)), And(0x4c < ((v2b + v3b) - v57), (v45 - (v54 + v2e)) < (v4f * v2e ^ v52))), 1, 0),
    (And(0xf0 < ((v3a - v3c) * v56), ((v48 + v25) * v27) < 0xe1), 3, 0),
    (And(((v36 + v2d) - v30) < (v38 - v3f | v58), ((v44 ^ v5a) & v54) < 0x24), 4, 0),
    (And(And(And(And(((v43 + v3a) * v3d) < 0xe4, 0x11 < (v36 & v31 ^ v49)), 0xca < (v42 + v3e + v2b)), And(((v4d | v43) ^ v46) < (v56 ^ v25 ^ v2a), (v41 * v43 & v40) < ((v5b & v41) + v29))), And((v34 * v58 & v49) < ((v35 ^ v54) & v2b), (v2c ^ v27 ^ v3c) < (v4f - (v58 + v53)))), 9, 0),
    (And(((v58 + v42) - v26) < 0x81, (v3d ^ v38 ^ v35) < (v33 ^ v48 | v2e)), 2, 0),
    (And(And(And(0x2f < (v32 & v45 | v44), (v49 + v55 & v59) < ((v56 | v38) & v2e)), ((v50 + v31) * v5a) < 0xd9), And(0x62 < ((v42 & v38) + v4b), ((v34 ^ v4a) * v3e) < ((v29 - v34) + v4c))), 7, 0),
    (And(And(0x84 < ((v3c ^ v5c) + v39), 0x10 < (v58 * v26 ^ v4b)), ((v33 + v47) - v4f) < (v44 | v5c | v48)), 5, 0),
    (And(And(((v33 | v49) * v44) < (v53 * v30 & v3a), ((v31 - v27) + v2c) < 10), And(And(And((v48 ^ v27 | v25) < (v41 - v57 ^ v4b), And(And(((v26 | v4c) - v4b) < 0xcf, (v28 + v27 | v55) < (v42 * v30 | v59)), 4 < ((v39 ^ v30) & v26))), And(((v2e | v26) * v51) < (v5c | v49 - v39), 2 < (v5a & v36 & v35))), 0x18 < (v48 * v33 & v3a))), 1, 0),
    (And(And((v4c + v35 | v42) < ((v3a | v27) - v4f), (v36 ^ v30 ^ v49) < ((v28 + v2e) * v4f)), And((v33 * v35 * v37) < 0xc0, And(0xfc < ((v46 ^ v3d) - v38), ((v58 | v3b) - v2f) < ((v48 ^ v2e) & v2d)))), 7, 0),
    (And(And(((v34 | v42) - v44) < 0x42, 0x98 < ((v5a | v32) * v4d)), (v36 + v4a ^ v50) < 0xcd), 4, 0),
    (And(And(0x25 < (v47 * v3b * v3a), ((v32 | v5a) * v4d) < 0x99), (v28 & v54 | v3b) < ((v58 | v4b) & v45)), 1, 0),
    (And(And(0xfc < (v57 * v43 * v50), ((v45 ^ v42) * v35) < 0x57), And(((v55 + v34 & v29) + 0x34) < (v40 * v34 * v32 - 8), 0x55 < (v3f & v2e ^ v3b))), 2, 0),
    (And((v57 + v43 + v58) < 0xd0, And(And(And((v39 * v37 & v5b) < 0x3d, (v2a + v55 | v3f) < ((v2c & v52) - v37)), 0xfc < (v4f * v44 ^ v3f)), 4 < (v53 * v5b - v3b))), 1, 0),
    (And(And(0x4c < ((v3f & v49) + v39), 4 < (v47 ^ v27 ^ v5c)), And((v56 & v5a ^ v4e) < (v36 + v5a + v29), (v54 & v52 | v46) < 100)), 5, 0),
    (And(And(0x5b < (v3b - v30 | v4d), ((v2d | v50) & v46) < (v5c - (v5a + v27))), 0xfc < (v32 - v53 | v25)), 7, 0),
    (And(And(And((v4f * v2a * v58) < (v51 + v5a ^ v58), (v4d & v48 & v27) < ((v25 & v39) - v51)), (v35 ^ v5b | v2c) < 0x96), ((v4b | v58) ^ v33) < (v44 * v4d * v3e)), 10, 0),
    ((v39 + v56 ^ v35) < 0xaf, 8, 0),
    (And(And((v25 | v57 | v45) < ((v3e | v4b) & v32), 0x61 < (v4a + v54 ^ v32)), And(And((v29 + v41 * v2a) < (v4d & v31 ^ v2a), And(((v25 - v57) + v28) < 0x7d, ((v30 | v32) * v58 - 10) < ((v56 & v57) * v33))), 0x41 < (v2b - v54 | v42))), 1, 0),
    (And(And(And(((v5a | v28) - v2d) < (v3b * v48 ^ v35), 0x6e < (v53 ^ v3b + v5a)), (v3f | v2a | v31) < 0x43), (v36 * v52 & v57) < (v45 - (v54 + v2e))), 8, 0),
    (And((v52 - v33 & v37) < ((v28 | v53) + v44), 0xb1 < ((v2c - v5b) * v42)), 9, 0),
    (And(And((v46 - v4a & v29) < ((v42 | v31) - v39), ((v47 & v4f) - v2c) < 0xfd), And(((v41 ^ v46) - v35) < ((v2d ^ v28) * v25), And(0xc5 < (v49 * v25 - v53), 0x6e < (v58 & v46 & v27)))), 9, 0),
    (And(And((v49 - v39 | v5c) < (v25 ^ v45 ^ v4f), 0xe < ((v48 ^ v3f) & v57)), (v4a + v2e * v56) < ((v2b | v3b) & v25)), 1, 0),
    (And((v4b + v48 + v5b) < 10, ((v55 - v26) * v44) < ((v25 ^ v2f) + v46)), 1, 0),
    (And(And((v34 + v44 ^ v25) < ((v36 + v2d) - v30), (v2f * v30 * v43) < 99), And((v25 - v35 & v48) < ((v52 | v2d) ^ v34), (v2e | v50 | v42) < ((v57 ^ v42) & v35))), 5, 0),
    (And(And(And(((v43 + v3f) * v3b) < 0x97, 0xcf < ((v37 ^ v56) - v2d)), (v4b - (v56 + v43)) < 0xb6), And(0x3b < (v47 & v58 | v4c), (v2a * v47 - v35) < 9)), 3, 0),
    (And(And((v36 + v58 + v41) < (v4b - (v34 + v50)), (v48 + v29 & v25) < (v57 & v27 ^ v39)), And(0x33 < ((v4e | v43) ^ v53), And((v5a & v3e & v2c) < 3, ((v2a ^ v4f) + v29) < (v42 - v4d & v3a)))), 1, 0),
    (And(And((v59 & v53 | v4d) < 0x54, ((v43 - v27) * v33) < 0xf), ((v3f | v58) & v31) < 0x28), 1, 0),
    (And((v4c - (v4d + v2d)) < 0xb3, And(And((v26 * v37 * v4a) < ((v41 + v42) * v29), (v42 - v54 ^ v45) < (v5c * v42 * v47)), 0x2c < (v4a - v4c ^ v26))), 10, 0),
    (And(And(0x47 < ((v2f + v5c) - v26), (v3e + v39 & v25) < ((v2c + v43) * v3e)), ((v41 - v46) * v35) < ((v38 | v5b) * v43)), 10, 0),
    (And(And(And((v56 + v35 & v27) < ((v52 + v3d) * v41), 0x66 < ((v2e & v3e) + v38)), 0xc < ((v44 | v5c) ^ v52)), And((v51 ^ v2b | v56) < (v31 | v3b | v58), (v48 - (v55 + v40)) < (v3c + v54 + v25))), 7, 0),
    (And(And(((v30 & v2d) - v31) < (v54 * v32 ^ v5c), (v4b * v2f | v50) < 0x32), And(0xb9 < ((v3a - v3f) * v40), And((v2b + v29 & v3d) < 0x1d, ((v2e | v38) & v56) < 0x52))), 10, 0),
    (And(And(And(((v34 ^ v51) - v3d) < 0x1c, ((v33 + v28) * v45) < ((v2b | v3c) ^ v38)), (v54 * v2b * v39) < (v27 | v39 | v44)), (v4d - v26 | v35) < ((v43 ^ v3a) & v41)), 9, 0),
    (And(0x48 < (v37 & v48 & v55), (v31 - v44 & v39) < ((v45 ^ v48) * v4b)), 5, 0),
    (And(And(((v50 | v57) & v58) < ((v4e | v2b) & v4f), ((v27 | v2f) * v55) < 0xfd), And((v40 * v3b & v54) < ((v5c | v3a) ^ v57), And(0x81 < ((v26 ^ v2c) * v59), ((v48 ^ v2c) * v30) < 0x17))), 9, 0),
    (And(And(0xcc < (v5a * v5b | v50), And(((v58 ^ v59) - v5c) < (v54 + v3a | v4e), ((v4c | v48) & v2c) < ((v30 - v4c) + v40))), And(0x25 < (v46 - v2e & v2a), And(And((v36 + v2e | v26) < ((v4d | v5a) + v4e), ((v28 ^ v54) + v4f) < ((v44 | v5b) + v2e)), (v2b & (v36 | v4e)) < (v35 & v4e | v4c)))), 10, 0),
    (((v46 ^ v4e) & v2d) < 3, 7, 0),
    (And(And((v29 + v57 + v58) < 0xfd, ((v3b | v2b) & v25) < (v2d - v4e | v3b)), 0x3a < ((v41 | v30) ^ v47)), 4, 0),
    (And(And((v31 | v58 | v3b) < (v56 + v2e + v44), (v3f * v2b * v4d) < 0xb4), ((v37 ^ v57) & v29) < (v4e & v42 ^ v48)), 5, 0),
    (And(And(And((v4a - (v46 + v40)) < 0x83, (v51 * v29 ^ v5a) < 0xfd), (v4f & v55 & v54) < 0x1f), And(And((v30 ^ v52 ^ v57) < ((v45 ^ v2d) & v5c), ((v26 ^ v52) - v4c) < 0x22), (v4b | v45 ^ v5c) < (v34 & v43 & v33))), 2, 0),
    (And(And(((v4e ^ v56) & v38) < ((v4c | v48) & v2c), 0x6f < (v4b ^ v4c | v27)), And(((v5b | v2a) - v29) < ((v59 | v54) + v31), (v25 + v4b & v46) < (v34 + v4a | v3d))), 3, 0),
    (And(And(And(((v2f & v47) * v37) < ((v50 & v25) + v3e), (v50 - v48 ^ v3c) < ((v49 & v44) * v27)), 0x4c < ((v41 | v46) ^ v54)), And((v5a & v36 & v35) < 3, 0xad < ((v5b & v57) - v33))), 10, 0),
    (And(And((v3f + v4f + v3d) < 0x94, 2 < ((v41 ^ v25) & v46)), And(((v51 + v3c) - v49) < (v5c & v4d & v54), (v4b * v4c ^ v34) < (v27 & v28 ^ v42))), 8, 0),
    (And(((v5b & v25) * v38) < (v52 - (v4a + v29)), And(And((v40 * v28 | v4d) < ((v5c | v29) * v53), 0xdb < ((v33 + v29) * v53)), ((v4b | v53) + v55) < ((v2d & v30) - v31))), 1, 0),
    (And(And((v4d ^ v28 ^ v30) < 0x67, ((v2e & v3e) + v38) < 0x67), 0x87 < (v45 * v2c * v54)), 7, 0),
    (And(And(((v31 ^ v26) * v25) < ((v2f + v4c) - v35), 0x22 < (v43 & v37 & v3c)), (v38 * v5c - v2e) < 0x1e), 10, 0),
    (And(And(And(((v35 | v4a) * v34) < ((v5a | v2d) ^ v49), ((v4f & v37) - v52) < 0xa3), (v52 - v3d ^ v39) < 0x19), And(((v4c + v29) * v44) < ((v29 ^ v35) * v4a), (v3e + v40 & v38) < 3)), 5, 0),
    (And(And((v30 * v41 | v34) < ((v51 ^ v2b) + v4f), (v38 * v3e * v39) < ((v42 - v38) * v46)), And(((v27 - v2c) * v5b) < ((v2d + v4a) - v3c), And(And((v2f ^ v4c | v34) < 100, 0x7e < (v25 | v27 | v3a)), ((v43 & v32) * v4d) < 0xcb))), 10, 0),
    (And((v48 + v29 * v34) < (v4e * v2b * v2c), And(And((v40 + v48 ^ v34) < ((v5a & v5c) + v51), 0xda < (v44 * v5a - v2d)), And((v25 + v39 + v3f) < ((v58 ^ v51) - v3c), And(0x5e < (v27 * v3d | v59), ((v4a & v5a) + v51) < ((v57 | v58) - v28))))), 2, 0),
    (And(And(And(((v47 | v53) ^ v3c) < (v39 + v51 | v3a), 0x11 < (v31 - v56 & v53)), 0xbf < (v37 * v35 * v33)), (v51 + v3c + v40) < ((v41 ^ v43) * v33)), 5, 0),
    (And(And(((v54 | v59) + v31) < ((v2f & v4f) - v3b), 0x9c < ((v5a ^ v34) - v4b)), And((v47 + v58 & v30) < 0x32, (v57 * v58 ^ v50) < (v41 + v31 | v54))), 8, 0),
    (And(And((v28 & v27 ^ v42) < (v3e & v59 | v3c), (v43 & v33 & v34) < ((v36 | v2d) & v53)), And(((v3a - v42) + v5b) < (v5c + v59 + v4c), And(0x4a < ((v3b & v51) + v3d), ((v39 | v27) - v47) < (v54 & v28 | v3b)))), 1, 0),
    (And(And(And(((v28 | v41) ^ v29) < ((v47 | v50 | v2d) + 0xc), ((v4b ^ v2f) + v55) < (v39 + v3e & v25)), ((v48 + v3c) * v2b) < ((v2a & v28) - v3f)), And(And(0x4a < (v49 * v2e & v3a), (v3b * v49 | v36) < (v52 ^ v56 | v37)), ((v57 ^ v3b) & v43) < ((v3d | v50) ^ v28))), 6, 0),
    (And(And((v49 * v57 - v3c) < 0xa2, 0x31 < (v4b * v2f | v50)), (v25 * v58 ^ v49) < (v52 - v53 ^ v4f)), 1, 0),
    (And(And((v41 * v2c * v46) < 0x3b, ((v35 ^ v36) * v3c) < (v3a + v3b | v3d)), ((v45 & v40) + v55) < (v2f + v34 + v32)), 6, 0),
    (And((v54 + v37 * v42) < 0x22, ((v43 ^ v41) * v33) < (v4b * v4d | v2c)), 1, 0),
    (And(And((v3b * v48 ^ v35) < ((v2e | v45) * v35), 0xf9 < ((v43 & v5a) * v32)), And(((v27 ^ v5a) - v3d) < ((v47 | v4b) - v53), ((v50 ^ v2f) - v27) < (v58 * v34 & v49))), 3, 0),
    (And(And(((v58 | v57) - v28) < (v2b * v51 | v38), And(And((v32 - v2a & v57) < 0x3b, (v4b * v4d | v4a) < 0xfd), 0x26 < ((v26 | v3d) & v32))), And(And(((v55 | v3e) - v41) < (v5b | v4b | v59), (v59 ^ (v3e | v3d)) < (v30 ^ v57 ^ v52)), 99 < (v3f * (v2a | v58)))), 9, 0),
    (And(((v53 | v51) ^ v2d) < 0x11, 0x72 < (v50 + v31 * v2e)), 10, 0),
    (((v53 ^ v2d) + v2e) < 0x56, 4, 0),
    (And(And(And((v2e + v57 ^ v30) < (v32 - v3a & v52), 2 < (v42 - v52 & v35)), ((v49 + v3a) - v3f) < 0x53), And(((v29 ^ v26) & v4c) < ((v45 & v4c) - v50), ((v4e | v2b) & v4f) < (v38 * v45 & v3c))), 4, 0),
    (And(And(And(((v47 | v50 | v2d) + 0xc) < ((v4e ^ v3f | v30) - 0x2a), (v45 + v3e ^ v36) < 0xb9), And((v56 | v46 | v28) < (v2d - v2c & v52), And(And(((v3d ^ v44) + v26) < ((v4f + v49) - v37), 0x40 < ((v54 + v49) - v39)), (v27 * v38 | v2e) < ((v32 | v46) * v54)))), 0x96 < ((v43 + v3f) * v3b)), 3, 0),
    (And(And(0x1c < (v2b + v29 & v3d), 0x8a < (v46 + v2b ^ v47)), (v43 & v27 | v41) < (v50 - v48 ^ v3c)), 9, 0),
    (And(And(2 < (v37 + v3d & v46), 2 < (v35 + v4e & v46)), And(((v34 & v54) * v45) < 0x3f, (v41 - v56 ^ v45) < ((v28 + v33) * v45))), 3, 0),
    (And(((v59 | v4f) & v56) < 0x6f, 0xcf < (v57 + v58 + v43)), 5, 0),
    (And(And(And((v57 - (v3d + v41)) < (v2c * v2d | v56), 0x89 < (v35 ^ v56 | v4f)), ((v3b | v5c) * v2e) < 0x37), ((v42 | v2c) & v3f) < 0x2e), 7, 0),
    (And(And(((v58 - v34) * v27) < 0x55, 0x16 < ((v2c ^ v48) * v30)), (v52 + v51 + v40) < ((v4c ^ v29) + v2b)), 1, 0),
    (And(And((v59 & v3d | v27) < 0x59, (v4c + v3f * v5c) < ((v26 ^ v29) & v4c)), And(0x26 < (v3f & v27 & v57), (v5b + v34 ^ v4d) < (v2a - v40 | v58))), 3, 0),
    (And(2 < (v3f - v42 & v40), ((v2d | v52) * v5a) < (v26 - (v52 + v4d))), 2, 0),
    (And(And((v32 & v4f ^ v44) < 5, 0x4c < (v45 ^ v38 ^ v50)), ((v48 ^ v2e) & v2d) < (v52 * v5b - v27)), 10, 0),
    (And(And(And((v36 + v30 + v39) < (v50 - v5c ^ v3c), (v4f | v5a | v52) < (v4e + v29 * v33)), And(((v54 + v39) * v3c) < 0x59, And((v2c ^ v49 | v44) < 0x45, ((v43 + v33) - v46) < (v41 * v56 ^ v2d)))), 0x70 < ((v47 + v51) * v3a)), 6, 0),
    (And((v41 - v3a | v34) < 0xfd, 2 < (v27 * v38 & v5b)), 1, 0),
    (And(And(And(((v38 ^ v56) + v4a) < 0x3e, (v58 - v43 | v2a) < (v5a + v46 ^ v48)), (v32 + v4a + v36) < 0xea), ((v31 | v42) - v39) < ((v2f & v3b) - v52)), 6, 0),
    (And((v2b - v54 | v42) < 0x42, ((v2f | v3a) + v4e) < 0xee), 6, 0),
    (And(And(((v48 | v29) ^ v3d) < (v4f * v2a * v58), (v43 ^ v48 ^ v27) < 0x39), And(((v5c - v38) * v29) < ((v49 ^ v36) + v41), And(((v2d | v59) - v34) < 0x1f, (v40 - v4f ^ v32) < (v25 - v35 & v48)))), 9, 0),
    ((v40 * v42 - v30) < 0xfd, 5, 0),
    (And(And(0xb8 < (v3e + v45 ^ v36), ((v25 + v59) * v57) < 0xf6), (v31 * v4a ^ v41) < (v3a ^ v4f ^ v51)), 9, 0),
    (And(And(0xe3 < ((v43 + v3a) * v3d), ((v28 | v26) ^ v36) < 0x66), And(And(And(0x79 < (v37 ^ v5a | v4e), And((v25 ^ v2a ^ v56) < (v27 & v46 & v44), (v54 - v2f | v3d) < (v56 & v5a ^ v4e))), ((v2b + v3b) - v57) < 0x4d), 0x38 < ((v48 | v3a) - v33))), 2, 0),
    (And(And(And(4 < ((v2b ^ v42) & v3d), (v4d & v52 | v5c) < ((v38 ^ v30) + v27)), 5 < (v4f ^ v58 ^ v59)), And(((v35 + v2c) - v54) < (v37 | v53 | v33), (v39 ^ v46 ^ v3f) < ((v50 | v2d) + v42))), 9, 0),
    (And(And(0xcc < ((v30 + v27) * v46), (v2f | v4a | v2b) < ((v3b & v25) * v34)), 0x13 < (v35 & v3e ^ v31)), 6, 0),
    (And((v5b & v58 & v2f) < 3, ((v4d & v33) + v5b) < ((v40 | v4f) + v45)), 4, 0),
    (And(And(And((v25 ^ v4f | v4d) < 100, (((v51 + v42) - v36) + 0x1a) < ((v44 - (v5a + v57)) + 0x73)), ((v2f & v51) + v32) < 0x71), And(And(0xfc < ((v2a ^ v46) - v4d), ((v46 + v4f) - v3b) < 0x2f), And(((v58 | v2a) * v3f) < 100, 2 < (v2c + v3e & v4d)))), 6, 0),
    (0xc3 < ((v3f ^ v52) * v44), 7, 0),
    (And(And(((v29 | v5c) * v53) < ((v50 | v45) + v52), 0x5a < ((v3a + v3d) - v2c)), And(0x45 < ((v27 | v36) * v57), And((v3f - v4f | v54) < (v58 * v57 ^ v50), (v48 + v41 * v47) < (v5a - v43 | v4b)))), 4, 0),
    (And((v5c | v27 | v35) < ((v2f & v3c) + v32), ((v3d - v5c) + v2c) < 0x1b), 5, 0),
    (And((v49 - v2e & v27) < 3, And(And((v53 & v37 | v55) < (v30 * v27 ^ v40), (v29 & v40 | v54) < 0x3e), 0xfc < ((v3e ^ v30) * v50))), 7, 0),
    (And((v56 | v34 | v38) < 0x78, (v32 - v3a & v52) < ((v35 | v4e) + v45)), 6, 0),
    (And(And((v5c * v4e - v2b) < (v54 * v50 - v2a), (v2f - (v4a + v28)) < 0xea), And((v40 + v25 ^ v3f) < ((v45 & v32) - v36), (v3d & v49 ^ v46) < 0x6b)), 10, 0),
    (And(((v55 | v32) + v53) < ((v2f & v47) * v37), 2 < (v59 - v44 & v3e)), 3, 0),
    (((v2a & v40) - v43) < 0xfd, 1, 0),
    (And(And(And(And((v38 ^ v2c | v35) < ((v29 + v4c) * v44), 0x80 < (v4a + v4c | v5c)), (v50 ^ v39 | v25) < (v59 * v3c & v54)), And(0x6a < (v3d & v49 ^ v46), 0xd0 < (v31 - v38 ^ v4e))), (v52 | v34 | v51) < ((v56 & v3d) * v39)), 7, 0),
    (And(And((v5c + v59 ^ v47) < ((v29 | v59) + v51), (v45 - v47 & v32) < 0x3b), And((v56 ^ v35 | v4f) < 0x8a, And((v42 + v5b & v45) < (v48 & v43 | v3d), 0x22 < (v4c + v25 & v55)))), 8, 0),
    (And((v25 * v28 & v41) < (v34 + v2b * v42), And(And((v56 * v41 ^ v2d) < (v47 * v2b - v38), (v49 | v38 | v59) < 0x8f), (v48 + (v56 | v34)) < 0xe8)), 2, 0),
    (And(And((v30 * v5c * v59) < 0x81, (v4d & v5c & v54) < (v2c + v4c | v56)), And(((v42 - v38) * v46) < (v39 + v3f | v3e), ((v40 - v39) + v33) < ((v3a | v30) * v39))), 8, 0),
    (And(0x5f < (v4e ^ v2f ^ v54), And(And(((v26 ^ v30) * v46) < (v44 - v5b | v2c), ((v47 | v26) & v3a) < ((v38 & v5b) + v32)), And(((v53 + v26) - v35) < 0x3d, ((v45 & v4c) - v50) < (v4c + v3f * v5c)))), 10, 0),
    (And(And(And(0x6c < (v48 - v2b | v3e), (v32 ^ v3e ^ v57) < 0x51), (v2c - (v4d + v4c)) < (v3b * v35 & v49)), And(0x2b < ((v25 & v41) - v54), (v56 * v29 ^ v35) < 0x16)), 4, 0),
    (And(And(((v50 | v39) - v2e) < (v4f - v55 ^ v40), (v3f - (v29 + v56)) < 0x91), And((v44 & v27 & v46) < ((v4d | v43) ^ v46), (v59 - (v51 + v5c)) < (v5b + v42 & v45))), 2, 0),
    (And(And(And((v32 - v29 ^ v4f) < ((v4c ^ v48) & v28), 0x7e < (v3f | v2f | v41)), 0xa9 < (v52 + v5a ^ v31)), 0x7e < (v2c - (v52 + v5a))), 8, 0),
    (And(And(((v51 - v50) * v56) < (v3d ^ v38 ^ v35), 0x3d < (v56 + v5a * v4b)), And((v52 & v51 | v27) < 0x5e, 0xde < (v5b + v42 + v59))), 3, 0),
    (And(And(0x9c < ((v33 | v58) + v42), ((v41 | v30) - v48) < ((v4a ^ v34) * v3e)), And(((v29 + v2c) * v2b) < 0x32, (v2c - v47 ^ v4e) < ((v5c ^ v30) + v2f))), 7, 0),
    (And(And(((v4b ^ v36) & v39) < 3, 0xfc < ((v40 | v51) - v2a)), 0x1d < ((v25 + v38) * v46)), 10, 0),
    (And(0xfa < (v3a - v37 | v54), ((v34 | v37) - v56) < (v2e | v42 | v50)), 5, 0),
    (And(((v5a & v38) * v5c) < (v58 & v28 ^ v4b), 0x7e < ((v2e ^ v48) * v4d)), 2, 0),
    (And(And((v48 * v33 & v3a) < 0x19, (v34 + v42 * v2b) < ((v55 | v2e) & v42)), And(And(And((v42 - v56 ^ v47) < (v52 & v4e | v46), ((v45 + v46) * v3e) < 0xd7), (v36 + v34 | v29) < (v5c * v38 * v37)), And((v2d - v4e | v3b) < (v4a + v56 * v2e), (v4f - v32 ^ v50) < ((v4d & v4e) * v39)))), 4, 0),
    (And(4 < (v51 - v4c & v4e), And(And(((v43 + v2e) - v3c) < 0x2c, ((v2f - v4d) * v53) < 0xda), And((v37 | v5c | v59) < (v3d * v3c & v2f), ((v28 & v2e & v25) + 0xb7) < ((v30 | v32) * v58 - 10)))), 8, 0),
    (And(((v57 ^ v3c) - v44) < ((v2b | v3c) - v36), ((v50 | v4d) & v49) < 0x3a), 1, 0),
    (And(0x2d < ((v55 | v51) * v32), 0xfc < ((v4f & v47) - v2c)), 7, 0),
    (And(And(And(And((v44 - v58 & v5c) < 0x11, ((v55 & v3c) * v3e) < 0xf1), (v52 - v57 | v4e) < (v58 - v49 | v25)), ((v3b | v2f) & v47) < ((v4d + v52) - v26)), And(((v32 | v38) - v48) < ((v39 | v3d) - v48), ((v4b | v3e) & v32) < ((v4c ^ v59) * v32))), 6, 0),
    (And(And((v28 + v43 | v5c) < ((v45 - v49) + v3b), 2 < ((v3e - v3a) * v3c)), And(((v4e ^ v3e) * v33) < 0x7f, 0x24 < (v27 & v55 & v26))), 7, 0),
    (And(((v42 & v29) + v5b) < (v5a & v4b | v53), (v52 | v45 | v56) < 0x91), 3, 0),
    (And(And(((v4e + v46) - v40) < (v43 * v41 & v40), ((v30 & v50) - v34) < 0xb7), ((v5c ^ v3c) + v39) < 0x85), 3, 0),
    (And(And(((v51 ^ v58) - v3c) < ((v3e + v4a) * v57), ((v41 | v27) * v3d) < 0x46), ((v28 & v2a) - v3f) < (v4e ^ v27 | v4b)), 8, 0),
    (And(And(0x51 < ((v55 - v51) + v4a), (v40 * v4d | v28) < 0x85), And(((v2a & v51) + v42) < (v27 | v5c | v35), (v53 & v4d & v3b) < (v29 * v3f - v3c))), 9, 0),
    (And(And((v44 - v2c | v39) < 0xdc, (v34 * v37 | v49) < 0xca), ((v3e ^ v30) * v50) < 0xfd), 2, 0),
    (And(0x4a < (v59 & v44 | v41), (v4f * v2e ^ v52) < (v36 * v52 & v57)), 9, 0),
    (And(And(((v2f & v29) - v4f) < ((v48 ^ v2e) * v30), 0x89 < (v50 | v48 | v4c)), And((v39 + v28 & v47) < 0x21, 0x8b < (v34 * v31 ^ v38))), 7, 0),
    (And(((v37 & v5b) * v34) < (v4c + v58 | v4d), 0x17 < ((v32 ^ v3b) - v49)), 9, 0),
    (And((v30 & v54 ^ v2b) < (v41 & v5c | v3e), 0x13 < ((v3d ^ v48) & v43)), 8, 0),
    (And(And(And((v4d + v4a & v51) < (v59 + v42 & v3c), ((v58 | v3c) & v33) < ((v4c & v29) + v36)), ((v2c & v52) - v37) < ((v50 | v4a) - v28)), And(((v47 ^ v28) & v41) < 3, 0xe < (v4e * v42 * v5a))), 10, 0),
    (And(And(And((v44 - v5b | v2c) < (v26 + v48 | v41), 0x68 < ((v35 + v37) - v28)), And((v2f + v4c + v54) < 0x88, And(And((v29 & v4e | v54) < 0x3f, (v3a + v3b | v3d) < (v3a & v37 & v43)), ((v33 | v39) & v2d) < 0x27))), (v30 * v51 * v47) < (v4b * v44 ^ v5c)), 6, 0),
    (And((v42 & v4e ^ v48) < (v3c * v3d - v36), And(And((v34 * v31 & v55) < (v35 & v30 | v4e), 0x96 < (v2f * (v31 + v3c))), And(((v37 + v55) * v2f) < 0x94, And(((v4b ^ v55) * v48) < (v4b ^ v55 | v44), ((v2e ^ v37) - v40) < ((v46 ^ v41) - v35))))), 5, 0),
    (And(And(And(And((v36 ^ v5b | v40) < (v46 + v47 & v31), 0x29 < (v3f & v3a | v29)), (v2c + v3e & v4d) < 3), And(And((v5c ^ v48 ^ v54) < 7, (v39 - v2d ^ v45) < 0xa3), And(((v4e + v3a) - v3d) < (v49 - v45 ^ v52), And((v41 * v2f - v47) < 0x52, 0x50 < (v3b * v43 ^ v32))))), (v52 * v5b - v27) < ((v58 | v3b) - v2f)), 4, 0),
    (And(And(And((v2c + v3d ^ v2d) < ((v55 & v4b) - v5c), ((v57 | v44) - v4c) < 5), 0x3e < (v4e & v29 | v54)), (v34 * v2e ^ v27) < (v3c * v33 * v39)), 6, 0),
    (And(And((v3f & v47 ^ v29) < ((v49 | v35) - v3f), ((v56 & v57) * v33) < ((v2e & v28 & v25) + 0xb7)), And(0x3e < (v2a - v4c | v57), And(0x52 < (v48 * v2b * v36), 4 < ((v30 | v2d) ^ v2a)))), 2, 0),
    (0x87 < ((v4e ^ v31) + v53), 3, 0),
    (And(And(And((((v42 ^ v3a) - v52) - 0x2c) < (v58 * v43 ^ v4a), (v40 + v52 | v43) < (v3f ^ v4f | v3c)), 0xb7 < (v47 + v30 + v53)), And((v4e * v42 * v5a) < 0xf, ((v5b ^ v4a) - v54) < 0x48)), 9, 0),
    (And(And((v47 - v39 | v57) < ((v29 & v42) + v5b), ((v2f + v4c) - v35) < (v30 * v4c * v32)), And(((v45 | v2d) + v51) < ((v38 + v27) - v54), And((v52 + v46 & v51) < (v26 * v4a * v37), 0x37 < ((v25 ^ v31) & v3e)))), 8, 0),
    (And((v5c - v33 ^ v4a) < 0x28, (v2b - (v48 + v27)) < (v3b * v40 & v54)), 1, 0),
    (And(((v3e & v2f) * v47) < ((v4b & v28) - v3a), 0x1d < ((v49 ^ v56) - v3c)), 2, 0),
    (And(And(0xcc < ((v2c & v38) * v51), (v5a + v52 ^ v31) < 0xaa), And(((v39 ^ v2c) + v37) < 0x6f, (v3f + v39 | v3e) < (v39 * v38 * v3e))), 9, 0),
    (And(And((v2d ^ v39 ^ v4a) < 0x3f, And(And(And((v46 * v28 ^ v4e) < ((v44 ^ v58) & v42), ((v5a - v37) + v32) < 0x19), ((v43 | v4e) ^ v53) < 0x34), 0x19 < ((v57 ^ v38) - v28))), And(And(((v52 | v4b) + v2a) < ((v3e + v41) * v38), 0xe7 < ((v4d | v42) * v56)), And(((v4c & v2a) - v36) < (v4d - v26 | v35), ((v3d & v52) - v3f) < ((v3e - v39) + v2c)))), 1, 0),
    (And(And(And(0x66 < ((v3f + v59) * v2d), 0x4b < ((v51 ^ v2f) * v41)), (v53 & v40 | v31) < ((v2b ^ v34) & v50)), And(((v44 - v36) * v4b) < ((v3e | v55) - v41), ((v3b | v3e) * v2d) < ((v35 & v55) * v39))), 5, 0),
    (And(And(And((v2f - v5b | v4f) < ((v3e & v2f) * v47), (v52 * v4d ^ v40) < 0x6f), 0xe4 < ((v51 | v3c) * v4c)), ((v4e & v54) + v25) < (v53 * v4d & v3c)), 7, 0),
    (And(And(And(And(((v44 ^ v30) * v4a) < ((v33 + v40) - v39), (v56 & v30 | v4c) < ((v48 - v30) + v5a)), And(And(((v45 - v49) + v3b) < ((v31 ^ v4f) + v55), (v58 + v26 * v55) < 0x39), 99 < (v2e * v53 - v55))), ((v5c | v3a) ^ v57) < (v2b - (v48 + v27))), And(And((v32 + v28 | v54) < ((v3c ^ v35) - v37), (v3f & (v27 | v5c)) < (v52 - v2e | v30)), (v41 & v51 ^ v4e) < (v37 | v58 & v30))), 8, 0),
    (And(And(And(((v3c | v4a) ^ v48) < (v57 + v44 & v4c), (v31 + v41 | v54) < (v3f - v4f | v54)), 0xc2 < ((v32 | v52) * v3e)), (v35 * v38 | v53) < 0xc3), 9, 0),
    (And(And((v2d + v41 + v4b) < ((v39 & v32) + v55), ((v58 & v49) + v42) < 100), And((v2c * v3d | v4c) < (v29 & v26 & v40), ((v4e ^ v5c) * v3e) < 0x18)), 9, 0),
    (And(And(0xa0 < (v3c * v25 * v57), 0x32 < (v2c ^ v31 ^ v51)), ((v50 & v25) + v3e) < ((v32 | v55) + v53)), 9, 0),
    (And(And(And(0x16 < ((v46 | v56) * v30), 0x87 < (v54 + v4c + v2f)), 0x5a < ((v47 + v37) - v2d)), ((v35 ^ v29) * v4a) < (v2c ^ v38 | v35)), 9, 0),
    (And(And(((v42 + v3c) - v4c) < 0x41, (v39 | v44 | v27) < ((v4b & v2a) - v2c)), And(0x34 < (v5a - v58 & v37), And(((v45 ^ v43) & v50) < 3, (v38 * v37 * v5c) < (v25 - (v3e + v55))))), 10, 0),
    (And(And(And(And(((v4d + v48) - v5b) < 0x93, ((v57 ^ v45) + v4e) < (v29 ^ v45 + v4d)), (v31 * v34 ^ v38) < 0x8c), 0x13 < ((v52 ^ v49) * v43)), And(And(((v47 | v38) & v26) < (v4c | v33 | v53), (v58 + v4c & v52) < ((v51 & v4c) - v52)), And((v53 & v38 & v2e) < ((v58 | v38) & v45), (v28 - (v33 + v49)) < 0xd6))), 10, 0),
    (And(And((v4f ^ v58 ^ v59) < 6, ((v43 + v44) * v42) < ((v4b | v3e) ^ v35)), And((v4a * v4d * v5b) < 0xca, And(((v5a | v4d) + v4e) < (v47 + v25 * v56), 0x3a < (v32 - v2a & v57)))), 1, 0),
    (And(And(And((v48 * v2c * v4b) < ((v5b | v2f) & v4e), (v49 - v3c & v40) < 3), 0x11 < (v2a - v46 & v51)), And(((v27 | v26) & v41) < (v50 - v32 & v2b), ((v2d | v50) + v42) < ((v3f ^ v4d) * v3d))), 1, 0),
    (And(And((v30 & v55 & v45) < (v4d & v48 & v27), 0x14 < ((v42 ^ v56) & v4f)), ((v40 ^ v30) & v31) < (v29 + v45 + v38)), 4, 0),
    (And((v4b & v5a | v53) < (v47 - v39 | v57), And(And(And(((v4c & v32) * v59) < (v54 * v47 | v34), 0x65 < (v41 * (v54 | v57))), ((v4f ^ v2d) + v54) < 0x43), (v42 + v2b ^ v45) < ((v35 | v4a) * v34))), 5, 0),
    (And(And(0xbf < (v27 * v3c - v4d), (v32 * v30 * v4c) < ((v26 ^ v31) * v25)), And((v38 - (v47 + v2d)) < 0xe7, (v29 + v38 + v45) < ((v3d & v4d) + v53))), 2, 0),
    (And(And(((v3a | v27) - v4f) < (v2a ^ v47 | v34), (v25 * v37 & v44) < (v30 & v56 | v4c)), And(((v50 ^ v54) & v5a) < 3, And(And((v38 + v4f & v3e) < 3, ((v41 ^ v2a) + v4d) < 0xd6), ((v54 | v3a) - v3d) < ((v43 + v5a) * v3c)))), 10, 0),
    (And(And((v28 + v36 & v27) < (v31 ^ v36 ^ v4d), ((v38 + v30) * v45) < ((v52 + v47) - v2f)), 0xe < ((v3d ^ v36) & v2d)), 10, 0),
    (And(And(((v47 + v3d) - v2e) < 0x43, ((v37 ^ v28) + v32) < 0x96), (v5a | v29 | v56) < (v52 * v5a * v4d)), 7, 0),
    (And(And((v44 & v3e & v3b) < ((v28 ^ v50) * v39), (v40 & v2c | v47) < 0x36), And((v5a + v4a * v3a) < ((v5b + v3b) * v4c), And(And(0x40 < ((v42 - v4c) + v3c), (v2f - (v43 + v5c)) < (v30 & v54 ^ v2b)), ((v58 & v30) + v5a) < (v46 + v49 & v34)))), 7, 0),
    (And(And(And(((v42 | v40) - v36) < 0xf4, ((v35 + v37) - v28) < 0x69), And((v38 & v49 | v3c) < 0x41, And(((v3f + v59) * v2d) < 0x67, (v47 & v58 | v4c) < 0x3c))), 0x3e < (v4a ^ v2d ^ v39)), 5, 0),
    (And(And((v42 - v4d & v3a) < ((v29 ^ v3a) - v2a), ((v32 ^ v5c) + v2a) < ((v29 - v44) * v41)), And((v4c + v58 | v4d) < ((v2b & v31) + v4b), And(And(0x65 < ((v47 & v3a) + v2b), 0x5c < ((v59 ^ v42) & v4b)), 0x35 < (v4f ^ v59 ^ v33)))), 4, 0),
    (And((v55 + v3d & v3a) < (v53 - (v51 + v33)), And(And(0x14 < ((v5c | v58) ^ v41), ((v26 ^ v40) * v48) < (v25 * v58 ^ v49)), (v4e | v55 | v5b) < (v28 | v48 * v5c))), 6, 0),
    (And(((v25 | v28) & v56) < (v2f | v2b | v4a), And(And((v41 + v29 + v3f) < (v44 & v3c | v4f), 0xf1 < (v2b - (v4a + v42))), And(0xfc < (v55 + v4b | v3e), And(And((v5c + v58 * v51) < 0xaf, (v2e * v29 | v3a) < ((v5c - v38) * v29)), (v4c + v25 & v55) < 0x23)))), 9, 0),
    (And(And(((v5b | v2f) & v4e) < (v4d + v48 & v40), ((v44 | v5b) + v2e) < ((v41 ^ v2e) & v53)), And(0x42 < (v39 * v51 ^ v36), And(((v29 + v4c) - v34) < ((v30 | v41) - v48), ((v38 | v5b) * v43) < (v2d ^ v4c | v35)))), 1, 0),
    (And(And(0x59 < ((v57 | v26) ^ v55), 0x33 < (v45 & v2d & v54)), (v27 * v30 ^ v40) < (v3f * v4d ^ v31)), 2, 0),
    (And(And(((v3e + v3c) - v43) < 0x61, 0xc1 < ((v45 & v3a) + v25)), ((v33 ^ v38) + v28) < (v55 + v49 & v59)), 5, 0),
    (And(And(((v43 | v5c) & v26) < 0x41, (v52 + v51 * v43) < 3), (v54 * v32 ^ v5c) < ((v53 | v4b) + v55)), 7, 0),
    (And(And(And(((v57 | v2d) ^ v32) < ((v49 & v59) + v4b), 0xb < ((v3d ^ v46) & v2b)), (v31 - v38 ^ v4e) < 0xd1), And((v2f + v39 * v2d) < 0xf9, (v30 * v33 - v31) < (v30 ^ v49 ^ v36))), 10, 0),
    (And(0x84 < (v2d * v25 - v57), (v3c + v49 & v31) < 0x26), 6, 0),
    (((v56 & v40) - v42) < 0xef, 6, 0),
    (And(((v52 & v27) * v2b) < ((v3b ^ v4f) - v5b), 0xae < ((v50 & v45) + v58)), 3, 0),
    (And(0x49 < ((v57 ^ v33) * v4c), ((v59 ^ v45) + v3d) < 0xc5), 9, 0),
    (And(And(And(0x67 < ((v45 & v40) * v31), ((v4b & v55) - v5c) < (v34 * v31 * v47)), 0x42 < (v2a | v31 | v3f)), And(And(99 < (v52 & v54 | v46), ((v29 & v44) + v41) < (v44 * v45 * v58)), And((v35 + v2b | v54) < 0x6e, And(0xf9 < (v5a * v34 - v50), ((v2c | v40) * v3d) < 0x3d)))), 6, 0),
    (And(And(And(((v4c | v41) - v59) < ((v3e | v3b) * v2d), 0x9d < ((v47 & v4c) + v4d)), (v5a * v5b | v50) < 0xcd), (v30 & v35 | v4e) < (v42 + v43 ^ v46)), 4, 0),
    (And(And(((v2a ^ v39) + v26) < (v28 + v39 + v44), 0xd2 < ((v25 ^ v55) * v35)), And((v59 * v27 & v49) < (v40 + v25 ^ v3f), ((v4c | v2a) & v30) < (v51 & v41 ^ v4e))), 10, 0),
    (And(And((v4b + v44 + v5c) < (v28 * v43 | v53), (v30 - v32 | v3f) < (v4c + v58 & v52)), And(0xe7 < ((v34 | v56) + v48), And(((v27 & v38) - v58) < ((v3a - v42) + v5b), 0x3d < (v38 + v47 * v49)))), 3, 0),
    (And(And(((v3d + v52) * v41) < ((v5a ^ v3c) & v58), 0xbb < (v31 * v46 - v41)), And((v2d & v49 | v28) < 0x39, And(And(And((v2d - v32 & v57) < 3, ((v25 ^ v56) - v49) < (v4e | v52 - v57)), ((v29 & v4c) + v36) < ((v35 ^ v53) + v48)), ((v45 | v2e) * v35) < ((v28 | v5a) - v2d)))), 6, 0),
    (And(And((v2f & v37 & v41) < (v4d - (v26 + v55)), And(And(((v3b & v25) * v34) < ((v28 | v25) & v56), 0x5a < (v46 & v34 | v57)), (v3c | v56 & v26) < ((v3f + v3b) * v47))), And(And((v48 ^ v37 | v43) < (v58 - v43 | v2a), (v2c + v45 & v3b) < ((v5b & v2f) * v48)), And(((v2e | v58) & v45) < (v2a * v58 * v3a), And(0x6c < (v39 & v32 | v56), ((v2b ^ v51) + v4f) < (v52 ^ v57 ^ v42))))), 9, 0),
    (And(And(And(((v30 | v3a) * v39) < ((v44 ^ v30) * v4a), 0x8d < (v32 & v4c | v4d)), (v48 + v46 * v44) < 0x12), And((v2b * v46 * v54) < 0x31, ((v31 ^ v45) * v42) < ((v32 - v3c & v35) + 0x41))), 3, 0),
    (And(And(((v2d | v38) - v27) < ((v32 | v53) ^ v45), And(((v39 & v25) - v51) < (v55 & v45 & v30), 0x24 < (v34 + v3c * v32))), And(((v2e + v44) - v52) < ((v4b ^ v55) * v48), And(And((v33 + v45 & v34) < 0x60, ((v3b - v39) * v30) < ((v29 & v44) + v41)), (v48 - v2b | v3e) < 0x6d))), 6, 0),
    (And(And(((v46 - v4a) + v44) < ((v48 + v45) * v3a), 0x10 < ((v58 ^ v3c) - v2a)), And(0x8a < (v3c - v54 ^ v4e), ((v40 & v33) - v50) < (v27 ^ v48 | v25))), 9, 0),
    (And(And(0x39 < ((v54 | v25) - v59), (v49 * v38 * v48) < ((v30 + v38) * v45)), 2 < ((v33 ^ v30) * v42)), 3, 0),
    (And(And((v29 ^ v5c ^ v2d) < 0x5b, ((v51 | v42) + v37) < 0x82), 0x82 < (v5b - v3a ^ v3b)), 8, 0),
    (And(((v2b + v38) - v4e) < (v4b & v35 | v51), ((v34 | v2b) & v51) < 0x36), 3, 0),
    (And(And(And(((v3a | v2c) * v4a) < ((v49 ^ v48) & v2b), (v27 & v53 | v40) < 0x2d), And(((v59 | v3c) + v3a) < 0xbc, 0x80 < (v3e * v5a | v48))), And((v3f ^ v4f | v3c) < (v36 - v32 & v33), ((v3c | v2b) - v36) < (v52 ^ v33 | v26))), 8, 0),
    (And(And((v52 - (v4a + v29)) < (v57 | v50 | v3d), 0xd5 < ((v41 ^ v2a) + v4d)), And((v5a - v58 & v37) < 0x35, And(And((v31 * v57 ^ v5a) < 0xb6, ((v2f | v37) ^ v4b) < 0xc), ((v51 * v4c | v3a) + 0x4d) < ((v5b & v27) * v52)))), 5, 0),
    (And(And(0x4f < (v2e + v3f ^ v50), (v35 ^ v36 | v32) < 0x86), And(0xae < (v5c + v58 * v51), 0xfc < (v53 * v32 | v58))), 1, 0),
    (And(And((v35 ^ v34 ^ v50) < ((v2b - v48) * v50), 0x7a < ((v25 + v53) - v4f)), And((v2b - (v4a + v42)) < 0xf2, ((v3e - v3a) * v3c) < 3)), 9, 0),
    (And(And(And((v59 + v51 + v50) < 0xca, 0x4f < (v2e & v59 ^ v48)), 0x2a < (v2c & v35 & v2d)), ((v3c | v2d) & v30) < ((v4d + v58) * v53)), 8, 0),
    (And(0x95 < (v5a - v52 ^ v27), And(And((v32 + v27 + v4b) < (v4d & v52 | v5c), ((v4d + v5a) - v3f) < (v2a + v4d & v5b)), (v45 ^ v27 ^ v55) < (v39 & v54 ^ v31))), 3, 0),
    (And(And(((v58 + v4d) * v53) < ((v2a ^ v59) - v49), ((v50 & v45) * v52) < 0xfd), And(And(((v2e & v36) * v47) < (v26 & v56 | v3c), (v29 * v3f - v3c) < (v2a - (v50 + v47))), And((v4e & v52 | v46) < (v32 & v49 | v52), (v3b ^ v3f & v2e) < 0x56))), 4, 0),
    (And(And(((v4f ^ v3a) - v39) < ((v58 | v2e) & v45), ((v44 & v59) - v53) < 0xdb), (v3c ^ (v58 | v4f)) < (v4a * v31 ^ v41)), 6, 0),
    (And(And((v36 * v29 ^ v2a) < (v2c - v47 ^ v4e), 0xc2 < (v57 + v3a ^ v3c)), And(0x13 < ((v30 ^ v27) & v39), ((v2b - v48) * v50) < ((v42 | v39) ^ v4e))), 8, 0),
    (And(And(((v32 | v30) - v47) < (v48 & v34 & v42), ((v35 ^ v3c) - v37) < (v4a & v40 & v2c)), And(0x39 < ((v56 | v2d) & v53), And(((v38 + v27) - v54) < (v36 * v28 - v57), ((v4f & v53) - v3c) < ((v33 + v59) * v51)))), 6, 0),
    (And(And(((v33 - v34) * v4c) < ((v46 & v3f) - v37), (v5a + v25 | v34) < 0xfd), ((v38 ^ v30) + v27) < (v32 + v27 + v4b)), 4, 0),
    (And(And(((v42 - v3e) * v40) < 0x5e, ((v41 | v58) * v42) < 100), And((v3b - v53 | v35) < 0x2b, And((v39 & v54 ^ v31) < (v36 - v48 & v45), (v43 * v58 ^ v4a) < (((v55 | v35) ^ v47) + 0x83)))), 1, 0),
    (And(((v36 + v5b) - v53) < ((v27 & v29) * v41), And(0x60 < ((v51 + v3b) * v31), ((v4f ^ v3b) - v5b) < (v26 * v3b & v42))), 9, 0),
    (And(And(And(And((v43 * v2a - v37) < (v4e * v43 ^ v2d), (v54 - (v31 + v55)) < (v30 ^ v59 ^ v3c)), ((v3f | v49) + v42) < 0x6c), And(0x2c < (v33 + v44 * v2f), 0x92 < ((v4d + v48) - v5b))), ((v3d & v56) * v39) < (v3d & v49 & v26)), 1, 0),
    (And(And(0x7b < (v3f + v51 | v56), ((v59 + (v34 ^ v3d)) - 0x25) < ((v45 ^ v31) * v42)), And(0x42 < ((v29 | v59) - v51), And((v44 * v41 | v25) < 0xe2, ((v4a | v50) - v28) < (v2a + v55 | v3f)))), 2, 0),
    (And(And(And(((v28 ^ v48) * v2d) < (v33 ^ v58 | v27), And(((v36 | v27) * v57) < 0x46, (v36 * v28 - v57) < ((v45 | v2d) + v51))), And((v2b & v58 ^ v48) < 0x58, ((v4b & v2a) - v2c) < (v39 * v2b * v54))), And(And(((v40 + v30) - v4c) < ((v4e ^ v56) & v38), (v4e ^ v27 | v4b) < ((v3c + v48) * v2b)), ((v5c | v27) * v59) < ((v50 | v2d) & v46))), 6, 0),
    (And(And(And((v34 - v28 ^ v58) < 0x5e, (v4e | v51 | v5b) < (v41 * v26 * v2b)), And((v4c ^ v27 ^ v3c) < 0x7b, And((v33 ^ v48 | v2e) < ((v51 - v50) * v56), (v38 * v54 - v2c) < ((v32 | v38) - v48)))), (v46 + v47 & v31) < ((v4d & v3e) - v3d)), 10, 0),
    (And(And(And((v3e & v59 | v3c) < (v4c * v4b ^ v34), 0x2f < ((v3a | v32) - v2a)), ((v35 ^ v31) + v2d) < ((v57 - v28) * v39)), ((v45 ^ v48) * v4b) < (v33 ^ v3e | v3a)), 6, 0),
    (And(And((v4b * v44 ^ v5c) < (v25 * v3c & v32), (v2d - (v30 + v31)) < 0xe2), ((v4d & v44) + v35) < (v3b * v4a | v3a)), 7, 0),
    (And(And((v3c * v27 - v4d) < 0xc0, ((v31 ^ v57) * v32) < ((v5c ^ v32) + v2a)), And(0x2e < (v3f ^ v43 | v2c), And(((v3e + v41) * v38) < ((v2e ^ v5a) & v3a), ((v2d | v5a) ^ v49) < (v42 + v2b ^ v45)))), 10, 0),
    (And(And(((v3e & v4d) - v3d) < (v5b ^ v36 | v40), 2 < (v27 + v41 & v51)), ((v3a & v55) - v2b) < ((v2e | v36) + v29)), 9, 0),
    (And(And(0x7e < ((v3e ^ v4e) * v33), (v4d - (v26 + v55)) < ((v4f ^ v54) & v57)), And(2 < (v49 - v2e & v27), And((v30 * v42 | v59) < (v34 | v30 | v29), 0x13 < (v47 * v4d & v2c)))), 7, 0),
    (And(0xe9 < (v4a + v36 + v32), And(And(And(And((v5c & v27 ^ v58) < (v28 + v36 & v27), (v5a + v44 + v43) < ((v26 | v27) & v41)), (v31 ^ v2c ^ v51) < 0x33), And(0x3c < (v39 * v37 & v5b), (v46 + v3a * v58) < 0xe6)), (v33 ^ v3e | v3a) < (v39 & v31 - v44))), 8, 0),
    (And(And((v42 * v4c | v40) < ((v54 | v3a) - v3d), 0xe6 < ((v34 + v3d) * v2a)), And(((v37 | v3d) - v25) < ((v4d | v50) ^ v30), (v45 - v38 & v4b) < 0x3e)), 1, 0),
    (And(And(And(((v42 - v53) * v31) < (v37 | v59 | v5c), (v2c & v35 & v2d) < 0x2b), (v43 - (v3f + v5a)) < (v40 & v53 | v31)), And(((v25 + v2a) - v4d) < 0x4e, ((v53 - (v34 + v51)) - 0x27) < ((v2f + v30) * v4b))), 1, 0),
    (And(And((v55 | v34 | v5a) < 0x7c, ((v25 - v4d) + v5c) < (v3b + v3f ^ v30)), (v33 + v44 * v2f) < 0x2d), 9, 0),
    (And(And(0xfc < (v41 - v3a | v34), 0xce < ((v26 + v29) * v28)), And(((v3c & v3d) + v52) < 0xa6, And(And(0xe4 < ((v57 & v35) * v4d), ((v2d ^ v5c) - v33) < (v3f & v52 | v55)), ((v43 + v3b) * v34) < ((v27 ^ v5a) - v3d)))), 7, 0),
    (And(And(0xad < ((v3f + v48) * v55), (v4b * v4d | v2c) < (v40 + v3c + v51)), And(0x67 < ((v43 ^ v5c) & v34), 2 < (v3e + v40 & v38))), 3, 0),
    (And(And((v4c + v57 + v2c) < ((v51 + v44) * v3f), 2 < (v4b & v41 ^ v27)), And(0xfc < (v59 * v27 ^ v2b), And(2 < ((v29 ^ v50) * v42), ((v35 & v57) * v4d) < 0xe5))), 5, 0),
    (And(0xa8 < ((v4e | v5b) + v57), (v28 ^ v3d | v41) < 0x5e), 1, 0),
    (And(And((v3c - v37 ^ v52) < ((v42 | v5b) & v33), (v4a | v3c | v32) < 0x36), (v45 & v32 | v44) < 0x30), 7, 0),
    (And(And(0x78 < (v3f + v3d * v28), (v37 + v47 + v59) < 0xbd), ((v27 + v30) * v46) < 0xcd), 4, 0),
    (And(And(0x29 < ((v5b ^ v49) & v2e), 0xd1 < (v2a - (v32 + v44))), (v59 | v5b | v4b) < ((v44 - v36) * v4b)), 7, 0),
    ((v2d & v30 ^ v34) < 0x68, 10, 0),
    (And(And(And(((v45 ^ v48) & v32) < 0x11, (v5a + v46 ^ v48) < (v37 ^ v48 | v43)), (v3a + v35 & v2f) < 0xc), (v5c ^ v47 ^ v27) < 5), 7, 0),
    (And((v2c * v34 * v2b) < (v38 * v27 | v2e), And(And(0x23 < (v46 & v4a & v28), 0x17 < ((v4e | v2f) ^ v46)), And(((v37 - v54) * v31) < (v48 + v29 & v25), 0x1a < (v46 & v4a & v50)))), 2, 0),
    (And(And(((v55 | v43) * v29) < 0xf, ((v4c ^ v29) + v2b) < (v3e * v57 | v4c)), (v50 * v29 * v35) < ((v2d | v2b) + v37)), 2, 0),
    (And(And(((v59 ^ v2a) - v49) < ((v2d | v3c) & v30), (v5c & v45 ^ v37) < 0x6e), ((v32 & v45) - v36) < (v27 * v59 & v49)), 4, 0),
    (And(And((v44 * v45 * v58) < ((v3b - v39) * v30), (v3b + v3a * v57) < 0x1c), ((v42 + v59) * v5b) < ((v2d + v31) * v30)), 2, 0),
    (And(9 < ((v31 - v27) + v2c), And(And((v49 - v45 ^ v52) < ((v33 | v3c) + v4d), ((v58 | v3c) & v5a) < (v48 + v29 ^ v2f)), And(And((v26 * v3c - v2c) < ((v47 + v33) - v4f), And(And((v3b ^ v5b | v25) < 0x83, ((v36 | v2d) & v53) < (v5c ^ v45 | v4b)), (v35 & v4b | v51) < (v4a & v48 | v37))), (v3f + v28 * v3d) < 0x79))), 8, 0),
    (And(And((v33 ^ v59 ^ v4f) < 0x36, ((v2c | v3b) + v59) < 0x9d), And(0x22 < ((v3d ^ v36) - v50), 0xf3 < ((v40 | v42) - v36))), 5, 0),
    (And(((v42 | v4d) * v56) < 0xe8, 0x73 < (v54 + v4c + v39)), 10, 0),
    (And(And(And(((v55 + v4a) - v51) < 0x52, ((v3d - v37) * v4f) < 0x6c), (v2c * v2d | v56) < (v57 & v31 & v48)), ((v45 + v48) * v3a) < (v4d - v59 | v53)), 1, 0),
    (And(((v3a + v51) - v40) < (v4c - v53 & v52), And(And(((v38 | v28) * v53) < ((v2f & v29) + v2b), 0x21 < (v35 - v25 & v38)), And(((v50 | v45) + v52) < (v4d | v28 * v40), ((v4b | v3a) * v44) < 0xd5))), 2, 0),
    (And(And(((v2a + v27) - v29) < ((v35 + v45) * v51), 0x36 < ((v59 ^ v53) - v29)), And(0x2c < (v40 | v53 & v27), ((v39 & v32) + v55) < (v30 + v58 ^ v34))), 9, 0),
    (And(And(((v57 + v4a) * v4c) < ((v30 & v58) + v5a), 0x25 < ((v3b | v47) & v2d)), (v26 & v40 & v29) < ((v34 | v2e) & v55)), 2, 0),
    (And(And(((v5c - v4e) * v53) < 0xbb, (v3f - v31 & v59) < ((v58 ^ v59) - v5c)), And(((v44 ^ v58) & v42) < (v4c * v4a ^ v45), 0xd4 < ((v3a | v4b) * v44))), 5, 0),
    (And(((v40 | v4b) & v48) < (v3b + v30 | v38), 0x94 < ((v35 ^ v5c) * v34)), 1, 0),
    (And(And((v2b * v51 | v38) < ((v4a & v5a) + v51), ((v3d | v48) + v28) < 0x8f), (v3c + v59 + v27) < ((v4e | v36) & v2b)), 4, 0),
    (And(And(0x2f < ((v3f & v40) * v4c), (v35 + v27 | v3c) < ((v2a | v56) * v25)), And(((v33 ^ v57) * v4c) < 0x4a, ((v42 ^ v59) & v4b) < 0x5d)), 5, 0),
    (And(And(0x51 < ((v38 | v2e) & v56), ((v3b | v59) ^ v3d) < (v5b * v52 ^ v3d)), And((v4f + v51 ^ v29) < 100, And((v38 - v3f | v58) < (v34 + v44 ^ v25), 0x42 < ((v57 | v51) ^ v56)))), 9, 0),
    (And(And(And(And((v48 & v4a | v37) < ((v2b + v38) - v4e), ((v59 | v29) + v51) < (v47 * v29 * v2a)), 0x99 < ((v2d & v56) * v55)), 0x10 < (v44 - v58 & v5c)), And(And(((v49 & v44) * v27) < (v43 & v27 | v41), 0x38 < (v27 ^ v48 ^ v43)), 0x33 < ((v3d | v3e) & v2b))), 4, 0),
    (And(And(((v40 | v56) - v4c) < ((v58 | v3c) & v5a), 0x96 < ((v45 & v54) * v5a)), (v3b * v29 * v37) < 0x7d), 6, 0),
    (And(And(And(And(0x6d < (v2b + v35 | v54), ((v5a | v35) & v4f) < 0x3e), 0x2b < ((v2e + v43) - v3c)), And(((v3a ^ v43) & v41) < ((v2a & v4c) - v36), ((v46 | v32) * v54) < (v34 * v2b * v2c))), ((v30 | v53) * v36) < ((v52 & v3d) - v3f)), 9, 0),
    (And(And((v26 + v48 | v41) < ((v30 ^ v26) * v46), (v3a & v3f | v29) < 0x2a), And(And((v3e * v41 | v39) < (v36 + v41 + v58), And(And(((v2c ^ v3e) * v36) < 0x3d, (v2c | v3a | v2d) < (v55 & v3e & v47)), (v5c + v43 + v25) < 3)), (v49 + v4d * v55) < 0x16)), 1, 0),
    (And(And(((v53 ^ v35) + v48) < ((v58 | v3c) & v33), And((v44 ^ v3c ^ v29) < (v3b & v44 & v3e), ((v41 + v42) * v29) < (v52 + v46 & v51))), And(And((v27 & v44 | v33) < ((v34 + v55 & v29) + 0x34), And(0x69 < ((v3a + v2f) * v34), ((v40 & v52) + v4f) < 0x57)), 0xc5 < ((v2d ^ v27) + v3a))), 6, 0),
    (And(0x23 < (v58 + v2d & v28), (v30 + v58 ^ v34) < (v4b + v2d + v41)), 3, 0),
    (And(And(((v2f + v49) - v2c) < ((v28 | v37) ^ v4c), 0x51 < (v26 + v2f | v34)), ((v30 + v27) * v40) < (v39 + v30 + v36)), 8, 0),
    (And(0x22 < (v5c - v56 & v4f), 0x69 < (v2c & v35 | v59)), 2, 0),
    (And(4 < (v32 & v4f ^ v44), And(And((v4c + v2c | v56) < ((v51 + v3c) - v49), ((v40 & v4c) - v34) < 0xb3), And((v40 - v56 & v37) < 0x43, 0x1d < (v3b - v4f ^ v29)))), 1, 0),
    (And(And(((v25 ^ v41) & v46) < 3, 0x66 < ((v2e + v36) - v40)), ((v2b | v3c) ^ v38) < (v41 - v56 ^ v45)), 9, 0),
    (And(And(0x10 < (v26 * v29 ^ v5a), ((v25 ^ v3b) * v49) < 3), And(0x70 < ((v2f & v51) + v32), 0x38 < (v58 + v55 * v26))), 3, 0),
    (And(0xe9 < ((v3f + v45) - v58), 0xca < ((v43 & v32) * v4d)), 2, 0),
    (And(And(And((v4e * v2b * v2c) < ((v3d ^ v5c) - v4d), ((v50 & v54) - v39) < ((v33 + v42) * v3c)), 0x20 < (v28 * v35 & v27)), (v25 * v3c & v32) < (v47 * v51 * v30)), 1, 0),
    (And(And((v50 + v41 ^ v38) < (v4e * v5c - v2b), (v30 + v3b | v38) < (v26 * (v30 ^ v5c))), And((v32 + v2c ^ v3e) < 6, And((v54 + v3a | v4e) < (v3f - v31 & v59), ((v5a ^ v3c) & v58) < (v35 + v56 & v27)))), 6, 0),
    (And(And(And(((v42 | v5b) & v33) < ((v41 + v48) - v5a), (v44 & v26 | v52) < 0x8f), ((v55 ^ v3a) + v2c) < (v54 - (v55 + v31))), And(((v4d & v4e) * v39) < ((v35 | v2c) + v5a), 0x2b < (v3d & v2f | v28))), 9, 0),
    (And(And(((v45 & v29) * v37) < (v47 & v3f ^ v29), ((v26 + v29) * v28) < 0xcf), And((v36 & v31 ^ v49) < 0x12, And(((v46 ^ v27) * v44) < 0x99, ((v2d ^ v27) + v3a) < 0xc6))), 5, 0),
    (And(And(And(((v41 | v30) ^ v47) < 0x3b, ((v2f & v3b) - v52) < (v46 - v4a & v29)), ((v25 & v48) * v37) < 0x3c), And(And(0x8e < (v4e * v28 ^ v50), ((v2b | v3f) - v3d) < 5), ((v37 + v29) - v39) < ((v58 | v4b) ^ v33))), 6, 0),
    (And(And(0x58 < ((v57 ^ v45) + v52), (v2e - v59 & v3b) < (v3a + v47 + v2c)), (v44 + v2f & v38) < ((v4f & v53) - v3c)), 2, 0),
    (And(((v3d ^ v5c) - v4d) < (v48 + v34 * v29), ((v53 & v3c) + v35) < 0x6f), 3, 0),
    (And(And(And((v50 - v5c ^ v3c) < ((v30 + v27) * v40), (v53 | v49 | v33) < 0x3d), 0x3b < (v39 ^ v3f ^ v47)), (v32 & v4b & v3b) < (v31 - v35 & v26)), 1, 0),
    (And(And((v44 * v4d * v3e) < ((v37 - v39) + v29), ((v27 & v43) - v34) < 0xb8), And(0x4e < ((v5b | v56) * v3d), ((v3b ^ v5c) + v39) < ((v30 ^ v25) & v3b))), 7, 0),
    (And((v4c * v4a ^ v45) < (v46 * v28 ^ v4e), (v42 * v29 ^ v2b) < 0x78), 6, 0),
    (And(And(0x14 < (v50 + v34 * v42), (v49 * v5a & v3d) < (v46 | v56 | v28)), (v52 ^ v42 ^ v57) < (v41 * v30 | v34)), 4, 0),
    (And(And(((v5a - v30) + v48) < (v37 * v25 & v44), (v2a & v56 ^ v54) < 0x17), (v2c + v47 + v3a) < (v2f + v30 ^ v25)), 3, 0),
    (And(And(0x37 < (v3d ^ v42 ^ v2c), ((v55 | v58) & v48) < 0x6a), And(0x65 < (v4b ^ v50 | v2e), And(And(0xce < ((v4c | v26) - v4b), (v31 & v4d ^ v2a) < (v35 | v4c & v3d)), 0x17 < (v3a & v56 ^ v58)))), 10, 0),
    (And(And((v52 - v53 ^ v4f) < ((v40 ^ v26) * v48), 0x9f < ((v34 ^ v36) - v33)), ((v5b ^ v2e) & v55) < (v29 + v41 + v3f)), 2, 0),
    (And(And(0xad < (v39 + v35 + v3e), ((v5b & v38) + v32) < (v3a + v4e ^ v54)), And(And(((v58 ^ v25) + v53) < (v3c - v48 ^ v3f), ((v30 ^ v25) & v3b) < (v4b * v2e ^ v3c)), And(0xbd < (v36 + v53 + v2a), And(And((v44 + v57 & v4c) < (v42 | v4e | v3d), 0xc2 < (v53 | v38 * v35)), (v4d + v48 & v40) < (v4b * v48 * v2c))))), 10, 0),
    (And(And(((v49 | v35) - v3f) < ((v29 & v45) * v37), (v2d ^ v28 | v4e) < (v48 + v40 ^ v34)), And((v3b * v35 & v49) < ((v5c + v29) - v53), And((v4a & v49 & v3c) < 0x3e, ((v52 | v48) ^ v2e) < 0x59))), 4, 0),
    (And(And(((v38 | v56) & v2e) < ((v33 ^ v38) + v28), ((v54 + v4e) * v38) < 0x1f), ((v2a & v54) * v2e) < (v32 - v29 ^ v4f)), 1, 0),
    (And(And(And(0x3a < (v3e ^ v47 ^ v38), (v52 * v5b ^ v3d) < ((v3d + v47) - v2d)), And((v43 * v3a | v3b) < ((v40 ^ v5b) & v48), (v3e - v40 ^ v42) < 0x13)), And((v29 * v43 ^ v3a) < ((v3a - v40) + v51), (v5a + v51 ^ v58) < ((v29 | v48) ^ v3d))), 10, 0),
    (And(And(((v2c + v3e) - v39) < ((v30 | v53) * v36), 0x48 < ((v28 | v43) ^ v34)), And((v2b * v36 * v48) < 0x53, (v4f - v55 ^ v40) < (v31 + v3b * v41))), 6, 0),
    (And(And((v5a + v29 + v36) < (v54 - v2f | v3d), (v41 * v2b * v26) < (v53 & v4c ^ v3d)), And(And(And(((v3f & v46) - v37) < (v59 + v44 * v56), ((v30 ^ v41) * v3b) < 0x30), (v2d + v54 ^ v40) < ((v38 | v47) & v26)), (v28 & v59 | v54) < ((v34 ^ v37) & v42))), 2, 0),
    (And(And(((v59 + v33) * v51) < (v2f + v44 & v38), ((v31 ^ v4f) + v55) < (v43 + v28 | v5c)), And(((v4b | v58) & v45) < ((v39 | v27) - v47), (v27 & (v58 ^ v51)) < 0x46)), 5, 0),
    (And(((v28 | v37) ^ v4c) < ((v39 | v4f) + v48), (v4d * v51 & v3c) < 0x18), 5, 0),
    (And(And(And(((v51 - v4d) * v4c) < ((v28 | v45) * v50), ((v44 & v47) + v4d) < 0x7d), ((v4b ^ v58) * v52) < 0x4d), (v3e - (v33 + v31)) < ((v3b ^ v52) * v43)), 5, 0),
    (And(0x7c < ((v46 | v39) + v31), And(And(0x2e < ((v4f + v46) - v3b), (v30 - v3b ^ v38) < (v49 * v3b | v36)), (v53 * v3d * v5a) < ((v2c | v3a) * v4a))), 9, 0),
    (And(And(0xe6 < (v35 - (v53 + v51)), 0xa4 < (v2f * v28 - v46)), (v3b + v3f ^ v30) < ((v38 ^ v34) + v47)), 4, 0),
    (And(And((v2a + v4d & v5b) < (v31 | v2c | v2b), 0x4a < ((v48 - v4d) + v56)), (v36 - v48 & v45) < (v27 ^ v45 ^ v55)), 3, 0),
    (((v4a ^ v2e) - v50) < 0xe9, 3, 0),
    (And(And((v40 - v3a ^ v55) < ((v51 - v4d) * v4c), (v34 + v3c * v32) < 0x25), And(And((v53 * v52 & v39) < 0x23, And((v2a | v2e | v37) < 0x87, (v45 ^ v4f ^ v25) < ((v26 | v2e) * v51))), ((v48 ^ v2e) * v30) < ((v42 ^ v3c) * v41))), 8, 0),
    (And(And(And(((v3d | v50) ^ v28) < ((v37 ^ v28) - v3e), (v3b + v4a ^ v30) < 0xa9), ((v29 & v2f) + v2b) < ((v41 + v29) * v45)), (v27 | v2f | v2d) < ((v40 | v58) + v4e)), 1, 0),
    (And(((v28 + v2e) * v4f) < (v33 * v30 - v31), 0xc0 < (v32 - v56 | v36)), 7, 0),
    (And((v33 ^ v58 | v27) < ((v25 & v59) * v26), And(And(And((v44 + v56 + v2e) < (v51 ^ v2b | v56), ((v30 & v44) + v3b) < 0x91), And(0x89 < ((v29 & v44) + v34), And(And(0xd9 < ((v2f - v4d) * v53), ((v57 | v26) ^ v55) < 0x5a), (v4b - (v34 + v50)) < (v41 * v3e | v39)))), ((v46 | v56) * v30) < 0x17)), 6, 0),
    (And(And((v39 + v35 + v3e) < 0xae, 0xe8 < (v4a + v3e | v50)), And(And(0xfc < (v3f - v38 ^ v33), And((v31 + v30 ^ v53) < (v56 & v38 & v44), ((v5c ^ v30) * v26) < ((v4b | v40) & v48))), ((v58 | v40) + v4e) < (v2a + v34 * v3f))), 6, 0),
    (And(And(And(((v47 + v52) - v2f) < (v38 * v48 * v49), (v3d + v48 & v54) < 0x19), (v4c & v3d | v35) < (v29 + v41 * v2a)), And(And(0xb3 < (v2d * v5b * v58), 0x3c < ((v40 | v2c) * v3d)), ((v4e | v5b) + v57) < 0xa9)), 7, 0),
    (And(And(0x60 < ((v3e + v3c) - v43), (v52 + v43 & v42) < ((v45 & v40) + v55)), And(199 < (v37 * v5a - v31), And(And(((v48 | v52) ^ v3d) < 0x61, ((v28 & v3c) - v34) < ((v3d | v37) - v25)), 4 < ((v2b | v3f) - v3d)))), 9, 0),
    (And(((v3d ^ v46) & v2b) < 0xc, And(And((v2a - v40 | v58) < (v35 - (v5a + v4b)), ((v32 - v3c & v35) + 0x41) < ((v59 + (v34 ^ v3d)) - 0x25)), And((v55 + v33 ^ v41) < 0xd7, And(0x85 < ((v38 & v2a) * v50), (v5c - v56 & v4f) < 0x23)))), 6, 0),
    (And(And(And(And((v43 & v37 & v3a) < ((v36 ^ v35) * v3c), (v32 * v53 | v58) < 0xfd), 0x31 < (v47 + v58 & v30)), And(((v54 + v25) * v29) < 0x49, ((v5b & v57) - v33) < 0xae)), (v2d | v3c | v55) < (v59 - v3a & v51)), 5, 0),
    (And(And((v4a * v3b | v3a) < (v2b * v3a & v2e), (v32 - v52 | v25) < 0xf3), ((v39 + v58) * v55) < 0xcb), 4, 0),
    (And(((v44 + v51) * v3f) < (v41 - v4a | v57), And(And(And(0x5a < (v29 ^ v2d ^ v5c), (v34 | v29 | v30) < (v28 + v27 | v55)), 2 < (v26 * v2d & v51)), And((v59 + v42 + v5b) < 0xdf, (v26 - (v52 + v4d)) < (v40 | v55 | v53)))), 9, 0),
    (And(And(((v27 ^ v2b) * v3e) < (v53 & v38 & v2e), (v5c - (v27 + v5a)) < (v59 * (v5c | v27))), And(And(((v29 - v44) * v41) < ((v31 ^ v57) * v32), ((v3c ^ v58) - v2a) < 0x11), And(And((v4a * v54 | v2e) < 0xc0, And(And(((v3b + v3f) * v47) < ((v36 & v2e) * v47), ((v43 | v37) - v51) < 0x43), ((v44 - (v5a + v57)) + 0x73) < (v5c * v27 * v37))), 2 < (v4f + v38 & v3e)))), 5, 0),
    (And(And(And(0x2d < ((v42 | v2c) & v3f), ((v28 + v5c) - v4d) < (v48 - (v55 + v40))), ((v43 + v2c) * v3e) < ((v2f ^ v4b) + v55)), And(And(((v2d | v2c) + v33) < 0x83, (v2d - v2c & v52) < (v5a * v49 & v3d)), 0x18 < ((v5a - v37) + v32))), 8, 0),
    (And(0x38 < (v2d & v49 | v28), 0x33 < (v42 + v49 ^ v5c)), 9, 0),
    (And(And(And((v25 - (v3e + v55)) < (v34 + v36 | v29), ((v26 | v4a) ^ v43) < 3), (v33 ^ v52 | v26) < ((v3c ^ v57) - v44)), ((v3f ^ v4d) * v3d) < (v39 ^ v3f ^ v46)), 4, 0),
    (And(And(((v41 & v5b) + v29) < ((v4e + v46) - v40), ((v38 | v57) ^ v4b) < 0x18), And((v56 & v38 & v44) < ((v49 | v38) - v3c), 99 < (v4f ^ v25 | v4d))), 5, 0),
    (And(((v2b & v31) + v4b) < ((v37 & v5b) * v34), (v39 & v4c ^ v3b) < 0x57), 8, 0),
    (And(And(And(((v50 & v56) * v34) < (v3d + v55 & v3a), (v48 * v5c | v28) < (v2f * v35 & v3a)), (v25 | v3a | v27) < 0x7f), And(And((v5a - v43 | v4b) < (v3e & v3d | v58), 0x33 < (v2b + v57 * v50)), ((v4c | v45) ^ v46) < (v3b & v4b & v32))), 1, 0),
    (And(And((v52 ^ v4a ^ v59) < ((v3a & v55) - v2b), ((v2d + v4a) - v3c) < ((v4d | v37) ^ v2f)), And(0x72 < (v54 + v2c | v4e), 0x33 < (v4e - v52 & v30))), 6, 0),
    (And(And(And(((v57 | v51) ^ v56) < 0x43, (v29 ^ v41 ^ v3c) < 0x6d), 0xcb < (v2f + v3a ^ v28)), 0x91 < (v5b - (v3e + v3f))), 2, 0),
    (And(And(And((v4a - v4c ^ v26) < 0x2d, 0x31 < ((v2c + v29) * v2b)), And(((v27 + v53) * v2e) < 0xaf, And(0x8f < (v37 & v41 | v25), (v3a * v58 * v2a) < ((v4f ^ v3a) - v39)))), ((v38 + v25) * v46) < 0x1e), 3, 0),
    (And(And(0x82 < (v4a - (v46 + v40)), (v31 + v41 * v3b) < ((v39 | v50) - v2e)), (v49 * v57 & v50) < 0x3b), 4, 0),
    (And(0x3d < (v45 - v38 & v4b), And(And((v2b * v3a & v2e) < ((v44 & v4d) + v35), (v5a * v4d & v39) < 0x14), And(((v26 - v3a) + v36) < (v50 ^ v39 | v25), (v3f | v2f | v41) < 0x7f))), 9, 0),
    (And(And(((v35 ^ v50) & v28) < ((v4c & v32) * v59), ((v2f & v3c) + v32) < ((v2a & v51) + v42)), And(0x59 < (v54 ^ v58 ^ v39), And(0xca < (v55 * (v39 + v58)), (v40 * v54 & v25) < (v55 | v3c | v2d)))), 9, 0),
    (And(0x1d < (v46 - v31 ^ v51), And(And(And(((v25 ^ v26) - v58) < 0xb4, 0x21 < ((v52 ^ v26) - v4c)), ((v3d & v4d) + v53) < ((v30 ^ v40) & v31)), And(((v32 ^ v33) - v2c) < (v44 * v41 ^ v2b), ((v4f | v58) + v36) < (v59 & v28 | v54)))), 1, 0),
    (And((v45 & v51 & v49) < 0x26, (v2d * v25 - v57) < 0x85), 3, 0),
    (And(((v2f + v30) * v4b) < (((v4c | v4a) & v58) + 0x42), And(And(And((v3e - (v2a + v53)) < ((v35 - v54) + v2c), 0x93 < ((v55 + v37) * v2f)), 0x91 < ((v58 - v2f) + v28)), And(And((v2a - (v32 + v44)) < 0xd2, (v5c * v37 * v27) < (((v51 + v42) - v36) + 0x1a)), And(8 < (v47 * v2a - v35), ((v50 | v36) + v53) < ((v2d | v57) ^ v32))))), 1, 0),
    (And(And(0x54 < (v2f ^ v28 ^ v5b), ((v36 | v2e) + v29) < (v59 ^ v52 ^ v4a)), (v53 * v42 * v2a + 0x41) < ((v51 * v4c | v3a) + 0x4d)), 1, 0),
    (And(0xf1 < (v35 + v4c * v34), (v39 - v47 | v56) < (v2c + v45 & v3b)), 1, 0),
    (And(And(And(0x58 < (v3d & v59 | v27), ((v4a + v3e) * v57) < (v39 + v3f + v25)), 0xcc < (v38 | v57 * v3d)), And(And(((v4f - v37) + v49) < ((v52 + v2a) - v42), (v2d ^ v2a | v27) < ((v33 ^ v43) - v2f)), 0x59 < (v28 * v3a | v3b))), 10, 0),
    (And(And(((v2d | v52) ^ v34) < (v40 - v4f ^ v32), ((v3a | v29) + v3d) < 0xd1), And((v52 - v2e | v30) < (v4c ^ v2a ^ v36), And((v4d | v4c & v32) < 0x8e, ((v41 ^ v2e) & v53) < ((v28 ^ v54) + v4f)))), 10, 0),
    (And(And(((v29 ^ v3a) - v2a) < ((v4f ^ v2a) + v29), ((v3e + v34) * v4a) < 0x38), (v53 & v28 ^ v40) < ((v25 ^ v58) + v53)), 5, 0),
    (And(And((v2b + v2c | v30) < (v42 - v54 ^ v45), 0x60 < (v57 | v58 | v35)), And(((v39 | v47) ^ v37) < ((v33 & v4d) + v5b), (v4e & v35 | v4c) < (v3c + v59 + v27))), 5, 0),
    (And((v58 ^ v2a | v55) < 0x53, (v48 | v49 | v33) < 0x6c), 1, 0),
    (And(And(And(And(And((v55 ^ v4b | v44) < ((v2e + v44) - v52), (v46 + v49 & v44) < 0xf), (v27 * v59 ^ v2b) < 0xfd), And(0x5d < ((v42 - v3e) * v40), 2 < (v49 - v3c & v40))), ((v43 ^ v34) * v4c) < 0x34), 0x42 < ((v3d - v2e) + v47)), 6, 0),
    (And(And(0x56 < ((v52 & v40) + v4f), 0x2c < ((v43 - v3e) + v36)), And(((v59 | v29) - v51) < 0x43, (v39 + v51 | v3a) < ((v49 | v34) * v3d))), 5, 0),
    (And(And(And(And(0xfc < (v29 * v51 ^ v5a), ((v4c & v51) - v52) < (v30 - v32 | v3f)), ((v2a | v28) ^ v34) < 0x4d), And(0x3c < (v49 | v33 | v53), (v56 - v42 | v2d) < (v5a + v4a * v3a))), ((v47 + v51) * v3a) < 0x71), 5, 0),
    (And(And((v5b * v53 - v3b) < 5, (v2a + v34 * v3f) < (v2d | v2f | v27)), 0xd3 < (v32 * v3b | v45)), 3, 0),
    (And(And(((v48 + v41) - v5a) < (v3c - v37 ^ v52), (v50 - v32 & v2b) < (v44 + v5a + v43)), 0x21 < ((v4e | v57) * v58)), 3, 0),
    (And(And(0x62 < (v3a & v4e | v28), (v27 + v34 * v35) < (v2a ^ v2d | v27)), And(And((v4c & v53 ^ v3d) < (v51 | v4e | v5b), And((v4d - v59 | v53) < ((v46 - v4a) + v44), 0xe0 < ((v25 + v48) * v27))), ((v2e | v55) & v42) < (v25 * v28 & v41))), 10, 0),
    (And((v51 ^ v4f ^ v3a) < ((v58 | v4f) ^ v3c), And(And(And(0x44 < ((v2f | v3f) ^ v4e), (v4e - v52 & v30) < 0x34), 2 < (v2b & v59 & v26)), And(((v43 ^ v33) - v2f) < (v27 + v35 * v34), 0x42 < ((v37 | v43) - v51)))), 5, 0),
    (And(And(((v2f & v4f) - v3b) < ((v2a | v5b) - v29), (v2e + v3f ^ v50) < 0x50), 0x73 < ((v56 + v4a) - v57)), 3, 0),
    (And(And(And(0x6f < (v29 * v2e - v2f), (v56 + v4b * v5a) < 0x3e), ((v58 | v38) & v45) < ((v27 ^ v2b) * v3e)), (v4f - (v58 + v53)) < ((v54 ^ v5a) + v48)), 10, 0),
    (And(And(((v5a ^ v54) + v48) < (v2c ^ v3c ^ v27), (v46 | v25 | v37) < 0x7a), And(((v34 + v33) - v4f) < 100, And((v36 + v3b ^ v2d) < ((v50 & v54) - v39), ((v45 & v36) * v2a) < ((v4d ^ v44) * v41)))), 7, 0),
    (And(And(((v5c ^ v30) + v2f) < (v36 * v29 ^ v2a), 0xe < ((v43 - v27) * v33)), (v3c ^ v58 ^ v4d) < 0x32), 9, 0),
    (And(And((v3c * v59 & v54) < ((v36 + v26) - v3a), 0x6e < (v2a + v3c | v39)), (v2f * v35 & v3a) < (v5b | v55 | v4e)), 3, 0),
    (And(And(0x79 < (v46 | v37 | v25), ((v5b & v2f) * v48) < (v39 - v47 | v56)), And((v53 & v31 ^ v3c) < 3, (v43 & v48 | v3d) < (v59 - (v51 + v5c)))), 6, 0),
    (And(And((v3c * v3d & v2f) < ((v42 - v53) * v31), 0xc < (v27 - v5b & v4c)), (v29 - (v47 + v54)) < 0xdd), 8, 0),
    (And(And(((v30 | v2d) ^ v2a) < 5, (v40 & v2c & v4a) < (v28 + v32 | v54)), And(0xcb < ((v55 + v58) * v53), And((v3b * v26 & v42) < ((v52 & v27) * v2b), (v35 - (v53 + v51)) < 0xe7))), 8, 0),
    (And(0x3b < (v2f * v4e ^ v34), ((v28 ^ v50) * v39) < (v3c ^ v44 ^ v29)), 8, 0),
    (And(And(0x50 < (v57 ^ v3e ^ v32), (v41 * v2c & v45) < 0x3b), 0x45 < (v31 - v33 ^ v5a)), 10, 0),
    (And(And(And(And(((v2b + v4b) * v55) < ((v42 + v59) * v5b), ((v3c | v33) + v4d) < ((v4e + v3a) - v3d)), And(0x4c < ((v37 | v42) - v40), And(0x47 < ((v4a ^ v5b) - v54), 0x69 < ((v58 | v55) & v48)))), 0x10 < ((v53 | v51) ^ v2d)), And((v4f * v5a & v3c) < 0x23, (v26 ^ v3b ^ v2a) < ((v38 | v2d) - v27))), 4, 0),
    (And(And(And((v47 - v3b ^ v58) < (v39 * v42 | v5a), ((v49 ^ v36) + v41) < (v2e * v29 | v3a)), (v3f - v38 ^ v33) < 0xfd), ((v40 ^ v49) & v48) < 3), 1, 0),
    (And(((v40 | v4f) + v45) < ((v39 | v47) ^ v37), And(And(And((v4c - v55 ^ v25) < ((v5c ^ v2d) - v33), 0x27 < (v34 * v47 & v38)), And(0x1d < (v38 * v5c - v2e), And((v30 ^ v3c ^ v59) < ((v3a ^ v55) + v2c), ((v5a & v5c) + v51) < (v28 ^ v2d | v4e)))), And(0x8e < (v26 & v44 | v52), (v2f + v4e | v56) < ((v49 | v33) * v44)))), 5, 0),
    (And(((v44 ^ v4d) * v41) < (v51 * v40 - v45), And(And(And((v52 & v28 | v2d) < ((v35 ^ v31) + v2d), (v4e + v35 & v46) < 3), (v31 ^ v4d ^ v36) < (v27 & v5c ^ v58)), 0x10 < (v2a * v30 & v3c))), 10, 0),
    (And(And(And((v31 * v46 - v41) < 0xbc, 0x55 < ((v29 - v42) * v26)), (v51 ^ v46 - v31) < 0x1e), And(And((v56 & v4a & v39) < ((v54 & v4e) + v25), 0x10 < ((v48 ^ v45) & v32)), (v59 - v3a & v51) < (v40 * v54 & v25))), 8, 0),
    (And(And(0x4b < ((v2b ^ v2d) + v5c), ((v34 ^ v37) & v42) < ((v58 | v4f) + v36)), (v3e * v57 | v4c) < (v52 + v51 + v40)), 7, 0),
    (And(And(((v35 | v2b) & v27) < 0x24, (v4d * v3f ^ v31) < (v37 & v53 | v55)), 6 < (v5c ^ v54 ^ v48)), 5, 0),
    (And(And(0xb7 < ((v2d & v4b) * v3f), (v49 * v38 & v41) < (v52 - v33 & v37)), 0x7c < ((v4d | v37) & v4b)), 2, 0),
    (And(And((v54 ^ v4e ^ v2f) < 0x60, ((v2b - v3f) * v4d) < 0x1a), And((v4a + v2d * v2c) < (v43 * v2a - v37), (v58 & v30 | v37) < ((v4c | v2a) & v30))), 2, 0),
    (And(And(And((v53 | v55 | v40) < ((v2d | v52) * v5a), 0x11 < (v48 + v44 * v46)), (v40 - v57 & v3f) < (v4d + v3e * v5b)), And(And(((v42 ^ v57) & v35) < ((v34 | v37) - v56), ((v33 + v42) * v3c) < (v36 + v3b ^ v2d)), And(((v51 | v4f) - v48) < 0xe2, ((v39 | v42) ^ v4e) < (v34 ^ v35 ^ v50)))), 9, 0),
    (And((((v4c | v4a) & v58) + 0x42) < ((v53 - (v34 + v51)) - 0x27), And(And(0x58 < ((v52 | v48) ^ v2e), 0x6c < (v3c ^ v29 ^ v41)), And(0xae < ((v27 + v53) * v2e), And(And(And((v4e ^ v52 | v46) < 0x5d, (v47 * v2b - v38) < ((v43 - v46) + v33)), 0xb < ((v2f | v37) ^ v4b)), 0x40 < ((v5c | v43) & v26))))), 3, 0),
    (And(And(0x46 < ((v4a ^ v57) + v31), (v55 & v47 & v3e) < ((v5b + v30) * v2c)), And((v4e + v33 * v29) < (v4c * v56 & v50), And(((v25 ^ v2f) + v46) < (v49 * v5a ^ v43), (v2d ^ v4c | v35) < ((v41 - v46) * v35)))), 1, 0),
    (And(And(And((v42 | v4e | v3d) < ((v4a | v3c) ^ v48), (v29 + v48 ^ v2f) < ((v40 | v56) - v4c)), 8 < ((v2d + v26) - v36)), And(((v2a & v38) * v50) < 0x86, (v41 + v57 ^ v2a) < ((v39 ^ v2a) + v26))), 8, 0),
    (And(And(((v5c ^ v47) - v53) < 0x25, 0xfc < (v4b * v4d | v4a)), ((v49 | v34) * v3d) < (v3c ^ (v53 | v47))), 3, 0),
    (And(And(((v3d | v4a) + v4d) < 0x81, ((v53 | v28) + v44) < (v49 * v38 & v41)), (v55 ^ v52 ^ v3b) < 0x4a), 4, 0),
    (And(And((v4a + v54 ^ v32) < 0x62, 0x5f < (v3a & v55 | v2a)), 0x42 < (v40 - v56 & v37)), 9, 0),
    (And(And(And((v32 & v39 | v56) < 0x6d, 0x46 < ((v28 | v2b) * v4e)), ((v51 | v40) - v2a) < 0xfd), And(And((v45 + v4d ^ v29) < (v46 & v38 ^ v34), ((v3d | v39) - v48) < (v54 * v38 - v2c)), (v53 - (v51 + v33)) < ((v50 & v56) * v34))), 9, 0),
    (And(And(And(((v53 + v43) - v40) < (v4a + v4d & v51), 0x8d < ((v2d ^ v32) * v2a)), And((v46 & v58 & v27) < 0x6f, And((v3d ^ v2c ^ v42) < 0x38, 0xd7 < ((v3e & v42) - v5a)))), (((v55 | v35) ^ v47) + 0x83) < (((v3a ^ v42) - v52) - 0x2c)), 10, 0),
    (And(And(And(((v55 & v35) * v39) < ((v4c | v41) - v59), ((v4e | v35) * v44) < 0xfd), (v47 + v56 * v25) < (v36 + v2e | v26)), ((v5c | v39) ^ v47) < ((v30 | v32) - v47)), 8, 0),
    (And(And(((v25 & v59) * v26) < ((v48 ^ v28) * v2d), ((v51 | v3c) * v4c) < 0xe5), 0x17 < (v48 - v2a & v3f)), 3, 0),
    (And(And(((v29 & v44) + v34) < 0x8a, 0x20 < ((v35 ^ v3a) - v26)), And((v32 + v34 + v2f) < (v52 + v43 & v42), And(((v5a + v43) * v3c) < (v4c * v42 | v40), ((v4e | v35) + v45) < (v2e + v57 ^ v30)))), 2, 0),
    (And(And((v57 | v50 | v3d) < ((v25 & v5b) * v38), (v36 - v32 & v33) < (v40 + v52 | v43)), 0xfc < (v3a + v40 | v4b)), 2, 0),
    (And(And((v3f & v52 | v55) < (v4c - v55 ^ v25), (v45 * v54 * v2c) < 0x88), And(0x53 < (v2a * v2c * v44), And((v47 ^ v38 ^ v3e) < 0x3b, ((v48 | v3a) - v33) < 0x39))), 8, 0),
    (And(And(((v49 & v59) + v4b) < ((v36 | v50) + v53), 0x27 < ((v3f | v58) & v31)), ((v25 ^ v4b) * v43) < 0x50), 3, 0),
    (And(And(0x61 < ((v2c - v2f) * v29), ((v27 & v5b) * v52) < (v53 * v2a * v42 + 0x41)), 0x40 < ((v4f - v29) + v31)), 5, 0),
    (And(And((v47 ^ v2a | v34) < (v4c + v35 | v42), 0x15 < (v56 * v29 ^ v35)), And((v4a + v54 ^ v44) < 0x65, And(((v5c + v29) - v53) < (v2c - (v4c + v4d)), (v41 & v5c | v3e) < (v2f - (v5c + v43))))), 6, 0),
    (And(And((v47 * v42 * v5c) < (v2c + v2b | v30), ((v35 + v45) * v51) < ((v3d & v2b) * v25)), And(And(And(And(((v37 ^ v28) - v3e) < ((v57 ^ v3b) & v43), (v52 * v2f | v41) < (v3a * v43 | v3b)), 0x44 < (v49 ^ v2c | v44)), And(0x7d < ((v3c & v42) + v39), (v54 * v47 | v34) < ((v50 ^ v35) & v28))), (v3c + v25 + v54) < ((v28 + v5c) - v4d))), 7, 0),
    (And((v54 * v50 - v2a) < (v41 + v50 ^ v38), And(And((v4c - v53 & v52) < (v29 * v43 ^ v3a), (v56 * v4c & v50) < (v5a | v52 | v4f)), And((v30 * v25 - v2e) < 0x30, ((v4d + v52) - v26) < ((v28 - v40) * v32)))), 7, 0),
    (And(And(And((v53 * v30 & v3a) < (v4e + v2f | v56), (v3d + v37 & v46) < 3), ((v28 ^ v2d) * v25) < ((v2e ^ v37) - v40)), And((v35 * v3e * v5a) < 0x42, (v58 & v28 ^ v4b) < (v29 - (v49 + v3f)))), 7, 0),
    (And(And((v26 + v37 & v45) < (v47 - v3b ^ v58), 0x4c < ((v4b ^ v58) * v52)), And(0xd2 < ((v4c | v44) * v3e), ((v42 | v37) - v40) < 0x4d)), 7, 0),
    (And(And((v4f - (v4b + v29)) < 0xbd, ((v3d + v47) - v2d) < ((v59 | v3b) ^ v3d)), And(2 < (v5c + v43 + v25), And(((v52 ^ v3b) * v43) < (v44 - v38 ^ v51), (v42 + v43 ^ v46) < (v34 * v31 & v55)))), 7, 0),
    (And(And((v29 * v2a * v47) < (v5c + v59 ^ v47), 0x56 < (v31 | v39 | v4d)), 0x42 < ((v2d ^ v4f) + v54)), 8, 0),
    (((v37 | v2a) + v2e) < 0xd2, 10, 0),
    (And(And(((v41 ^ v28) - v30) < 0x1c, (v47 * v33 * v55) < 0x2e), And(((v34 | v2e) & v55) < (v3d * v2c | v4c), (v3c * v3d - v36) < ((v37 ^ v57) & v29))), 2, 0),
    (And(And(0x12 < ((v52 | v4c) * v4b), 0x52 < ((v49 + v3a) - v3f)), ((v2d | v2b) + v37) < ((v3b | v37) - v25)), 5, 0),
    (And((v31 + v4c ^ v5a) < 0x3f, ((v48 ^ v49) & v2b) < (v3d * v5a * v53)), 2, 0),
    (And(And(And(((v3d | v3e) & v2b) < 0x34, (v4c | v33 | v53) < (v2d + v54 ^ v40)), (v31 & v30 ^ v43) < 3), 0xa2 < (v39 - v2d ^ v45)), 3, 0),
    (And(And(0x5d < (v34 - v28 ^ v58), ((v4c ^ v59) * v32) < (v25 | v57 | v45)), And(0x33 < ((v43 ^ v34) * v4c), And((v5c | v48 | v44) < (v26 * v3c - v2c), (v56 & v54 | v35) < 0x31))), 4, 0),
    (And(And(((v5b + v3b) * v4c) < (v56 - v42 | v2d), 0x98 < (v58 + v45 ^ v38)), ((v46 & v37) + v3f) < (v34 * v2e ^ v27)), 10, 0),
    (And(And((v41 & v29 | v4f) < 0x36, 0x84 < (v44 + v40 + v2f)), And((v4b & v41 ^ v27) < 3, And((v4e * v43 ^ v2d) < (v4a + v2c * v2d), (v3f + v51 | v56) < 0x7c))), 10, 0),
    (And(And(And((v34 * v47 * v31) < (v2c + v3d ^ v2d), ((v4e | v2f) ^ v46) < 0x18), 0x61 < (v4a & v50 | v3b)), And((v48 | v50 | v4c) < 0x8a, ((v36 ^ v3d) - v50) < 0x23)), 8, 0),
    (And(And(((v50 | v4d) ^ v30) < ((v3c & v28) - v34), 0x71 < ((v25 - v31) * v39)), And((v4d + v5b * v3e) < (v47 + v3f + v2b), ((v3a & v31) * v4c) < (v29 | v5a | v56))), 1, 0),
    (And(((v5b & v4e) - v35) < 0x11, (v58 - v49 | v25) < ((v56 ^ v25) - v49)), 8, 0),
    (And((v4e + v3a ^ v54) < ((v26 | v47) & v3a), And(And(And((v29 - (v49 + v3f)) < ((v5a & v38) * v5c), (v26 - (v49 + v52)) < 0x8a), ((v35 | v2c) + v5a) < (v4f - v32 ^ v50)), ((v2a + v52) - v42) < ((v3d ^ v44) + v26))), 1, 0),
    (And(((v28 | v45) * v50) < (v40 - v3a ^ v55), And(And((v43 * v28 | v53) < (v26 + v5c | v59), (v44 - v38 ^ v51) < (v3e - (v33 + v31))), And((v46 & v38 ^ v34) < ((v57 ^ v45) + v4e), And((v3c - v3d | v57) < 0x3c, (v5c + v59 + v4c) < ((v27 & v38) - v58))))), 6, 0),
    (And(And(((v2e ^ v5a) & v3a) < ((v4b | v52) + v2a), (v57 + v3a ^ v3c) < 0xc3), (v4e + v4c & v3b) < 3), 6, 0),
    (And(And(((v48 ^ v4c) & v28) < ((v2a & v54) * v2e), 0xcc < (v36 + v4a ^ v50)), And((v43 - v3b & v28) < 0xc, And(((v56 ^ v37) - v2d) < 0xd0, (v31 - v33 ^ v5a) < 0x46))), 7, 0),
    (And(0xd1 < (v54 * v53 - v3c), (v3c - v48 ^ v3f) < (v28 & v53 ^ v40)), 3, 0),
    (And(And((v43 & v5c & v38) < 3, (v5b - v3a ^ v3b) < 0x83), (v2c | v2b | v31) < ((v5a - v3f) + v4d)), 2, 0),
    (And(And((v28 + v44 + v39) < (v41 + v57 ^ v2a), 0x51 < (v2f * v41 - v47)), And(0xdf < (v33 + v2a * v39), (v5a * v49 ^ v43) < ((v55 - v26) * v44))), 10, 0),
    (And(And((v51 * v40 - v45) < ((v36 & v45) * v2a), 4 < (v55 + v38 & v31)), (v27 & v57 ^ v39) < ((v37 - v54) * v31)), 6, 0),
    (And(And(And(((v45 & v40) * v31) < 0x68, 0x6b < (v33 | v49 | v48)), (v52 ^ v56 | v37) < (v30 - v3b ^ v38)), And((v4d | v2b | v3d) < 0x95, ((v4b & v28) - v3a) < (v2f - v5b | v4f))), 8, 0),
    (And(And((v55 ^ v37 | v53) < 0x41, 0x17 < ((v5c ^ v4e) * v3e)), (v41 - v4a | v57) < (v2c + v57 + v4c)), 7, 0),
    (And(And(And(((v54 ^ v4f) & v57) < (v37 & v41 & v2f), 0xce < (v5a + v51 ^ v46)), (v48 & v57 & v31) < (v57 - (v41 + v3d))), (v45 * v51 - v4d) < (v35 + v27 | v3c)), 4, 0),
    (And((v5b + v3d & v54) < 0x3a, And((v2e * v4b ^ v3c) < ((v5c ^ v3b) + v39), ((v47 | v4b) - v53) < ((v43 + v3b) * v34))), 10, 0),
    (And(And(((v3a + v2c) - v2e) < 0x68, 0x80 < ((v3d | v4a) + v4d)), And(((v50 | v34) ^ v3f) < 0x4b, And(0xc9 < (v37 * v34 | v49), (v35 - (v5a + v4b)) < (v5b + v34 ^ v4d)))), 7, 0),
    (And(And(And((v3f ^ v31 | v4b) < 0x66, ((v45 ^ v2d) & v5c) < ((v3e | v3d) ^ v59)), 0xb7 < ((v43 & v27) - v34)), (v49 & v32 | v52) < (v42 - v56 ^ v47)), 6, 0),
    (And(9 < ((v3b | v2a) * v42), ((v2c - v2f) * v29) < 0x62), 6, 0),
    (And(((v5c & v25) - v40) < 0x1c, ((v5b + v30) * v2c) < (v2d | v2c | v3a)), 10, 0),
    (And(And(And(((v34 ^ v2b) & v50) < (v43 - (v3f + v5a)), 0x45 < (v30 * v44 - v54)), ((v37 | v4d) & v4b) < 0x7d), ((v31 + v2d) * v30) < (v55 * (v4b + v2b))), 5, 0),
    (And(And((v59 + v44 * v56) < ((v33 - v34) * v4c), 0xd8 < (v40 * v55 - v50)), And((v29 * v26 ^ v5a) < 0x11, And((v5a * v44 - v2d) < 0xdb, (v3d & v26 & v49) < (v51 | v34 | v52)))), 9, 0),
    (And(And(And(((v3f | v2f) ^ v4e) < 0x45, ((v3e ^ v58) - v5a) < 0xa9), ((v2c & v38) * v51) < 0xcd), And(And((v2b + v3f + v47) < (v40 - v57 & v3f), 0x3c < (v5a - v33 ^ v3a)), 0x22 < (v52 * v53 & v39))), 3, 0),
    (And(And((v5a * v52 * v4d) < ((v3a & v31) * v4c), (v3b - v30 | v4d) < 0x5c), And(((v59 ^ v3b) * v40) < 0x37, And(And((v5a - v33 ^ v3a) < 0x3d, (v3e & v3d | v58) < (v48 + v47 * v41)), ((v2b & v3d) * v25) < ((v2a + v27) - v29)))), 7, 0),
    (And((v26 + v5c | v59) < (v44 + v5c + v4b), And(And((v31 - v35 & v26) < ((v4c | v45) ^ v46), ((v38 | v49) - v3c) < (v30 + v31 ^ v53)), And(((v3e | v4b) ^ v35) < (v4e + v5a * v45), 0x73 < (v39 + v59 | v4d)))), 9, 0),
    (And(And(0xdc < (v29 - (v47 + v54)), (v28 * v3a | v3b) < 0x5a), And(0xc0 < (v32 + v5c | v50), 0xd8 < ((v31 + v50) * v5a))), 1, 0),
    (And((v46 & v50 & v4a) < 0x1b, And(And(And(And(And((v3b - v4f ^ v29) < 0x1e, 0x7c < (v29 * v3b * v37)), 0x67 < ((v3a - v2e) + v2c)), And(((v38 | v4f) + v33) < 0x89, ((v28 - v40) * v32) < ((v2f | v3b) & v47))), 0x65 < ((v26 | v28) ^ v36)), (v34 + v4a | v3d) < ((v30 - v34) + v25))), 7, 0),
    (And(10 < ((v28 - v3b) + v43), ((v33 ^ v30) * v42) < 3), 7, 0),
    (And(And(0xd6 < (v2e + v54 * v3e), (v57 * v50 * v43) < 0xfd), 0x3b < ((v48 & v25) * v37)), 5, 0),
    (And(0x23 < ((v2a ^ v3b) * v32), (v49 + v46 & v34) < ((v57 + v4a) * v4c)), 7, 0),
    (And(And((v33 * v3c * v39) < ((v46 & v37) + v3f), (v44 & v3c | v4f) < ((v5b ^ v2e) & v55)), And(0x9e < ((v5c & v4f) - v59), (v48 & v42 & v34) < (v47 ^ (v5c | v39)))), 7, 0),
    ((v46 & v52 | v27) < 0x65, 8, 0),
    (And(And(And(((v42 ^ v3c) * v41) < ((v2f & v29) - v4f), ((v3e & v42) - v5a) < 0xd8), 99 < ((v58 | v41) * v42)), And(((v47 | v44) - v36) < 0xe1, (v45 * (v29 + v41)) < ((v28 | v38) * v53))), 4, 0),
    (And(And((v44 * v41 ^ v2b) < ((v54 & v51) + v59), ((v4a & v42) - v2a) < 0xd9), And(((v3f ^ v4e | v30) - 0x2a) < ((v28 | v41) ^ v29), And(((v57 - v28) * v39) < (v52 & v28 | v2d), ((v3b | v37) - v25) < (v50 * v29 * v35)))), 4, 0),
    (And(And(And(((v2c ^ v26) * v59) < 0x82, ((v27 & v29) * v41) < ((v5a ^ v59) * v3b)), (v41 - v57 ^ v4b) < ((v40 & v33) - v50)), 0x9a < ((v4c ^ v4f) * v53)), 6, 0),
    (And(And(2 < (v2b + v41 & v4d), (v40 * v32 * v34 - 8) < (v27 & v44 | v33)), And((v2a - (v50 + v47)) < (v53 & v4d & v3b), 0x18 < (v3d + v48 & v54))), 7, 0),
    (And(0xa2 < ((v4f & v37) - v52), 0x35 < ((v40 | v34) - v31)), 7, 0),
    (And(And(((v54 ^ v35) & v2b) < ((v50 ^ v2f) - v27), ((v5b ^ v40) & v48) < (v52 * v2f | v41)), 0x41 < ((v4d | v2d) ^ v30)), 6, 0),
    (0x2f < (v59 - v47 | v49), 9, 0),
    (And(And(And((v2a ^ v4c ^ v36) < ((v5c | v27) & v3f), 0x46 < ((v41 | v40) * v45)), And((v5b - (v3f + v3e)) < 0x92, And(0x35 < (v29 & v41 | v4f), 0xc9 < (v50 + v51 + v59)))), 0xd5 < (v28 - (v49 + v33))), 8, 0),
    (And(And(And(((v38 ^ v34) + v47) < ((v25 - v4d) + v5c), 0x53 < (v3e & v38 | v2f)), ((v48 + v3f) * v55) < 0xae), (v45 * v38 & v3c) < ((v57 | v50) & v58)), 6, 0),
    (And(And((v30 + v2f ^ v25) < (v2e - v59 & v3b), ((v37 | v4d) ^ v2f) < ((v27 - v2c) * v5b)), And(((v56 & v50) + v41) < 0x9b, And(((v54 & v51) + v59) < ((v32 ^ v33) - v2c), ((v25 + v30) - v34) < (v4b + v25 & v46)))), 4, 0),
    (And(And(And(0x4a < ((v27 | v5b) ^ v2a), (v5a * v3e | v48) < 0x81), 0x1b < ((v41 ^ v28) - v30)), And((v4d * v53 & v3c) < (v39 & v4a & v56), ((v32 | v53) ^ v45) < (v26 ^ v2a ^ v3b))), 4, 0),
    (And(And(((v53 ^ v48) - v32) < 0x25, (v33 | v53 | v37) < (v3e - (v53 + v2a))), ((v56 | v2a) * v25) < (v51 * v45 - v4d)), 6, 0),
    (And(And(And((v39 * v42 | v5a) < (v37 + v26 & v45), (v3c & v4f & v44) < 0x31), (v56 & v3a ^ v58) < 0x18), And(((v59 ^ v5a) * v3b) < ((v5b + v36) - v53), 0x15 < (v49 + v55 * v4d))), 5, 0),
    (And(((v39 | v4f) + v48) < ((v2f + v49) - v2c), 0x7b < (v33 * v50 | v3a)), 4, 0),
]

def print_model(model):
    flag = ""
    for var in reversed(vars):
        flag += chr(model.evaluate(var.val).as_long())

    # > 0x5f2 (> 1522) was needed
    max_score = model.evaluate(objective)
    print(f"score: {max_score} | {flag}")


objective = 0
for i, (condition, score, _) in enumerate(ifs):
    # Possibly minor improvement with add_soft, but not much
    # opt.add_soft(condition, score)
    objective += simplify(condition) * score

opt.set_on_model(print_model)
opt.maximize(objective)
# Still print flag on cancel, due to set_on_model not strictly necessary though
try:
    check_result = opt.check()
    print(check_result)
except:
    pass

print("=====")
print_model(opt.model())
