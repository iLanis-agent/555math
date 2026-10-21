// 555 Math engine: astable timing, monostable pulse, and the resistor for a target pulse. Standard chart constants 0.693 and 1.1. Exact integers (ohms, hundredths of a uF, hundredths of a ms), half-up on display only.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _pi(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,7}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _R = "each resistance must be a whole number from 1 to 1000000 Ω";
var _C = "the capacitance must be from 0.01 to 10000 µF with at most two decimal places";
var _T = "the target pulse must be from 0.01 to 360000 ms with at most two decimal places";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  if (v < 0) return "-" + _dec(-v, places);
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _ohm(r) { return r + " Ω"; }
function _uf(c) { return _dec(c, 2) + " µF"; }
function _ms(t100) { return _dec(t100, 2) + " ms"; }

function astableTruth(r1, r2, c) {
  var a = _pi(r1, _R, 1, 1000000), b = _pi(r2, _R, 1, 1000000), k = _p(c, _C, 5, 2, 1, 1000000);
  var th = _hu(693 * (a + b) * k, 1000000);       // hundredths of a ms
  var tl = _hu(693 * b * k, 1000000);
  var n = 693 * (a + 2 * b) * k;                     // period numerator
  var f = _hu(10000000000000, n);                    // hundredths of a Hz
  var duty = _hu((a + b) * 10000, a + 2 * b);        // hundredths of a percent
  return "With " + _ohm(a) + " and " + _ohm(b) + " around a " + _uf(k) + " capacitor, each cycle runs high for " + _ms(th) + " and low for " + _ms(tl) + ". That works out to " + _dec(f, 2) + " Hz at " + _dec(duty, 2) + "% high.";
}
function monoTruth(r, c) {
  var a = _pi(r, _R, 1, 1000000), k = _p(c, _C, 5, 2, 1, 1000000);
  var t = _hu(11 * a * k, 10000);                 // hundredths of a ms
  return "A " + _ohm(a) + " resistor with a " + _uf(k) + " capacitor gives a " + _ms(t) + " pulse (the 1.1·R·C rule).";
}
function partsTruth(t, c) {
  var t100 = _p(t, _T, 6, 2, 1, 36000000), k = _p(c, _C, 5, 2, 1, 1000000);
  var r = _hu(t100 * 1000000, 11 * k);             // hundredths of an ohm
  return "For a " + _ms(t100) + " pulse with a " + _uf(k) + " capacitor, the resistor works out to " + _dec(r, 2) + " Ω.";
}
