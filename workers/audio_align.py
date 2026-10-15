from common import *
ctx=context();p=ctx['project'];profile=ctx['worker_profile']
try:
    import whisperx
    # Existing utterance text and utterance windows are reused; no transcribe call.
    audio=whisperx.load_audio(str(Path(ctx['base'])/p['audio']['path']))
    model,metadata=whisperx.load_align_model(language_code=profile['language'],device=profile.get('device','cpu'),model_name=profile['model_path'])
    segments=[{'start':u['start_sample']/48000,'end':u['end_sample']/48000,'text':u['raw_text']} for u in p['utterances'] if u['start_sample'] is not None]
    result=whisperx.align(segments,model,metadata,audio,profile.get('device','cpu'),return_char_alignments=True,interpolate_method='ignore')
    words=[];issues=[]
    for i,seg in enumerate(result['segments']):
        utterance=p['utterances'][i]
        for j,word in enumerate(seg.get('words',[])):
            resolved='start' in word and 'end' in word
            wid=f'{utterance["id"]}_word_{j}'
            words.append({'id':wid,'utterance_id':utterance['id'],'token_index':j,'text':word['word'],'start_sample':round(word['start']*48000) if resolved else None,'end_sample':round(word['end']*48000) if resolved else None,'method':'whisperx','evidence_status':'aligned_estimate' if resolved else 'unresolved','audio_revision':p['audio']['id']})
            if not resolved:issues.append({'id':'unresolved_'+wid,'code':'ANCHOR_UNRESOLVED','severity':'warning','object_ids':[wid],'message':'Từ không căn được; giữ timestamp rỗng','status':'open','source':'alignment'})
        progress((i+1)/len(result['segments']))
    save(ctx,{'segments':p['analysis']['segments'],'words':words,'issues':issues,'model_hash':profile['model_hash'],'adapter':'whisperx-align-only'})
except Exception as e:fail(ctx,'ALIGNMENT_FAILED',str(e))
