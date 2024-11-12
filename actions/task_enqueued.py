class TaskEnqueued:
  def run(self, conversation, slots, dispatcher, metadata):
    media = {}
    active_media = slots.get('cimEvent',{}).get('data',{}).get('task',{}).get('activeMedia',[])
    
    if len(active_media) > 1:
      for _media in active_media:
        if _media.get('requestSession',{}).get('id','') ==  slots.get('cimEvent',{}).get('channelSession',{}).get('id',''):
          media = _media
    else:
      media = active_media[0]
    
    if media.get('type',{}).get('direction','') != 'CONSULT' and media.get('mrdId', '') != '62f9e360ea5311eda05b0242':
      dispatcher.text("You're routed to an agent, he/she will join in a moment.")
    
    return []
