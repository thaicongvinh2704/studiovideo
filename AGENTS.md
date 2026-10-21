# Mandatory character standard

## Current production direction: Mỏ Đen

The user has selected Mỏ Đen, an externally prepared cartoon cat, as the main recurring character instead of the human presenter. Read `assets/characters/mo_den/README.md` and `manifest.json` before planning character assets. The user will supply individual images and expressions from outside Studio. Accept those supplied assets regardless of their external creation method; the earlier no-image-generation constraint does not prohibit importing images the user deliberately supplies. Do not generate replacements or redesign Mỏ Đen without a request.

Preserve supplied originals, index reusable expressions/poses, check the library before requesting missing assets, and make requests specific to the script. Use vector drawings for arrows, routes, highlights and simple props. The initial screenshot is identity reference only. The named 24-image pack is now complete: all 24 usable static PNGs are indexed in `assets/characters/mo_den/manifest.json`. IDs 03, 18 and 21 were replaced with user-supplied complete PNGs; the corrupted ZIP originals remain archived. Always use exact indexed paths. All usable originals were preserved byte-for-byte. Image 03 leans left more than neutral; inspect placement when swapping. Native Qt compositing was checked; this audit did not implement the dedicated cat picker or cat export-QC integration.

The human-specific standards below remain applicable if a human illustration is explicitly requested; do not force human fingers, anatomy, or human QC metadata onto the cat. Cat identity/layout/transparency checks and any needed importer integration must be implemented honestly when actual assets arrive; do not label the cat as an object to bypass current character export checks.

## Selected recurring voice: Mỏ Đen

Maya production override (latest user selection, 21/10/2026): the user selected
`projects/mo_den_maya/voice_direction/local_custom_voices_nam_v3/08_nam_custom_H_1_25x.wav`
and explicitly authorized full Maya narration with it. Use the fixed H identity
in `projects/mo_den_maya/voice_direction/selected_voice_H.json`, its preserved
native generated reference and VoxCPM2 local for this production. Keep Northern
Vietnamese and apply 1.25x once; do not regenerate a fresh designed speaker for
each segment. Preserve old B files. The legacy Studio UI default below does not
override this Maya selection. New generated narration still needs listening QC.

Legacy Studio UI default (superseded by custom H for Maya): `voices/demos/vietnamese_ab/B_giong_ke_tieng_viet.wav` previously superseded the short variant-04 audition. Use `voices/mo_den_EFp49inlLuQ_04.voice.json` (UI label: `Mỏ Đen · giọng Bắc · bản B`) as the default recurring narration voice. Preserve the speaker/reference from variant 04, its fixed +0.8-semitone timbre and gentle EQ, and B's slower baseline pacing saved in `postprocess`. For directed semantic clips, use `delivery.intent_settings` for modest speed/gain changes and place the prescribed pauses on the timeline according to meaning. Do not loop the demo's eight beats onto unrelated scripts or pretend that saving a profile automatically directs emotions in arbitrary text. Preserve the chosen B WAV and encoded voice; do not silently replace them with earlier voices or presets. The speaker's identity is unverified. New narration still needs pronunciation and timing review; the user's selection does not batch-pass listening QC.

## Vietnamese narration standard

Before narration work, read `VIETNAMESE_NARRATION_STANDARD.md`. Output narration and demo scripts must be Vietnamese; the user confirmed the selected reference is Northern Vietnamese (Bắc). Preserve that region and speaker across segments. Keep original scripts and an explicit, context-bound pronunciation edit ledger. Natural semantic phrasing and tone accuracy take priority over expressiveness; do not add emotional pitch bends. Check model capabilities and actual listening separately; never mark pronunciation, region, or reference cleanliness passed from signal metrics alone.

## Historical human illustration standard

The current source drawing desk has editable Bezier nodes, pressure strokes, reference tabs, construction guides, shared-node bindings, group bindings, a draft template library and a JSON command API. Read `DRAWING_DESK_GUIDE.md` before using these. Use shared construction where useful, render and inspect changes; do not infer visual quality from constraints or tests. The workbench exercise contains objects only and is not a character master.

The user selected the THREE images in `assets/styles/explainer_reference_v1/` as the required visual direction. BOTH `net-moc-study-01` and `reference-person-study-02` were rejected. Study-02's aesthetic QC was a false positive: disconnected construction, mismatched proportions and poor facial/body harmony. Object illustrations were accepted; do not redesign them to solve a character problem.

There is currently NO accepted character master. The historical study-02 receipt is revoked, including copies embedded in old projects. Never use passing software tests or completed checkboxes to claim that a character is aesthetically successful. Do not recycle this rejected person with minor coordinate changes or a new identity string. Build a coherent whole-body construction and model sheet before further finished-character work; the present coordinate-by-coordinate method has not met the user's standard.

Before creating, changing, importing or delivering any illustrated person:

1. Read `CHARACTER_STANDARD.md` and the reference manifest. Open all three actual reference images with an image-viewing tool. Do not rely on a written recollection of the style.
2. Use drawn vector paths, not an image generation model, image-to-vector tracing of generated art, emoji, stick figures, or an unreviewed legacy presenter. People remain static unless the user explicitly changes this requirement.
3. Reuse a reviewed model when possible. For a new person/pose, tag the layer `role=character`, provide the semantic parts and landmarks, and generate the character QC packet. Do not describe a person as an object to evade QC.
4. Open and inspect the current full figure, face, BOTH hands, the small-size preview, and comparison against the references. Record concrete findings for EACH rubric item. Automated geometry checks or passing code tests do not constitute visual approval. Never batch-mark rubric items as passed without looking at the current renders.
5. Fix EVERY critical visual defect before recording internal QC. A visible hand must have a palm, thumb and readable fingers, or a clearly drawn appropriate grip. A rounded arm stump is a failure. Natural shoulder/elbow/wrist connections, finished facial features and clothing edges are mandatory.
6. QC is tied to the current path data, rendered evidence and reference version. Any edit to the artwork invalidates the old review. Re-run QC; do not copy an old receipt onto edited geometry.
7. `scene_layers` and final export must reject missing, failed, stale, or incomplete character QC. Draft save and QC preview remain available for repairs. `allow_draft` must not bypass the character QC gate on final export.
8. Deliver the actual current preview and an honest status. Internal QC does not mean the user approved a new character design. Never claim every aesthetic defect can be detected automatically or guarantee that a checklist alone makes an illustration beautiful.

Do not require the user to repeat these standards or approve routine internal QC. The user already authorized the workflow. If a reference is unavailable, retrieve the preserved project copy; do not silently invent a replacement style.
