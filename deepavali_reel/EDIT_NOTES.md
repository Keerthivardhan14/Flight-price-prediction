# Deepavali Reel — Edit Notes (Version A & B)

Output: 1080×1920, 30 fps, H.264 High, AAC 256k stereo 48 kHz, -14 LUFS, true peak < -0.5 dBFS.
Video files are not committed (personal footage + copyrighted song); `build_reel.py` rebuilds them with ffmpeg.

## Music map
Song = concert recording supplied by the user (32 s, ~130 BPM, beat 0.46 s).
Used section: song 14.40 → 31.52 s, placed so **song 17.57 s (drop) = reel 9.30 s**.

| Song time | What happens in the song | Reel time |
|---|---|---|
| 14.4–17.4 | breakdown (bass out) — swells under the aarti flame | 6.1–9.1 |
| 16.8–17.5 | ducked to near-silence; only the fuse sizzle remains | 8.6–9.3 |
| **17.57** | **drop** — fountain eruption | **9.30** |
| 24.38–24.85 | song "stops" for half a beat | 16.11–16.74 → calm aarti shot |
| 25.0 | re-drop | 16.74 → rapid montage |
| 31.45 | last kick | 23.18 → golden burst |

Opening 0–6 s has no song: synthesized temple bell + warm C drone (key-matched to the song) + real room tone.

## Version A timeline
| Reel | Shot | Source file @ source time | Treatment |
|---|---|---|---|
| 0.00–2.20 | Deity close-up | arathi_video @ 23.95 (0.5× slow-mo, 120 fps) | fade from black, slow push-in, warm grade, bell |
| 2.20–4.40 | Mother at shrine | PXL_..1212451272 (4K) @ 0.90 | push-in |
| 4.40–5.20 | Offerings (banana leaf) | ..121924112_food @ 2.00 (0.5×) | push-in, 2nd bell |
| 5.20–8.40 | Mother performs aarti → flame | arathi_video @ 13.60 (0.5×) | push into flame, room fades to black leaving flame, rumble + riser |
| 8.40–9.30 | **Real fuse ember** in darkness | ..144010420 @ 13.45 | heavy crush, glow, push-in, ignition tick, near-silence |
| 9.30–11.17 | **Fountain eruption (drop)** | ..144010420 @ 22.50 | flash, zoom punch, bass impact, crackle, glow |
| 11.17–12.55 | Tall fountain | ..144010420 @ 27.55 | light flash on kick |
| 12.55–14.18 | Mother raising sparkler | ..145526227 @ 7.60 | warm grade, glow |
| 14.18–16.11 | Mother laughing | ..145526227 @ 16.90 | — |
| 16.11–16.74 | Calm: aarti plate with lamps | arathi_video @ 22.78 (0.5×) | on the song's stop |
| 16.74–18.08 | Rapid montage ×3 (cracker / sparks / cracker) | ground_crackers @ 7.35, ..145526227 @ 13.40, ground_crackers @ 9.30 | cuts on kicks, flashes, motion blur |
| 18.08–19.48 | Green aerial burst | ..1446086882 @ 13.61 | deep blacks, glow |
| 19.48–20.62 | White starburst | ..1446086882 @ 7.89 | flash on peak (19.99) |
| 20.62–21.56 | Terrace fountain ignites | ..1446086882 @ 20.46 | flash on kick |
| 21.56–22.68 | Fountains | ..144010420 @ 25.00 | flash on kick |
| 22.68–24.30 | **Golden burst — final hit** | ..1446086882 @ 3.65 | burst lands on last kick 23.18, impact, decay to black |

## Version B (director's cut) — differences
- 0.0–0.5 s cold-open teaser of the golden burst + impact, 0.3 s black, then bell (hooks viewers in the first second; deity shot shortened so all later timings stay identical).
- Subtle film grain over the whole reel.
- Ending: golden burst then dissolves back to the aarti flame with a soft bell (24.77 s) — "the calm is the setup, the flame is the connection".

## Sound design layers
Song (enveloped), synthesized bell / C drone / sub rumble / noise riser / ignition tick / sub impacts (9.30, 16.74, 19.99, 23.18), plus real audio: room tone (..121027741), fuse sizzle, fountain roar, sparkler, crackers, aerial bursts. Bus: gentle compression + limiter, static gain to -14 LUFS.

## Limitations / manual finishing
- **Copyright:** the song is a fan recording of a commercial track. Instagram may mute or restrict the reel. Safer: upload with the in-app song, or ask for a no-music version (easy to export).
- The arathi and 25-sec pooja clips contain music added before upload, so their audio is not used.
- Aerial bursts were shot small/far; they're digitally zoomed (1.15–1.4×) from 1080p, so slightly soft.
- No editable NLE project (ffmpeg pipeline); the script is the timeline — change times/zoom there and re-run.
