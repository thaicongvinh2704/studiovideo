"""Measure within-scene motion; intentional scene cuts are excluded."""
import sys,math,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from studio.project import load
from studio.animation import evaluate_scene

root=Path(__file__).resolve().parents[1]
p=load(root/'examples'/'explainer_showcase'/'project.json');results=[]
for scene in p['scenes']:
    previous=None;peak=0
    for i in range(1,math.floor(scene['duration']*30)):
        pose=evaluate_scene(scene['objects'],i/30)
        if previous:
            peak=max(peak,max((math.dist(js[k],previous[oid][0][k]) for oid,(js,_) in pose.items() for k in js),default=0))
        previous=pose
    results.append(dict(scene=scene['name'],max_joint_step_design_px=peak))
(root/'outputs'/'explainer_v3'/'motion_measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
