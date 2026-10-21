# 555 Math

555 timer arithmetic. With 10000 Ω and 10000 Ω around a 100 µF capacitor, each cycle runs high for 1386 ms and low for 693 ms. That works out to 0.48 Hz at 66.67% high.

## What it computes

- **The astable truth** - high time, low time, frequency and duty for a free-running pair of resistors (1 to 1000000 Ω each) and a capacitor (0.01 to 10000 µF), from the standard 0.693 chart constant.
- **The monostable truth** - the pulse length from one resistor and one capacitor, from the 1.1·R·C rule.
- **The parts truth** - backwards: the resistor that gives a target pulse (0.01 to 360000 ms) with the capacitor at hand.

## Boundary

Arithmetic only, with the standard chart constants 0.693 and 1.1. The resistances and capacitances are the owner's own entries, every component and chip treated as ideal. It has not seen any circuit and does not know the tolerances, the leakage, the supply or the chip variant, and it gives no verdict that a timer circuit is adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on ohms, hundredths of a µF and hundredths of a ms, half-up on display).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/555math/
Repo: https://github.com/iLanis-agent/555math
