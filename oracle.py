# 555 Math oracle: independent Fraction mirror of engine.js. Writes expected.json.
import json
from fractions import Fraction

R = "each resistance must be a whole number from 1 to 1000000 Ω"
C = "the capacitance must be from 0.01 to 10000 µF with at most two decimal places"
T = "the target pulse must be from 0.01 to 360000 ms with at most two decimal places"

def p(t, err, intdigits, lo, hi):
    t = t.strip()
    parts = t.split(".")
    if len(parts) > 2 or not parts[0].isdigit() or len(parts[0]) > intdigits or (len(parts) == 2 and (not parts[1].isdigit() or len(parts[1]) > 2)):
        raise ValueError(err)
    v = int(parts[0]) * 100 + int(parts[1].ljust(2, "0")) if len(parts) == 2 else int(parts[0]) * 100
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def pi(t, err, lo, hi):
    t = t.strip()
    if not t.isdigit() or len(t) > 7:
        raise ValueError(err)
    v = int(t)
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def hu(n, d):
    return (2 * n + d) // (2 * d)

def dec(v):
    if v < 0:
        return "-" + dec(-v)
    s, f = str(v // 100), str(v % 100).rjust(2, "0").rstrip("0")
    return s + "." + f if f else s

def uf(x): return dec(x) + " µF"
def ms(x): return dec(x) + " ms"

def astableTruth(r1, r2, c):
    a = pi(r1, R, 1, 1000000); b = pi(r2, R, 1, 1000000); k = p(c, C, 5, 1, 1000000)
    th = int(hu(Fraction(693) * (a + b) * k, 1000000))
    tl = int(hu(Fraction(693) * b * k, 1000000))
    n = 693 * (a + 2 * b) * k
    f = int(hu(Fraction(10000000000000), n))
    duty = int(hu(Fraction((a + b) * 10000), a + 2 * b))
    return "With " + str(a) + " Ω and " + str(b) + " Ω around a " + uf(k) + " capacitor, each cycle runs high for " + ms(th) + " and low for " + ms(tl) + ". That works out to " + dec(f) + " Hz at " + dec(duty) + "% high."

def monoTruth(r, c):
    a = pi(r, R, 1, 1000000); k = p(c, C, 5, 1, 1000000)
    t = int(hu(Fraction(11) * a * k, 10000))
    return "A " + str(a) + " Ω resistor with a " + uf(k) + " capacitor gives a " + ms(t) + " pulse (the 1.1·R·C rule)."

def partsTruth(t, c):
    t100 = p(t, T, 6, 1, 36000000); k = p(c, C, 5, 1, 1000000)
    r = int(hu(Fraction(t100) * 1000000, 11 * k))
    return "For a " + ms(t100) + " pulse with a " + uf(k) + " capacitor, the resistor works out to " + dec(r) + " Ω."

FNS = {"astableTruth": astableTruth, "monoTruth": monoTruth, "partsTruth": partsTruth}

cases = []
for r1 in ["1", "1000", "10000", "999983", "1000000"]:
    for r2 in ["1", "10000", "1000000"]:
        for c in ["0.01", "100", "10000"]:
            cases.append(("astableTruth", [r1, r2, c]))
for r in ["1", "100000", "1000000"]:
    for c in ["0.01", "10", "10000"]:
        cases.append(("monoTruth", [r, c]))
for t in ["0.01", "1000", "60000", "360000"]:
    for c in ["0.01", "10", "10000"]:
        cases.append(("partsTruth", [t, c]))
errs = ["0", "1000001", "1.5", "x", ""]
out = []
for name, args in cases:
    fn = FNS[name]
    try: exp = fn(*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": name, "args": args, "expected": exp})
for bad in errs:
    for name, args in [("astableTruth", [bad, "10000", "100"]), ("astableTruth", ["10000", bad, "100"]),
                       ("astableTruth", ["10000", "10000", bad]), ("monoTruth", [bad, "10"]),
                       ("monoTruth", ["100000", bad]), ("partsTruth", [bad, "10"]),
                       ("partsTruth", ["1000", bad])]:
        fn = FNS[name]
        try: exp = fn(*args)
        except ValueError as e: exp = "ERR:" + str(e)
        out.append({"fn": name, "args": args, "expected": exp})
with open("expected.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(len(out), "cases written")
