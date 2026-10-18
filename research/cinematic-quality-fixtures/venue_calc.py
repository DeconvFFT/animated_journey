"""Turns the maker's six venue answers (FQ7) into the numbers that are scenarios until then. Round 2, 2026-10-18.
  python3 -I venue_calc.py venue.json          (or with no argument to print the template)
venue.json (fill in what is known; leave a field out to keep the default scenario value shown in the template):
 {"playback": "HDMI",              # DCP | HDMI | USB            -> grading gamma and master
  "screen_width_m": 6.0,           # lit picture width, tape-measured
  "picture_height_m": 3.375,       # lit picture height
  "projector_lumens": 3000,        # spec-sheet ANSI lumens (derate 20 to 30% for lamp age and lens)
  "screen_gain": 1.0,
  "lamp_derate": 0.75,
  "ambient_lux_on_screen": 2.0,    # phone-app reading with the room lights as at the event (uncalibrated sensor: use for ratios)
  "farthest_seat_m": 14.0, "nearest_seat_m": 3.0,
  "native_height_px": 1080}
Prints: peak luminance, grading gamma, signal level hidden by ambient light, seat distances in screen heights, arc-seconds per pixel at the nearest and farthest seat,
type-size floors (x-height, font size), what the MO8 jitter limits subtend, and which of FQ7's scenario defaults were still in use.
Formulas (all arithmetic, labelled M in the note): nits = lumens*derate*gain/(pi*area); ambient luminance = lux/pi (matte, gain 1);
hidden signal fraction f solves (f^gamma)*peak = ambient; x-height floor % = 0.525 * (farthest distance / picture height) (Q10: 0.0035 x distance in picture heights with a 1.5 margin);
arcsec per px = 206265 / (native_height_px * distance_in_picture_heights)."""
import sys, json, math

DEFAULT = dict(playback="HDMI", screen_width_m=6.0, picture_height_m=None, projector_lumens=3000.0, screen_gain=1.0, lamp_derate=0.75,
               ambient_lux_on_screen=2.0, farthest_seat_m=None, nearest_seat_m=None, native_height_px=1080)
GAMMA = {"DCP": 2.6, "HDMI": 2.4, "USB": 2.4, "TV": 2.2}


def calc(a):
    used_default = [k for k in ("playback", "screen_width_m", "projector_lumens", "ambient_lux_on_screen") if k not in a]
    v = {**DEFAULT, **a}
    w = float(v["screen_width_m"]); h = float(v["picture_height_m"] or w * 9 / 16)
    if not a.get("picture_height_m"): used_default.append("picture_height_m (16:9 from width)")
    area = w * h
    nits = v["projector_lumens"] * v["lamp_derate"] * v["screen_gain"] / (math.pi * area)
    gamma = GAMMA.get(str(v["playback"]).upper(), 2.4)
    amb = v["ambient_lux_on_screen"] / math.pi * v["screen_gain"]
    hidden = (amb / nits) ** (1.0 / gamma) if nits > 0 else 1.0
    far = float(v["farthest_seat_m"] or 5.0 * h); near = float(v["nearest_seat_m"] or 1.5 * h)
    if not v["farthest_seat_m"]: used_default.append("farthest_seat_m (5 screen heights)")
    if not v["nearest_seat_m"]: used_default.append("nearest_seat_m (1.5 screen heights)")
    dfar, dnear = far / h, near / h
    def arc_per_px(d): return 206265.0 / (v["native_height_px"] * d)
    out = dict(
        peak_luminance_cd_m2=round(nits, 1), vs_48_cd_m2=round(nits / 48.0, 2), grading_gamma=gamma,
        ambient_cd_m2=round(amb, 3), signal_hidden_below_pct=round(100 * hidden, 1), peak_contrast=round(nits / max(amb, 1e-6)) if amb > 0 else None,
        farthest_in_screen_heights=round(dfar, 2), nearest_in_screen_heights=round(dnear, 2),
        xheight_floor_pct=round(0.525 * dfar, 2), font_size_floor_pct=round(2 * 0.525 * dfar, 2), font_floor_px_at_1080=round(10.8 * 2 * 0.525 * dfar),
        arcsec_per_px_far=round(arc_per_px(dfar), 1), arcsec_per_px_near=round(arc_per_px(dnear), 1),
        one_pixel_is_one_arcmin_at_screen_heights=round(206265.0 / (60 * v["native_height_px"]), 2),
        jitter_arcsec_near={str(j): round(j * arc_per_px(dnear), 1) for j in (0.05, 0.1, 0.3)},
        jitter_arcsec_far={str(j): round(j * arc_per_px(dfar), 1) for j in (0.05, 0.1, 0.3)},
        reading="best-case vernier (alignment) acuity is about 8 arcsec (Wikipedia, citation needed); numbers above it are plausibly visible, numbers well below it are not (UNVERIFIED for moving, noisy pictures)",
        defaults_still_in_use=used_default)
    if v["playback"].upper() == "DCP": out["note"] = "DCP: also check the ST 431-1 tolerance of +/-10.2 cd/m2 around 48 for a Theater (FQ5)"
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps(DEFAULT, indent=1)); sys.exit(0)
    print(json.dumps(calc(json.load(open(sys.argv[1]))), indent=1))
