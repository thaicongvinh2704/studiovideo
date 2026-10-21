from PySide6.QtCore import QObject,QUrl
from PySide6.QtMultimedia import QAudioOutput,QMediaPlayer
from ..project import resolve

class AudioPreview(QObject):
    def __init__(self,parent=None):
        super().__init__(parent);self.players={}
    def stop(self):
        for player,output in self.players.values():player.stop();player.deleteLater();output.deleteLater()
        self.players.clear()
    def update(self,project,root,t,playing):
        active=[a for a in project['audio'] if not a.get('mute') and a['start']<=t<a['start']+a['duration']]
        ids={a['id'] for a in active}
        for ident in list(self.players):
            if ident not in ids:
                player,output=self.players.pop(ident);player.stop();player.deleteLater();output.deleteLater()
        voiced=any(a['group']=='voice' for a in active)
        for a in active:
            if a['id'] not in self.players:
                player=QMediaPlayer(self);output=QAudioOutput(self);player.setAudioOutput(output)
                player.setSource(QUrl.fromLocalFile(str(resolve(root,a['file']))));self.players[a['id']]=(player,output)
                desired=round((t-a['start']+a.get('trim',0))*1000)
                player.mediaStatusChanged.connect(lambda status,p=player,pos=desired: p.setPosition(pos) if status==QMediaPlayer.MediaStatus.LoadedMedia else None)
            player,output=self.players[a['id']]
            pos=t-a['start'];v=a.get('volume',1)
            if a.get('fade_in',0):v*=min(1,pos/a['fade_in'])
            if a.get('fade_out',0):v*=min(1,(a['duration']-pos)/a['fade_out'])
            if project.get('duck_music') and voiced and a['group']=='music':v*=.3
            output.setVolume(max(0,min(1,v)))
            target=round((pos+a.get('trim',0))*1000)
            if abs(player.position()-target)>250:player.setPosition(target)
            if playing:player.play()
            else:player.pause()
