from pathlib import Path
import asyncio,json,sys
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parent.parent

async def main():
    integration=json.loads((ROOT/'reports/integration-session.json').read_text('utf-8'))
    params=StdioServerParameters(command=sys.executable,args=[str(ROOT/'studio/mcp_bridge.py')],cwd=str(ROOT))
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize();tools=(await session.list_tools()).tools
            for name in ['studio_capabilities','project_summary','plan_preflight']:
                r=await session.call_tool(name,{} if name=='studio_capabilities' else {'project_id':integration['project_id']})
                data=json.loads(r.content[0].text);assert data['ok'],data
            report={'transport':'real STDIO through Python MCP ClientSession','tool_count':len(tools),'tested':['initialize','list_tools','studio_capabilities','project_summary','plan_preflight'],'Codex_client':'configuration generated, not connected','Antigravity_client':'configuration generated, not connected'}
            (ROOT/'reports/mcp-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            print(json.dumps(report,ensure_ascii=False))

asyncio.run(main())
