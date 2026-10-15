from common import *
ctx=context();profile=ctx['worker_profile']
try:
    import os
    os.environ['HF_HUB_OFFLINE']='1'
    from vieneu import Vieneu
    # Explicit local graph directory. Offline environment prevents hidden downloads.
    tts=Vieneu(backend='onnx',device='cpu',precision=profile.get('precision','fp32'),onnx_dir=profile['model_path'],backbone_repo=profile['backbone_path'],threads=4,babble_retries=0)
    text=ctx['parameters']['text']
    if not text.strip():fail(ctx,'TTS_TEXT_EMPTY','Không có lời để tạo')
    progress(.1)
    audio=tts.infer(text,voice=ctx['parameters'].get('voice',profile['voice']))
    target=Path(ctx['work'])/'tts.wav';tts.save(audio,str(target))
    save(ctx,{'audio_path':str(target),'voice':ctx['parameters'].get('voice',profile['voice']),'model_hash':profile['model_hash'],'license_record':profile['license_record'],'automatically_applied':False});progress(1)
except Exception as e:fail(ctx,'TTS_FAILED',str(e))
