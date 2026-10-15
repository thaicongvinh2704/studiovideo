from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
python=str(root/'.venv/Scripts/python.exe');script=str(root/'studio/mcp_bridge.py')
directory=root/'config';directory.mkdir(exist_ok=True)
# TOML literal strings preserve Windows backslashes; path is generated on this machine.
(directory/'codex.toml').write_text("[mcp_servers.story_motion_studio]\ncommand = '"+python+"'\nargs = ['"+script+"']\ncwd = '"+str(root)+"'\nstartup_timeout_sec = 30\ntool_timeout_sec = 40\n",encoding='utf-8')
(directory/'antigravity.json').write_text(json.dumps({'mcpServers':{'story_motion_studio':{'command':python,'args':[script],'cwd':str(root)}}},ensure_ascii=False,indent=2),encoding='utf-8')
print('Client examples generated. Global agent config has not been modified.')
