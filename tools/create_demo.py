import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from studio.demo import demo
from studio.project import save,new_object
from studio.subtitles import write
from studio.animation import ACTIONS
import json

def main():
    root=Path(__file__).resolve().parents[1]
    folder=root/'examples'/'yellow_umbrella';folder.mkdir(parents=True,exist_ok=True)
    p=demo();save(p,folder/'project.json');write(p['subtitles'],folder/'story.srt')
    presets=root/'presets';presets.mkdir(exist_ok=True)
    for a in ACTIONS:
        (presets/(a+'.json')).write_text(json.dumps(dict(action=a,speed=1.,amplitude=1.,motions=[],keys={}),indent=2))
    characters=root/'assets'/'characters';characters.mkdir(parents=True,exist_ok=True)
    for name in ('father','mother','son'):
        o=new_object(preset=name);o['character_id']=name
        (characters/(name+'.json')).write_text(json.dumps(o,indent=2))
    for name in ('backgrounds','props','audio','fonts'):(root/'assets'/name).mkdir(exist_ok=True)
    print('Created editable 12-scene demo and presets.')

if __name__=='__main__':main()
