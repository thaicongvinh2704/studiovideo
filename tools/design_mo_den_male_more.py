"""Four additional male Northern Vietnamese voice designs; no presets/references."""
import design_mo_den_local as local

local.OUT=local.ROOT/'projects/mo_den_maya/voice_direction/local_custom_voices_nam_v3'
NORTH=('A native Vietnamese man from Hanoi speaking Vietnamese in a consistent standard '
       'Northern accent, with clear Northern vowels and six distinct Vietnamese lexical tones. '
       'Natural adult mid-range pitch. ')
local.DESIGNS=[
    dict(id='07_nam_custom_G',seed=715903,prompt=NORTH+
         'A youthful male voice in his early twenties, lean and bright, dry close conversational '
         'sound, clipped agile consonants, casually cheeky and energetic like a witty young friend. '
         'Quick relaxed phrasing with an amused smile, no heavy chest resonance.'),
    dict(id='08_nam_custom_H',seed=284617,prompt=NORTH+
         'A male voice around thirty with a distinctive soft husky edge, slightly breathy texture '
         'and light resonance. Easygoing conversational rhythm, understated teasing humor and '
         'friendly curiosity. Spoken intimacy, never a solemn announcement or dramatic narration.'),
    dict(id='09_nam_custom_I',seed=963052,prompt=NORTH+
         'A youthful quirky male character voice, narrow focused nasal resonance and a slightly '
         'reedy texture, an impish grin, lively rhythmic articulation, mischievous quick questions. '
         'An expressive adult voice with springy conversational phrasing, not a child or falsetto.'),
    dict(id='10_nam_custom_J',seed=438279,prompt=NORTH+
         'A clean open resonant male voice in his mid twenties, smooth light tenor with clear '
         'ringing vowels and almost no rasp, friendly comic confidence, animated curious questions '
         'and an effortless smiling delivery. Relaxed throat, medium pitch, no booming low voice.'),
]


if __name__=='__main__':local.main()
