#!/usr/bin/env python3
"""Deepavali reel builder. Usage: build.py A|B"""
import subprocess, sys, os, json, math

VER = sys.argv[1]
U = os.environ.get("REEL_SRC", "./footage/")  # folder with the uploaded clips
W = os.path.dirname(os.path.abspath(__file__)) + f"/work{VER}/"
os.makedirs(W, exist_ok=True)
SONG = U + "b808c81e-The_Weeknd_in_HONG_KONG_omfg_how_to_recover_from_this_night__theweeknd__hongkong.mp3"
F = {
    "aarti": U + "17bc14be-arathi_video_.mp4",
    "shrine4k": U + "61d6b995-PXL_20261108_1212451272.mp4",
    "pooja25": U + "c2f42c13-PXL_20261108_121141252_25sec.mp4",
    "pooja7": U + "6e4ae1fd-PXL_20261108_121027741_7sec.mp4",
    "food": U + "7f3563fc-PXL_20261108_121924112_food_7sec.mp4",
    "fountain": U + "4ae03d13-PXL_20261108_144010420_part2_44.mp4",
    "sparkler": U + "4b72ae01-PXL_20261108_145526227_part2_66.mp4",
    "crackers": U + "72f2698a-ground_crackers.mp4",
    "aerial": U + "ed97a00a-PXL_20261108_1446086882.mp4",
}
OFF = 8.27          # reel_time = song_time - OFF   (song drop 17.57 -> reel 9.30)
DROP = 9.30

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)); print(r.stderr[-3000:]); sys.exit(1)

# ---------------------------------------------------------------- grades
WARM = ("eq=contrast=1.05:saturation=1.10:gamma=0.96,"
        "colorbalance=rs=0.04:bs=-0.07:rm=0.05:gm=0.01:bm=-0.06:rh=0.03:bh=-0.06,"
        "curves=all='0/0.015 0.25/0.21 0.75/0.75 1/0.93',vignette=angle=PI/4.5")
FIRE = ("curves=all='0/0 0.16/0.0 0.40/0.20 0.70/0.62 1/1',"
        "eq=saturation=1.35:contrast=1.04,"
        "colorbalance=rs=-0.02:bs=0.03:rm=0.05:bm=-0.05:rh=0.06:gh=0.02:bh=-0.07,vignette=angle=PI/4")
FIRE_SOFT = ("curves=all='0/0 0.10/0.0 0.40/0.28 0.75/0.70 1/0.98',"
             "eq=saturation=1.25:contrast=1.03,"
             "colorbalance=rm=0.05:bm=-0.05:rh=0.05:bh=-0.06,vignette=angle=PI/4")
GLOW = "format=gbrp,split[g0][g1];[g1]curves=all='0/0 0.6/0 1/1',gblur=sigma=28[g2];[g0][g2]blend=all_mode=screen:all_opacity={op}"

def seg(name, src, ss, dur, speed=1.0, z0=1.0, z1=1.0, cx=0.5, cy=0.5,
        grade=WARM, glow=0.0, punch=0.0, extra="", fadein=0.0, fadeout=0.0, blur=False):
    """Render one shot to 1080x1920@30 with push-in (z0->z1, eased), optional zoom punch."""
    D = dur
    srcdur = dur * speed + 0.2
    tt = "(in/30)"
    ease = f"(0.5-0.5*cos(PI*min({tt}/{D},1)))"
    z = f"(({z0})+(({z1})-({z0}))*{ease})*(1+{punch}*exp(-{tt}/0.11))"
    # 2x supersampled zoompan: crop window anchored at (cx,cy), sub-pixel smooth at output size
    vf = [f"setpts=(PTS-STARTPTS)/{speed}", "fps=30",
          "scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840",
          f"zoompan=z='{z}':x='(iw-iw/zoom)*{cx}':y='(ih-ih/zoom)*{cy}':d=1:s=1080x1920:fps=30",
          "setpts=N/30/TB", grade]
    if extra: vf.append(extra)
    if blur: vf.append("tmix=frames=3:weights='1 2 1'")
    if fadein: vf.append(f"fade=in:st=0:d={fadein}")
    if fadeout: vf.append(f"fade=out:st={D-fadeout}:d={fadeout}")
    chain = ",".join(vf)
    if glow:
        chain += "," + GLOW.format(op=glow)
    chain = f"[0:v]{chain},trim=duration={D},setsar=1,format=yuv420p[v]"
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(ss), "-t", str(srcdur), "-i", F[src],
         "-filter_complex", chain, "-map", "[v]", "-an", "-r", "30",
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", W + name + ".mp4"])
    return dict(name=name, src=src, ss=ss, dur=D, speed=speed)

# ---------------------------------------------------------------- timeline
# Darken-to-flame: gamma crush leaves only the brightest flame pixels alive.
def to_flame(a, b):
    p = f"clip((t-{a})/{b-a},0,1)"
    return f"eq=gamma='1-0.88*{p}':brightness='-0.12*{p}':contrast='1+0.9*{p}':eval=frame"

S = []
if VER == "B":
    # cold-open teaser: half a second of the finale, then black
    S.append(seg("b00_tease", "aerial", 4.20, 0.50, z0=1.25, z1=1.18, cx=0.5, cy=0.25, grade=FIRE, glow=0.5, punch=0.1))
    S.append(seg("b01_black", "aerial", 1.0, 0.30, grade="eq=brightness=-1"))
    S.append(seg("s01_deity", "aarti", 24.05, 1.40, speed=0.5, z0=1.04, z1=1.12, cx=0.55, cy=0.35, fadein=0.35))
else:
    S.append(seg("s01_deity", "aarti", 23.95, 2.20, speed=0.5, z0=1.04, z1=1.16, cx=0.55, cy=0.35, fadein=0.5))
S += [
    seg("s02_mother", "shrine4k", 0.90, 2.20, z0=1.0, z1=1.10, cx=0.35, cy=0.45),
    seg("s03_offer", "food", 2.00, 0.80, speed=0.5, z0=1.05, z1=1.12, cx=0.5, cy=0.5),
    seg("s05_flame", "aarti", 13.60, 3.20, speed=0.5, z0=1.0, z1=1.45, cx=0.38, cy=0.78,
        extra=to_flame(1.85, 2.95), fadeout=0.25),
    seg("s06_fuse", "fountain", 13.45, 0.90, z0=1.35, z1=1.65, cx=0.45, cy=0.52, grade=FIRE,
        extra="eq=gamma=0.55:brightness=-0.10", glow=0.6, fadein=0.30),
    # ---- DROP 9.30 (song 17.57)
    seg("s07_fountain", "fountain", 22.50, 1.87, z0=1.0, z1=1.06, cx=0.5, cy=0.4, grade=FIRE, glow=0.45, punch=0.14),
    seg("s08_fountain2", "fountain", 27.55, 1.38, z0=1.08, z1=1.0, cx=0.5, cy=0.4, grade=FIRE, glow=0.4, punch=0.06),
    # ---- human moment 12.55
    seg("s09_mom_raise", "sparkler", 7.60, 1.63, z0=1.05, z1=1.12, cx=0.6, cy=0.3, grade=WARM + ",eq=saturation=1.05", glow=0.3),
    seg("s10_mom_laugh", "sparkler", 16.90, 1.93, z0=1.10, z1=1.18, cx=0.62, cy=0.35, grade=WARM, glow=0.3),
    # ---- song stop 16.11-16.74 -> calm flash
    seg("s11_calm", "aarti", 22.78, 0.63, speed=0.5, z0=1.15, z1=1.2, cx=0.4, cy=0.2),
    # ---- rapid montage 16.74 (re-drop)
    seg("s12_crack1", "crackers", 7.35, 0.45, z0=1.15, z1=1.05, cx=0.5, cy=0.45, grade=FIRE_SOFT, glow=0.5, punch=0.08, blur=True),
    seg("s13_spark", "sparkler", 13.40, 0.41, z0=1.2, z1=1.3, cx=0.6, cy=0.7, grade=FIRE_SOFT, glow=0.5, blur=True),
    seg("s14_crack2", "crackers", 9.30, 0.48, z0=1.1, z1=1.0, cx=0.5, cy=0.4, grade=FIRE_SOFT, glow=0.5, punch=0.08, blur=True),
    # ---- grand finale 18.08
    seg("s15_green", "aerial", 13.61, 1.40, z0=1.30, z1=1.40, cx=0.55, cy=0.10, grade=FIRE, glow=0.55),
    seg("s16_star", "aerial", 7.89, 1.14, z0=1.15, z1=1.25, cx=0.5, cy=0.35, grade=FIRE, glow=0.5),
    seg("s17_terrace", "aerial", 20.46, 0.94, z0=1.0, z1=1.08, cx=0.3, cy=0.55, grade=FIRE, glow=0.5, punch=0.06),
    seg("s18_fount", "fountain", 25.00, 1.12, z0=1.15, z1=1.05, cx=0.5, cy=0.35, grade=FIRE, glow=0.45, punch=0.05),
]
if VER == "B":
    S.append(seg("s19_gold", "aerial", 3.65, 1.20, z0=1.30, z1=1.18, cx=0.5, cy=0.22, grade=FIRE, glow=0.6, fadeout=0.35))
    S.append(seg("s20_diya", "aarti", 14.55, 0.90, speed=0.5, z0=1.7, z1=1.8, cx=0.36, cy=0.80,
                 extra="eq=gamma=0.6:brightness=-0.08", fadein=0.3, fadeout=0.45))
else:
    S.append(seg("s19_gold", "aerial", 3.65, 2.32, z0=1.30, z1=1.12, cx=0.5, cy=0.22, grade=FIRE, glow=0.6, fadeout=0.12))

# ---------------------------------------------------------------- concat + flashes
with open(W + "list.txt", "w") as f:
    for s in S: f.write(f"file '{W}{s['name']}.mp4'\n")
t = 0; cuts = []
for s in S: cuts.append((s["name"], round(t, 3))); t += s["dur"]
TOTAL = round(t, 3)
json.dump(dict(segments=S, cuts=cuts, total=TOTAL), open(W + "timeline.json", "w"), indent=1)
print("total", TOTAL); [print(f"{c[1]:6.2f}  {c[0]}") for c in cuts]

sh = 0.8 if VER == "B" else 0.0   # B's cold open shifts nothing: deity is 0.8s shorter
flashes = [(DROP, .35), (11.17, .18), (16.74, .3), (17.19, .22), (17.60, .25), (18.08, .25),
           (19.99, .35), (21.16, .2), (22.26, .3), (23.18, .5)]
if VER == "B": flashes = [(0.0, .5)] + flashes
fx = "+".join(f"{a}*exp(-(t-{T})/0.07)*gte(t,{T})" for T, a in flashes)
vpost = f"eq=brightness='{fx}':eval=frame"
if VER == "B": vpost += ",noise=c0s=7:c0f=t+u,eq=contrast=1.02"
T0, T1 = 23.30, TOTAL                       # slogan in after the final hit, out with the fade
al = f"if(lt(t,{T0}),0,if(lt(t,{T0}+0.5),(t-{T0})/0.5,if(gt(t,{T1}-0.12),max(0,({T1}-t)/0.12),1)))"
al2 = al.replace(f"{T0}", f"{T0+0.25}")
FS = "/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf"
FL = "/usr/share/fonts/opentype/inter/Inter-Light.otf"
txt = (f"drawtext=fontfile={FL}:text='D I W A L I    2 0 2 6':fontsize=38:fontcolor=0xF6E7C1:"
       f"x=(w-text_w)/2:y=h*0.70:alpha='{al}',"
       f"drawtext=fontfile={FS}:text='Done & Dusted':fontsize=118:fontcolor=0xF9D98B:"
       f"x=(w-text_w)/2:y=h*0.70+62:alpha='{al2}'")
slog = (f"color=c=black@0.0:s=1080x1920:r=30:d={TOTAL},format=rgba,{txt},split[t0][t1];"
        "[t1]gblur=sigma=14,colorchannelmixer=rr=1.2:gg=0.85:bb=0.35[tg]")
vfc = (f"[0:v]{vpost}[b];{slog};[b][tg]overlay=format=auto[b2];[b2][t0]overlay=format=auto,format=yuv420p[v]"
       if VER == "A" else f"[0:v]{vpost},format=yuv420p[v]")
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", W + "list.txt",
     "-filter_complex", vfc, "-map", "[v]", "-c:v", "libx264", "-crf", "14", "-preset", "fast", W + "video.mp4"])

# ---------------------------------------------------------------- audio
A = W
SR = 48000
def synth(name, expr, dur):
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
         f"aevalsrc='{expr}':s={SR}:d={dur}", "-ac", "2", A + name + ".wav"])

# temple bell on C (inharmonic partials, long decay)
bell = "+".join(f"{a}*sin(2*PI*{f}*t)*exp(-t/{d})" for f, a, d in
                [(130.8, .25, 4), (261.6, .35, 3.2), (313.9, .18, 2.2), (392.4, .14, 2.0),
                 (523.3, .22, 1.8), (523.3*1.003, .1, 1.8), (716.8, .1, 1.1), (1046.5, .06, .7), (1438, .04, .4)])
synth("bell", f"0.5*({bell})", 5)
# warm pad: C2/G2/C3 drone with slow breathing
pad = "(0.30*sin(2*PI*65.41*t)+0.22*sin(2*PI*98.0*t)+0.16*sin(2*PI*130.81*t)+0.06*sin(2*PI*196*t))*(0.8+0.2*sin(2*PI*0.25*t))"
synth("pad", pad, 9)
# sub rumble for the build
synth("rumble", "0.5*sin(2*PI*(38+6*t/3)*t)*(0.7+0.3*sin(2*PI*7*t))", 4)
# cinematic impact: pitch-dropping sub + short noise crack
synth("impact", "0.9*sin(2*PI*(35*t+45/6*(1-exp(-6*t))))*exp(-t/0.7)+0.35*(random(0)*2-1)*exp(-t/0.04)", 2.5)
# tiny ignition tick
synth("tick", "0.6*(random(1)*2-1)*exp(-t/0.012)", 0.2)
# riser: filtered noise, exponential swell
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"anoisesrc=c=white:r={SR}:d=1.6:a=0.5",
     "-af", "highpass=f=2500,lowpass=f=9000,volume='pow(t/1.6,3)':eval=frame", "-ac", "2", A + "riser.wav"])

# natural sound bed, per section, from the real clips (aarti clip has added music: not used)
nat = [  # (src, ss, reel_start, dur, gain)
    ("pooja7", 0.0, 0.0, 7.0, 1.8),        # quiet room tone during pooja (other pooja clips carry added music)
    ("fountain", 13.45, 8.40, 0.45, 1.6),   # fuse sizzle (stops before a loud bang at +0.5 s)
    ("fountain", 22.50, 9.30, 3.25, 0.18),  # fountain roar
    ("sparkler", 7.60, 12.55, 3.56, 0.4),   # sparkler + family
    ("crackers", 7.35, 16.74, 1.34, 0.4),
    ("aerial", 13.61, 18.08, 6.92, 0.4),    # finale fireworks natural booms
]
sec = []
for i, (src, ss, st, d, g) in enumerate(nat):
    o = A + f"nat{i}.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(ss), "-t", str(d), "-i", F[src], "-vn",
         "-af", f"aresample={SR},afade=in:d=0.08,afade=out:st={d-0.15}:d=0.15,volume={g}", "-ac", "2", o])
    sec.append((o, (0.8 if VER == "B" and st == 0 else st)))

songA = A + "song.wav"
s_in = 14.40                                   # breakdown starts under the flame
# The recording stops at 31.52 s (reel 23.25). To keep the beat running to the last frame,
# play up to the downbeat at 31.45 and then repeat the previous bar (29.60 -> 31.45, 4 beats of 0.4627 s).
SPLICE, LOOP0 = 31.45, 29.60
need = TOTAL - (SPLICE - OFF) + 0.1
run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(s_in), "-t", str(SPLICE - s_in + 0.01), "-i", SONG,
     "-ss", str(LOOP0), "-t", str(need), "-i", SONG, "-filter_complex",
     (f"[0:a]aresample={SR},"
      # reel-relative envelope (t=0 is reel 6.13): swell in, near-silence before the drop, full after
      # gradual: steady crescendo under the flame (no silent gap), then ease up to full ~1.3 s after the drop
      "volume='if(lt(t,3.17), 0.05+0.47*pow(t/3.17,1.6), min(1, 0.52+0.48*pow(min((t-3.17)/1.3,1),0.8)))':eval=frame[s1];"
      f"[1:a]aresample={SR}[s2];[s1][s2]acrossfade=d=0.01:c1=tri:c2=tri[o]"),
     "-map", "[o]", "-ac", "2", songA])

# assemble: [file, reel_start, gain]
P0 = 0.8 if VER == "B" else 0.0
mix = [(songA, s_in - OFF, 1.35), (A + "pad.wav", P0, 0.0), (A + "bell.wav", P0 + 0.15, 0.55),
       (A + "bell.wav", 4.40, 0.30), (A + "rumble.wav", 5.4, 0.0), (A + "riser.wav", 7.1, 0.35),
       (A + "tick.wav", 8.42, 0.8), (A + "impact.wav", DROP, 0.4), (A + "impact.wav", 16.74, 0.45),
       (A + "impact.wav", 19.99, 0.4), (A + "impact.wav", 23.18, 0.85), (A + "bell.wav", 23.50, 0.35)] + [(o, st, 1.0) for o, st in sec]
if VER == "B":
    mix = [(f, st + 0.0, g) for f, st, g in mix]  # timeline identical after 0.8s; tease audio added below
    mix += [(A + "impact.wav", 0.0, 0.8), (A + "bell.wav", 23.95, 0.45)]
# pad and rumble get their own envelopes
run(["ffmpeg", "-y", "-loglevel", "error", "-i", A + "pad.wav", "-af",
     "lowpass=f=900,volume='0.22*min(t/1.5,1)*if(lt(t,7.4),1,max(0,1-(t-7.4)/0.9))':eval=frame", A + "pad_e.wav"])
run(["ffmpeg", "-y", "-loglevel", "error", "-i", A + "rumble.wav", "-af",
     "lowpass=f=120,volume='0.5*min(t/2.2,1)*if(lt(t,3.1),1,max(0,1-(t-3.1)/0.4))':eval=frame", A + "rumble_e.wav"])
mix = [((A + "pad_e.wav") if f.endswith("pad.wav") else (A + "rumble_e.wav") if f.endswith("rumble.wav") else f,
        st, (1.0 if f.endswith(("pad.wav", "rumble.wav")) else g)) for f, st, g in mix]
if VER == "B":  # everything except tease starts after cold open, but timeline was built so reel times match A
    pass

ins, fl = [], []
for i, (f, st, g) in enumerate(mix):
    ins += ["-i", f]
    fl.append(f"[{i}:a]volume={g},adelay={int(st*1000)}:all=1[a{i}]")
fl.append("".join(f"[a{i}]" for i in range(len(mix))) +
          f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{TOTAL},"
          "highpass=f=28,acompressor=threshold=0.25:ratio=2.5:attack=8:release=180,"
          f"alimiter=limit=0.89:level=false,afade=out:st={TOTAL-0.06}:d=0.06[out]")
run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fl), "-map", "[out]",
     "-ar", str(SR), A + "mix.wav"])

# loudness to ~-14 LUFS (static gain, keeps the drop dynamics)
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", A + "mix.wav", "-af", "ebur128", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
I = float(r.rsplit("I:", 1)[1].split("LUFS")[0])
gain = -14.0 - I
run(["ffmpeg", "-y", "-loglevel", "error", "-i", A + "mix.wav", "-af",
     f"volume={gain}dB,alimiter=limit=0.89:level=false", A + "mix_norm.wav"])
print(f"loudness {I:.1f} -> gain {gain:+.1f} dB")

out = os.path.dirname(os.path.abspath(__file__)) + f"/Deepavali_Reel_Version_{VER}.mp4"
run(["ffmpeg", "-y", "-loglevel", "error", "-i", W + "video.mp4", "-i", A + "mix_norm.wav",
     "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.1", "-crf", "18", "-maxrate", "10M", "-bufsize", "20M",
     "-preset", "slow", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
     "-movflags", "+faststart", "-shortest", out])
print("wrote", out)
