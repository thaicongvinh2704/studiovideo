"""Three additional offline voice designs with explicit Northern Vietnamese direction."""
import design_mo_den_local as local

# Reuse the verified local inference/export path; keep the previous auditions intact.
local.OUT=local.ROOT/'projects/mo_den_maya/voice_direction/local_custom_voices_bac_v2'
NORTHERN=(
    'Native Vietnamese man from Hanoi, speaking standard Northern Vietnamese only. '
    'Consistent Hanoi vowel pronunciation and all six Northern Vietnamese lexical tones, '
    'including distinct hoi and nga tones. No Southern or Central Vietnamese accent. '
    'Young adult male, medium speaking pitch, light vocal weight, lively conversational '
    'storytelling with a subtle mischievous smile. Clear natural phrasing and crisp words. '
)
local.DESIGNS=[
    dict(id='04_bac_custom_D',seed=20261104,prompt=NORTHERN+
         'A clear forward youthful timbre with a small nasal edge, nimble witty articulation, '
         'friendly teasing humor and spontaneous curiosity, like chatting with a close friend.'),
    dict(id='05_bac_custom_E',seed=20261105,prompt=NORTHERN+
         'A rounded light clean timbre, buoyant rhythm, relaxed open vowels, a friendly cheeky grin '
         'and playful surprise at questions. Intimate informal delivery, not a solemn narrator.'),
    dict(id='06_bac_custom_F',seed=20261106,prompt=NORTHERN+
         'A slightly textured airy youthful timbre, agile phrasing, understated deadpan wit '
         'and a soft amused smile, light resonance rather than heavy chest resonance.'),
]


if __name__=='__main__':local.main()
