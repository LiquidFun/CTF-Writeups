#!uv run
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "z3-solver",
# ]
# ///
import z3

def solve_constraints():
    """
    Uses the Z3 SMT solver to find byte values for variables local_55 to local_16
    that maximize the number of satisfied conditions from the provided C code snippet.
    """
    solver = z3.Optimize()

    # Define the variables: local_55 down to local_16 as 8-bit BitVectors (bytes)
    # 0x55 - 0x16 + 1 = 0x40 = 64 variables
    locals_bv = {}
    for i in range(0x16, 0x55 + 1):
        var_name = f"local_{i:x}"
        locals_bv[var_name] = z3.BitVec(var_name, 8)

    # Helper function to get variable BitVec by name
    def get_bv(name):
        # Check if the name is like local_XX
        if name.startswith("local_") and len(name) == 8:
             return locals_bv[name]
        else:
            # Handle potential errors if name format is unexpected
            raise ValueError(f"Unexpected variable name format: {name}")

    # List to hold the Z3 boolean expressions for each condition
    conditions = []

    # --- Translate C conditions to Z3 constraints ---
    # Note: (byte)(a + b) == c means the lower 8 bits of (a + b) equals c.
    #       Since we are using BitVec(8), addition is automatically modulo 256.
    # Note: Negative constants in C byte comparisons are treated as their
    #       unsigned 8-bit representation (two's complement).
    #       e.g., -0x70 == 0x90, -0x7f == 0x81, -1 == 0xff

    conditions.append(get_bv("local_3a") == 0x32)
    conditions.append((get_bv("local_36") ^ get_bv("local_3d")) == 0xaa)
    conditions.append((get_bv("local_36") + get_bv("local_27")) == 0x90) # -0x70
    conditions.append((get_bv("local_1a") + get_bv("local_31")) == 0x81) # -0x7f
    conditions.append(get_bv("local_48") == 0xbe)
    conditions.append(get_bv("local_35") == 100)
    conditions.append(get_bv("local_3b") == 0x31)
    conditions.append(get_bv("local_2b") == 0x39)
    conditions.append((get_bv("local_28") + get_bv("local_16")) == 0x93) # -0x6d
    conditions.append(get_bv("local_23") == 0x31)
    conditions.append((get_bv("local_54") + get_bv("local_46")) == ord('8'))
    conditions.append((get_bv("local_48") ^ get_bv("local_32")) == 0x8e)
    conditions.append((get_bv("local_54") ^ get_bv("local_27")) == 0x71)
    conditions.append(get_bv("local_2b") == 0xb4) # Conflicting with local_2b == 0x39
    conditions.append(get_bv("local_42") == 0x36)
    conditions.append(get_bv("local_39") == get_bv("local_25"))
    conditions.append((get_bv("local_4b") ^ get_bv("local_34")) == 3)
    conditions.append(get_bv("local_37") == 0x76)
    conditions.append(get_bv("local_50") == 0x32)
    conditions.append((get_bv("local_54") ^ get_bv("local_25")) == 0x85)
    conditions.append(get_bv("local_53") == 0x54)
    conditions.append(get_bv("local_3e") == 0xe1)
    conditions.append((get_bv("local_4c") ^ get_bv("local_1f")) == 0x81)
    conditions.append((get_bv("local_20") + get_bv("local_3b")) == ord('a'))
    conditions.append((get_bv("local_43") ^ get_bv("local_1c")) == 7)
    conditions.append((get_bv("local_43") ^ get_bv("local_50")) == 0x56)
    conditions.append((get_bv("local_47") + get_bv("local_20")) == ord('f'))
    conditions.append((get_bv("local_25") ^ get_bv("local_1d")) == 0x54)
    conditions.append(get_bv("local_21") == 0xe5)
    conditions.append(get_bv("local_31") == ord('o'))
    conditions.append((get_bv("local_30") + get_bv("local_37")) == ord('f'))
    conditions.append(get_bv("local_23") == 0x31) # Duplicate
    conditions.append(get_bv("local_3e") == 0x38) # Conflicting with local_3e == 0xe1
    conditions.append(get_bv("local_2e") == ord('4'))
    conditions.append((get_bv("local_1d") + get_bv("local_42")) == 0x97) # -0x69
    conditions.append((get_bv("local_42") ^ get_bv("local_23")) == 0x2d)
    conditions.append((get_bv("local_33") + get_bv("local_54")) == 0xa4) # -0x5c
    conditions.append((get_bv("local_26") + get_bv("local_2f")) == 0xf4) # -0xc
    conditions.append((get_bv("local_3a") + get_bv("local_26")) == 0x97) # -0x69
    conditions.append((get_bv("local_26") + get_bv("local_4b")) == 0x96) # -0x6a
    conditions.append(get_bv("local_53") == 0x72) # Conflicting with local_53 == 0x54
    conditions.append(get_bv("local_1a") == 0x36)
    conditions.append(get_bv("local_39") == 0xb1) # Conflicts with local_39 == local_25 potentially
    conditions.append((get_bv("local_4d") ^ get_bv("local_1b")) == 8)
    conditions.append((get_bv("local_53") ^ get_bv("local_27")) == 0x3a)
    conditions.append(get_bv("local_1a") == 0x44) # Conflicting with local_1a == 0x36
    conditions.append(get_bv("local_1c") == 0x12)
    conditions.append((get_bv("local_44") ^ get_bv("local_2d")) == 0x5b)
    conditions.append(get_bv("local_2c") == 0x2a)
    conditions.append(get_bv("local_2c") == 0x33) # Conflicting with local_2c == 0x2a
    conditions.append((get_bv("local_3b") + get_bv("local_2f")) == ord('?'))
    conditions.append((get_bv("local_18") ^ get_bv("local_55")) == 0x60)
    conditions.append(get_bv("local_40") == 0x24)
    conditions.append((get_bv("local_50") + get_bv("local_2a")) == ord('-'))
    conditions.append(get_bv("local_1c") == 99) # Conflicting with local_1c == 0x12
    conditions.append((get_bv("local_1e") ^ get_bv("local_21")) == 5)
    conditions.append(get_bv("local_51") == 0x7b)
    conditions.append((get_bv("local_45") + get_bv("local_4c")) == 0xad) # -0x53
    conditions.append((get_bv("local_3f") + get_bv("local_28")) == 0x98) # -0x68
    conditions.append(get_bv("local_3d") == 0x32)
    conditions.append(get_bv("local_25") == 0x35) # Conflicts with local_39 == local_25 and local_39 == 0xb1 potentially
    conditions.append((get_bv("local_1f") ^ get_bv("local_42")) == 0x5b)
    conditions.append((get_bv("local_1f") + get_bv("local_47")) == 0x99) # -0x67
    conditions.append(get_bv("local_20") == 0xd2)
    conditions.append((get_bv("local_55") ^ get_bv("local_25")) == 0x65)
    conditions.append((get_bv("local_2b") + get_bv("local_24")) == 0x9a) # -0x66
    conditions.append((get_bv("local_41") + get_bv("local_38")) == 0x96) # -0x6a
    conditions.append((get_bv("local_2d") ^ get_bv("local_23")) == 0xda)
    conditions.append((get_bv("local_19") + get_bv("local_35")) == 0x96) # -0x6a
    conditions.append((get_bv("local_2e") + get_bv("local_4e")) == 0x98) # -0x68
    conditions.append(get_bv("local_23") == get_bv("local_4b")) # Conflicts with local_23 == 0x31 potentially
    conditions.append((get_bv("local_1c") ^ get_bv("local_4b")) == 0x52)
    conditions.append(get_bv("local_1d") == 0x61)
    conditions.append(get_bv("local_41") == 0x61)
    conditions.append((get_bv("local_17") ^ get_bv("local_4d")) == 1)
    conditions.append((get_bv("local_29") ^ get_bv("local_33")) == 0x30)
    conditions.append(get_bv("local_34") == 0x32)
    conditions.append((get_bv("local_26") ^ get_bv("local_24")) == 4)
    conditions.append((get_bv("local_3a") ^ get_bv("local_3f")) == 0x53)
    conditions.append((get_bv("local_55") + get_bv("local_2c")) == 0x83) # -0x7d
    conditions.append(get_bv("local_43") == 0xf1)
    conditions.append(get_bv("local_39") == 0x35) # Conflicting with local_39 == 0xb1 and local_39 == local_25
    conditions.append(get_bv("local_45") == 0xd3)
    conditions.append((get_bv("local_4f") + get_bv("local_26")) == 0x99) # -0x67
    conditions.append((get_bv("local_39") + get_bv("local_3c")) == 0xaf) # -0x51
    conditions.append((get_bv("local_16") + get_bv("local_42")) == 0xb3) # -0x4d
    conditions.append(get_bv("local_38") == 0x35)
    conditions.append(get_bv("local_18") == 0x30)
    conditions.append((get_bv("local_46") + get_bv("local_3c")) == 0x85) # -0x7b
    conditions.append((get_bv("local_41") ^ get_bv("local_18")) == 0x4f)
    conditions.append((get_bv("local_3a") ^ get_bv("local_23")) == 3)
    conditions.append((get_bv("local_17") + get_bv("local_22")) == ord('b'))
    conditions.append((get_bv("local_41") + get_bv("local_29")) == 0xc5) # -0x3b
    conditions.append((get_bv("local_2a") + get_bv("local_43")) == 0xc9) # -0x37
    conditions.append((get_bv("local_4c") + get_bv("local_31")) == ord('h'))
    conditions.append(get_bv("local_4c") == get_bv("local_42"))
    conditions.append((get_bv("local_42") ^ get_bv("local_34")) == 4)
    conditions.append((get_bv("local_1e") + get_bv("local_55")) == 0x85) # -0x7b
    conditions.append(get_bv("local_3f") == 0x61)
    conditions.append(get_bv("local_44") == 0x39)
    conditions.append(get_bv("local_4b") == 0x31) # Conflicts with local_23 == local_4b and local_23 == 0x31
    conditions.append(get_bv("local_20") == 0x30) # Conflicting with local_20 == 0xd2
    conditions.append((get_bv("local_24") + get_bv("local_18")) == 0xe9) # -0x17
    conditions.append(get_bv("local_23") == 0x31) # Duplicate
    conditions.append((get_bv("local_1e") + get_bv("local_52")) == 0xbf) # -0x41
    conditions.append((get_bv("local_28") + get_bv("local_3c")) == 0x99) # -0x67
    conditions.append(get_bv("local_27") == 0x32)
    conditions.append((get_bv("local_3d") + get_bv("local_2a")) == 0x97) # -0x69
    conditions.append(get_bv("local_3b") == 0x31) # Duplicate
    conditions.append(get_bv("local_47") == 0x36)
    conditions.append((get_bv("local_52") + get_bv("local_17")) == ord('v'))
    conditions.append(get_bv("local_3a") == 0x32) # Duplicate
    conditions.append((get_bv("local_16") ^ get_bv("local_28")) == 0x4a)
    conditions.append((get_bv("local_29") + get_bv("local_47")) == 0xf0) # -0x10
    conditions.append(get_bv("local_4c") == 0xd8) # Conflicts with local_4c == local_42
    conditions.append((get_bv("local_1b") + get_bv("local_17")) == ord('b'))
    conditions.append((get_bv("local_18") + get_bv("local_3f")) == 0x93) # -0x6d
    conditions.append((get_bv("local_22") ^ get_bv("local_20")) == 2)
    conditions.append(get_bv("local_3a") == 0x32) # Duplicate
    conditions.append((get_bv("local_23") ^ get_bv("local_1a")) == 7)
    conditions.append(get_bv("local_21") == 0x30) # Conflicting with local_21 == 0xe5
    conditions.append(get_bv("local_34") == 0x79) # Conflicting with local_34 == 0x32
    conditions.append(get_bv("local_18") == 0x33) # Conflicting with local_18 == 0x30
    conditions.append((get_bv("local_40") + get_bv("local_24")) == 0xc5) # -0x3b
    conditions.append(get_bv("local_31") == ord('S')) # Conflicting with local_31 == ord('o')
    conditions.append(get_bv("local_46") == 9)
    conditions.append((get_bv("local_55") + get_bv("local_35")) == 0xb4) # -0x4c
    conditions.append((get_bv("local_47") + get_bv("local_22")) == ord('h'))
    conditions.append((get_bv("local_2a") ^ get_bv("local_47")) == 0xfb)
    conditions.append(get_bv("local_1b") == 0x4f)
    conditions.append(get_bv("local_4b") == 0x3e) # Conflicting with local_4b == 0x31
    conditions.append(get_bv("local_26") == 0xec)
    conditions.append(get_bv("local_28") == 0x37)
    conditions.append((get_bv("local_3f") + get_bv("local_1a")) == 0xff) # -1
    conditions.append((get_bv("local_3d") ^ get_bv("local_53")) == 0x28)
    conditions.append(get_bv("local_25") == 0xd1) # Conflicting with local_25 == 0x35
    conditions.append((get_bv("local_1e") ^ get_bv("local_4e")) == 0xe8)
    conditions.append(get_bv("local_26") == 0x65) # Conflicting with local_26 == 0xec
    conditions.append((get_bv("local_50") + get_bv("local_1c")) == 0xfc) # -4
    conditions.append((get_bv("local_3d") + get_bv("local_50")) == ord('d'))
    conditions.append((get_bv("local_33") ^ get_bv("local_1f")) == 2)
    conditions.append(get_bv("local_4c") == 0x36) # Conflicts with local_4c == 0xd8 and local_4c == local_42
    conditions.append(get_bv("local_50") == 0x32) # Duplicate
    conditions.append(get_bv("local_3b") == 0x31) # Duplicate
    conditions.append(get_bv("local_19") == 0x32)
    conditions.append((get_bv("local_51") + get_bv("local_4e")) == 0xdf) # -0x21
    conditions.append(get_bv("local_36") == 0x34)
    conditions.append((get_bv("local_23") ^ get_bv("local_21")) == 0x59)
    conditions.append(get_bv("local_1b") == 0x39) # Conflicting with local_1b == 0x4f
    conditions.append((get_bv("local_49") ^ get_bv("local_2a")) == 0x53)
    conditions.append(get_bv("local_4e") == 0x61)
    conditions.append((get_bv("local_20") ^ get_bv("local_4e")) == 0x54)
    conditions.append((get_bv("local_1a") + get_bv("local_4f")) == ord('j'))
    conditions.append((get_bv("local_44") + get_bv("local_39")) == ord('n'))
    conditions.append(get_bv("local_51") == 0x7b) # Duplicate
    conditions.append(get_bv("local_32") == 0x65)
    conditions.append((get_bv("local_31") + get_bv("local_29")) == 0x96) # -0x6a
    conditions.append(get_bv("local_16") == 0x7d)
    conditions.append((get_bv("local_3a") ^ get_bv("local_2c")) == 0x5d)
    conditions.append(get_bv("local_2d") == 0x62)
    conditions.append((get_bv("local_3d") ^ get_bv("local_40")) == 99)
    conditions.append((get_bv("local_40") ^ get_bv("local_42")) == 0x52)
    conditions.append(get_bv("local_4b") == 0x31) # Duplicate
    conditions.append((get_bv("local_30") + get_bv("local_4f")) == ord('g'))
    conditions.append(get_bv("local_4f") == 0x7b)
    conditions.append(get_bv("local_1d") == 0x93) # Conflicting with local_1d == 0x61
    conditions.append((get_bv("local_4c") ^ get_bv("local_38")) == 3)
    conditions.append(get_bv("local_26") == 199) # 199 = 0xc7. Conflicts with 0xec, 0x65
    conditions.append(get_bv("local_38") == 0x35) # Duplicate
    conditions.append(get_bv("local_16") == 0x7d) # Duplicate
    conditions.append((get_bv("local_22") + get_bv("local_2f")) == ord('G'))
    conditions.append((get_bv("local_19") + get_bv("local_41")) == 0x93) # -0x6d
    conditions.append((get_bv("local_54") ^ get_bv("local_46")) == 0x74)
    conditions.append((get_bv("local_4a") ^ get_bv("local_1b")) == 0x16)
    conditions.append(get_bv("local_23") == 0x31) # Duplicate
    conditions.append((get_bv("local_55") + get_bv("local_16")) == 0xcd) # -0x33
    conditions.append(get_bv("local_19") == 0x32) # Duplicate
    conditions.append(get_bv("local_1f") == 99)
    conditions.append(get_bv("local_4e") == 0x4b) # Conflicting with local_4e == 0x61
    conditions.append((get_bv("local_38") ^ get_bv("local_2d")) == 0x57)
    conditions.append(get_bv("local_1b") == 0x39) # Duplicate
    conditions.append((get_bv("local_34") ^ get_bv("local_29")) == 0x56)
    conditions.append(get_bv("local_44") == 0x96) # Conflicting with local_44 == 0x39
    conditions.append(get_bv("local_42") == 0xab) # Conflicting with local_42 == 0x36
    conditions.append((get_bv("local_1a") + get_bv("local_22")) == 0xaf) # -0x51
    conditions.append(get_bv("local_40") == 0x7f) # Conflicting with local_40 == 0x24
    conditions.append((get_bv("local_32") ^ get_bv("local_4a")) == 0xd1)
    conditions.append(get_bv("local_2d") == 0x62) # Duplicate
    conditions.append((get_bv("local_43") ^ get_bv("local_48")) == 0x5e)
    conditions.append(get_bv("local_4e") == 0x16) # Conflicting with 0x61, 0x4b
    conditions.append((get_bv("local_1f") + get_bv("local_4f")) == 0x97) # -0x69
    conditions.append(get_bv("local_23") == 0x31) # Duplicate
    conditions.append(get_bv("local_28") == 0x37) # Duplicate
    conditions.append((get_bv("local_42") + get_bv("local_50")) == ord('h'))
    conditions.append(get_bv("local_51") == 0x1a) # Conflicting with local_51 == 0x7b
    conditions.append(get_bv("local_17") == 0x30)
    conditions.append((get_bv("local_49") ^ get_bv("local_3d")) == 4)
    conditions.append((get_bv("local_27") + get_bv("local_35")) == 0x96) # -0x6a
    conditions.append(get_bv("local_33") == 0x61)
    conditions.append(get_bv("local_52") == 0x46)
    conditions.append((get_bv("local_4a") + get_bv("local_26")) == 0x97) # -0x69
    conditions.append(get_bv("local_27") == 0x32) # Duplicate
    conditions.append(get_bv("local_3c") == 0x60)
    conditions.append(get_bv("local_4c") == 0x36) # Duplicate
    conditions.append(get_bv("local_3b") == 0x3a) # Conflicting with local_3b == 0x31
    conditions.append((get_bv("local_1e") ^ get_bv("local_2b")) == 0xc)
    conditions.append((get_bv("local_33") ^ get_bv("local_42")) == 0x57)
    conditions.append(get_bv("local_1d") == 0x61) # Duplicate
    conditions.append((get_bv("local_2a") ^ get_bv("local_36")) == 0x51)
    conditions.append(get_bv("local_1e") == 0x35)
    conditions.append(get_bv("local_4c") == 0xa9) # Conflicting with 0xd8, 0x36, local_42
    conditions.append((get_bv("local_27") + get_bv("local_52")) == ord('x'))
    conditions.append(get_bv("local_25") == 0x1f) # Conflicting with 0x35, 0xd1
    conditions.append((get_bv("local_32") + get_bv("local_3e")) == 0x9d) # -99
    conditions.append(get_bv("local_31") == ord('m')) # Conflicting with 'o', 'S'
    conditions.append((get_bv("local_37") ^ get_bv("local_39")) == 6)
    conditions.append(get_bv("local_20") == 0x30) # Duplicate
    conditions.append(get_bv("local_41") == 0xf7) # Conflicting with 0x61
    conditions.append(get_bv("local_23") == 0x31) # Duplicate
    conditions.append((get_bv("local_19") + get_bv("local_28")) == ord('i'))
    conditions.append((get_bv("local_2c") ^ get_bv("local_49")) == 5)
    conditions.append((get_bv("local_4c") ^ get_bv("local_2b")) == 0x85)
    conditions.append(get_bv("local_35") == 100) # Duplicate
    conditions.append(get_bv("local_20") == 0x30) # Duplicate
    conditions.append((get_bv("local_2f") + get_bv("local_1e")) == ord('g'))
    conditions.append(get_bv("local_35") == get_bv("local_48")) # Conflicts with local_48 == 0xbe and local_35 == 100
    conditions.append(get_bv("local_31") == ord('2')) # Conflicting with 'o', 'S', 'm'
    conditions.append(get_bv("local_3e") == 0x9b) # Conflicting with 0xe1, 0x38
    conditions.append(get_bv("local_48") == 100) # Conflicting with local_48 == 0xbe
    conditions.append(get_bv("local_4d") == 0x31)
    conditions.append(get_bv("local_31") == ord('2')) # Duplicate
    conditions.append(get_bv("local_47") == 0xc3) # Conflicting with 0x36
    conditions.append((get_bv("local_2c") + get_bv("local_40")) == 0x97) # -0x69
    conditions.append((get_bv("local_28") + get_bv("local_30")) == ord('j'))
    conditions.append(get_bv("local_35") == 0x32) # Conflicting with local_35 == 100
    conditions.append(get_bv("local_29") == 100)
    conditions.append(get_bv("local_53") == 0x54) # Duplicate
    conditions.append((get_bv("local_32") ^ get_bv("local_23")) == 0x54)
    conditions.append(get_bv("local_22") == 0x32)
    conditions.append(get_bv("local_25") == 0x35) # Duplicate
    conditions.append(get_bv("local_2c") == 0x33) # Duplicate
    conditions.append(get_bv("local_3a") == 0x32) # Duplicate
    conditions.append((get_bv("local_24") + get_bv("local_1a")) == 0x97) # -0x69
    conditions.append(get_bv("local_31") == ord('2')) # Duplicate
    conditions.append(get_bv("local_3f") == 0x61) # Duplicate
    conditions.append((get_bv("local_1e") + get_bv("local_51")) == 0x12)
    conditions.append(get_bv("local_27") == 0x9e) # Conflicting with 0x32
    conditions.append((get_bv("local_3f") ^ get_bv("local_36")) == 0x55)
    conditions.append(get_bv("local_23") == 0x43) # Conflicting with 0x31, local_4b
    conditions.append(get_bv("local_3e") == 0x38) # Duplicate
    conditions.append(get_bv("local_21") == 0xc) # Conflicting with 0xe5, 0x30
    conditions.append(get_bv("local_21") == 0x30) # Duplicate
    conditions.append(get_bv("local_3f") == 0x61) # Duplicate
    conditions.append(get_bv("local_47") == 0x36) # Duplicate
    conditions.append(get_bv("local_53") == 0x54) # Duplicate
    conditions.append((get_bv("local_4d") ^ get_bv("local_3f")) == 0x50)
    conditions.append((get_bv("local_32") + get_bv("local_55")) == 0xa7) # -0x59
    conditions.append((get_bv("local_2e") + get_bv("local_53")) == 0xc7) # -0x39
    conditions.append((get_bv("local_2c") ^ get_bv("local_4f")) == 7)
    conditions.append((get_bv("local_34") + get_bv("local_4a")) == 0xa5) # -0x5b
    conditions.append(get_bv("local_3c") == 0x62) # Conflicting with 0x60
    conditions.append(get_bv("local_3b") == 0x31) # Duplicate
    conditions.append((get_bv("local_41") + get_bv("local_3a")) == ord('#')) # ord('#') = 0x23
    conditions.append((get_bv("local_4f") ^ get_bv("local_32")) == 0x9c)
    conditions.append((get_bv("local_47") ^ get_bv("local_4a")) == 4)
    conditions.append(get_bv("local_2e") == ord('4')) # Duplicate
    conditions.append((get_bv("local_2d") + get_bv("local_36")) == 0x96) # -0x6a
    conditions.append(get_bv("local_1c") == 99) # Duplicate
    conditions.append(get_bv("local_4e") == 100) # Conflicting with 0x61, 0x4b, 0x16
    conditions.append(get_bv("local_47") == 0x36) # Duplicate
    conditions.append(get_bv("local_50") == 0x43) # Conflicting with 0x32
    conditions.append((get_bv("local_3e") ^ get_bv("local_3f")) == 0x59)
    conditions.append(get_bv("local_40") == 100) # Conflicting with 0x24, 0x7f
    conditions.append((get_bv("local_3f") ^ get_bv("local_29")) == 5)
    conditions.append(get_bv("local_20") == 0x30) # Duplicate
    conditions.append(get_bv("local_36") == 0x34) # Duplicate
    conditions.append(get_bv("local_3f") == 0x61) # Duplicate
    conditions.append((get_bv("local_27") + get_bv("local_4d")) == ord('z'))
    conditions.append((get_bv("local_3c") ^ get_bv("local_52")) == 0x24)
    conditions.append(get_bv("local_2a") == 0x65)
    conditions.append(get_bv("local_29") == 0xf) # Conflicting with 100
    conditions.append((get_bv("local_45") ^ get_bv("local_40")) == 0x57)
    conditions.append((get_bv("local_4c") ^ get_bv("local_17")) == 6)
    conditions.append(get_bv("local_3a") == 0x32) # Duplicate
    conditions.append((get_bv("local_43") + get_bv("local_1f")) == 0xd1) # -0x2f
    conditions.append(get_bv("local_35") == 100) # Duplicate
    conditions.append((get_bv("local_1c") + get_bv("local_43")) == 0xc7) # -0x39
    conditions.append((get_bv("local_2a") ^ get_bv("local_35")) == 1)
    conditions.append(get_bv("local_44") == 0xa4) # Conflicting with 0x39, 0x96
    conditions.append((get_bv("local_4d") ^ get_bv("local_4c")) == 7)
    conditions.append(get_bv("local_2d") == 0x62) # Duplicate
    conditions.append((get_bv("local_1d") + get_bv("local_51")) == ord('\n')) # 0x0a
    conditions.append((get_bv("local_40") + get_bv("local_39")) == 0x99) # -0x67
    conditions.append(get_bv("local_49") == 0x7c)
    conditions.append((get_bv("local_16") + get_bv("local_43")) == 0xe1) # -0x1f
    conditions.append(get_bv("local_3a") == 0x32) # Duplicate
    conditions.append(get_bv("local_3e") == 0x38) # Duplicate
    conditions.append((get_bv("local_29") + get_bv("local_43")) == 0xc8) # -0x38
    conditions.append((get_bv("local_4c") + get_bv("local_42")) == ord('l'))
    conditions.append((get_bv("local_18") + get_bv("local_4a")) == 0xe7) # -0x19
    conditions.append(get_bv("local_40") == 100) # Duplicate
    conditions.append((get_bv("local_1c") + get_bv("local_36")) == 0x97) # -0x69
    conditions.append((get_bv("local_39") ^ get_bv("local_2d")) == 0x57)
    conditions.append(get_bv("local_28") == 0x37) # Duplicate
    conditions.append((get_bv("local_48") + get_bv("local_26")) == 0xc9) # -0x37
    conditions.append(get_bv("local_43") == 100) # Conflicting with 0xf1
    conditions.append(get_bv("local_46") == 0x37) # Conflicting with 9
    conditions.append((get_bv("local_1b") ^ get_bv("local_45")) == 10)
    conditions.append((get_bv("local_55") ^ get_bv("local_40")) == 0x34)
    conditions.append((get_bv("local_17") + get_bv("local_24")) == 0x91) # -0x6f
    conditions.append(get_bv("local_27") == 0x32) # Duplicate
    conditions.append((get_bv("local_1c") + get_bv("local_55")) == 0xa8) # -0x58
    conditions.append(get_bv("local_31") == ord('2')) # Duplicate
    conditions.append(get_bv("local_23") == 0x31) # Duplicate
    conditions.append(get_bv("local_25") == 0x35) # Duplicate
    conditions.append(get_bv("local_2b") == 0x39) # Duplicate
    conditions.append((get_bv("local_18") + get_bv("local_32")) == 0x95) # -0x6b
    conditions.append((get_bv("local_3a") + get_bv("local_54")) == ord('u'))
    conditions.append(get_bv("local_25") == 0x35) # Duplicate
    conditions.append((get_bv("local_32") ^ get_bv("local_34")) == 0x51)
    conditions.append((get_bv("local_38") ^ get_bv("local_1c")) == 0x56)
    conditions.append(get_bv("local_3e") == 0x4b) # Conflicting with 0xe1, 0x38, 0x9b
    conditions.append((get_bv("local_36") + get_bv("local_48")) == 0xac) # -0x54
    conditions.append(get_bv("local_2e") == ord('J')) # Conflicting with '4'
    conditions.append(get_bv("local_2e") == ord('4')) # Duplicate
    conditions.append(get_bv("local_34") == 0x73) # Conflicting with 0x32, 0x79
    conditions.append(get_bv("local_4e") == 100) # Duplicate
    conditions.append(get_bv("local_55") == 0x50)
    conditions.append(get_bv("local_3f") == 0x61) # Duplicate
    conditions.append((get_bv("local_17") + get_bv("local_1e")) == ord('e'))
    conditions.append(get_bv("local_21") == 0x30) # Duplicate
    conditions.append((get_bv("local_4e") + get_bv("local_3f")) == 0xcc) # -0x34
    conditions.append((get_bv("local_3b") ^ get_bv("local_47")) == 7)
    conditions.append(get_bv("local_53") == 0x54) # Duplicate
    conditions.append(get_bv("local_27") == 0x32) # Duplicate
    conditions.append(get_bv("local_21") == 0x30) # Duplicate
    conditions.append((get_bv("local_1f") ^ get_bv("local_32")) == 6)
    conditions.append((get_bv("local_36") ^ get_bv("local_33")) == 0x55)
    conditions.append(get_bv("local_34") == 0x32) # Duplicate
    conditions.append((get_bv("local_2d") + get_bv("local_34")) == 0x94) # -0x6c
    conditions.append(get_bv("local_4e") == 100) # Duplicate
    conditions.append(get_bv("local_46") == 0x37) # Duplicate
    conditions.append((get_bv("local_4b") ^ get_bv("local_2a")) == 0x54)
    conditions.append(get_bv("local_46") == 0x37) # Duplicate
    conditions.append((get_bv("local_38") + get_bv("local_37")) == ord('h'))
    conditions.append((get_bv("local_2a") ^ get_bv("local_48")) == 1)
    conditions.append((get_bv("local_1b") + get_bv("local_3d")) == 0xd9) # -0x27
    conditions.append((get_bv("local_44") + get_bv("local_18")) == ord('i'))
    conditions.append(get_bv("local_2c") == 0xa6) # Conflicting with 0x2a, 0x33
    conditions.append((get_bv("local_1f") ^ get_bv("local_3d")) == 0x51)
    conditions.append(get_bv("local_17") == 0x30) # Duplicate
    conditions.append((get_bv("local_1c") + get_bv("local_30")) == 0x96) # -0x6a
    conditions.append((get_bv("local_18") ^ get_bv("local_51")) == 0x4b)
    conditions.append((get_bv("local_30") + get_bv("local_21")) == ord('c'))
    conditions.append((get_bv("local_40") ^ get_bv("local_3b")) == 0x3d)
    conditions.append(get_bv("local_23") == 0xe9) # Conflicting with 0x31, 0x43, local_4b
    conditions.append((get_bv("local_50") ^ get_bv("local_38")) == 7)
    conditions.append(get_bv("local_36") == 0x34) # Duplicate
    conditions.append(get_bv("local_20") == 1) # Conflicting with 0xd2, 0x30
    conditions.append((get_bv("local_46") + get_bv("local_4e")) == 0x9b) # -0x65
    conditions.append(get_bv("local_2c") == 0x33) # Duplicate
    conditions.append((get_bv("local_32") + get_bv("local_3a")) == 0x97) # -0x69
    conditions.append(get_bv("local_2b") == 0x39) # Duplicate
    conditions.append(get_bv("local_3a") == 0x32) # Duplicate
    conditions.append(get_bv("local_26") == 0x65) # Duplicate
    conditions.append((get_bv("local_28") ^ get_bv("local_37")) == 4)
    conditions.append(get_bv("local_37") == 0x33) # Conflicting with 0x76
    conditions.append(get_bv("local_3f") == 0x61) # Duplicate
    conditions.append(get_bv("local_24") == 0x61)
    conditions.append((get_bv("local_36") + get_bv("local_40")) == 0x98) # -0x68
    conditions.append(get_bv("local_3d") == 0x32) # Duplicate
    conditions.append(get_bv("local_46") == 0x37) # Duplicate
    conditions.append(get_bv("local_32") == 0xcb) # Conflicting with 0x65
    conditions.append((get_bv("local_51") + get_bv("local_30")) == 0xae) # -0x52
    conditions.append(get_bv("local_24") == 0x61) # Duplicate
    conditions.append((get_bv("local_4e") ^ get_bv("local_36")) == 0x50)
    conditions.append((get_bv("local_46") + get_bv("local_42")) == ord('m'))
    conditions.append((get_bv("local_37") ^ get_bv("local_3f")) == 199) # 0xc7
    conditions.append((get_bv("local_45") ^ get_bv("local_19")) == 1)
    conditions.append(get_bv("local_49") == 0x36) # Conflicting with 0x7c
    conditions.append(get_bv("local_39") == 1) # Conflicting with 0xb1, 0x35, local_25
    conditions.append((get_bv("local_29") + get_bv("local_1b")) == 0x9d) # -99
    conditions.append((get_bv("local_24") ^ get_bv("local_30")) == 0x52)
    conditions.append(get_bv("local_4f") == 0x34) # Conflicting with 0x7b
    conditions.append(get_bv("local_2f") == 0x32)
    conditions.append(get_bv("local_17") == 0x30) # Duplicate
    conditions.append((get_bv("local_30") ^ get_bv("local_40")) == 0x57)
    conditions.append((get_bv("local_2d") + get_bv("local_50")) == 0x94) # -0x6c
    conditions.append((get_bv("local_4a") + get_bv("local_33")) == 0x93) # -0x6d
    conditions.append(get_bv("local_2a") == 0x99) # Conflicting with 0x65
    conditions.append((get_bv("local_3f") + get_bv("local_3a")) == 0x88) # -0x78
    conditions.append(get_bv("local_27") == get_bv("local_2f")) # Conflicts with local_27 == 0x32, 0x9e and local_2f = 0x32
    conditions.append((get_bv("local_25") ^ get_bv("local_18")) == 5)
    conditions.append(get_bv("local_49") == 0x56) # Conflicting with 0x7c, 0x36
    conditions.append((get_bv("local_29") ^ get_bv("local_39")) == 0x51)
    conditions.append(get_bv("local_28") == 0x37) # Duplicate
    conditions.append((get_bv("local_30") ^ get_bv("local_53")) == 0x67)
    conditions.append((get_bv("local_1f") ^ get_bv("local_45")) == 0x7b)
    conditions.append((get_bv("local_28") ^ get_bv("local_43")) == 0x91)
    conditions.append(get_bv("local_43") == 100) # Duplicate

    # --- Optimization Goal ---
    # Maximize the sum of satisfied conditions.
    # Use If(condition, 1, 0) to convert boolean condition to 1 or 0.
    # Sum() adds these up.
    objective = z3.Sum([z3.If(cond, 1, 0) for cond in conditions])
    solver.maximize(objective)

    # --- Solve and Print Results ---
    print(f"Total number of conditions: {len(conditions)}")
    print("Solving...")

    check_result = solver.check()

    if check_result == z3.sat:
        model = solver.model()
        max_score = model.evaluate(objective)
        print(f"\nMaximum score achievable: {max_score}")

        print("\nVariable values for maximum score:")
        result_bytes = bytearray(64) # Array to hold the result bytes

        # Sort names for consistent output (optional, but nice)
        sorted_vars = sorted(locals_bv.keys(), key=lambda x: int(x.split('_')[1], 16), reverse=True)

        a = ""
        for var_name in sorted_vars:
            var_bv = locals_bv[var_name]
            value = model.evaluate(var_bv, model_completion=True) # Get concrete value
            value_int = value.as_long() # Convert BitVecNumRef to Python int
            print(f"  {var_name}: {hex(value_int)} ({chr(value_int)})")
            a += chr(value_int)

            # Store byte in result array - calculate index based on hex address
            # Index 0 corresponds to local_55, Index 63 to local_16
            index = 0x55 - int(var_name.split('_')[1], 16)
            result_bytes[index] = value_int
        print(a)

        print("\nResulting byte string (local_55 to local_16):")
        try:
            # Try decoding as ASCII, replace errors
            print(result_bytes.decode('ascii', errors='replace'))
        except Exception:
             # Fallback if decoding fails entirely (shouldn't happen with 'replace')
             print("Could not decode as ASCII.")
        print("Hex representation:")
        print(result_bytes.hex())


    elif check_result == z3.unsat:
        print("\nThe constraints are unsatisfiable (this shouldn't happen with Optimize unless constraints conflict badly).")
    else:
        print(f"\nSolver finished with status: {check_result}")

# Run the solver
if __name__ == "__main__":
    solve_constraints()
