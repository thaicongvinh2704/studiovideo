from common import *
ctx=context();p=ctx['project'];profile=ctx['worker_profile']
try:
    from faster_whisper import WhisperModel
    from difflib import SequenceMatcher
    model=WhisperModel(profile['model_path'],device=profile['device'],compute_type=profile['compute_type'],local_files_only=True,cpu_threads=4)
    segments,info=model.transcribe(str(Path(ctx['base'])/p['audio']['path']),language=profile['language'],vad_filter=True,word_timestamps=False,beam_size=5)
    output=[]
    for seg in segments:
        output.append({'id':'asr_'+str(seg.id),'start':seg.start,'end':seg.end,'text':seg.text,'start_sample':round(seg.start*48000),'end_sample':round(seg.end*48000),'avg_logprob':seg.avg_logprob})
        progress(min(.95,seg.end/(p['audio']['sample_count']/48000)))
    issues=[]
    for u in p['utterances']:
        overlapping=[s['text'] for s in output if s['end_sample']>u['start_sample'] and s['start_sample']<u['end_sample']]
        observed=' '.join(overlapping).strip()
        if SequenceMatcher(None,u['raw_text'].lower(),observed.lower()).ratio()<.65:
            issues.append({'id':'mismatch_'+u['id'],'code':'AUDIO_TEXT_MISMATCH','severity':'warning','object_ids':[u['id']],'message':'ASR và lời gốc khác nhau; cần đối chiếu, không tự sửa','evidence':{'srt':u['raw_text'],'asr':observed},'status':'open','source':'asr_diff'})
    save(ctx,{'segments':output,'language':info.language,'model_hash':profile['model_hash'],'adapter':'faster-whisper','issues':issues,'words':[]});progress(1)
except Exception as e:fail(ctx,'GPU_OOM' if 'out of memory' in str(e).lower() else 'ASR_FAILED',str(e))
