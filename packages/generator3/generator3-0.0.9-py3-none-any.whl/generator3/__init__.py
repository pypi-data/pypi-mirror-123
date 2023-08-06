import requests
import flask
import json
import os

class Generator():
  def __init__(self,id):
    self.id = str(id)
  def toBlocks(self, path):
    '''
    Converts to scratchblocks and puts each sprites' scripts in a HTML file
    '''
    os.chdir(os.getcwd()+path)
    targets = json.loads(requests.get('https://projects.scratch.mit.edu/'+self.id).text)['targets']

    JSON = []
    fh = open('results.txt','a')

    for i in range(len(targets)):
      ht = open(targets[i]['name']+'.html'.lower(),'w')
      fh.write('{}\n'.format(targets[i]['name']))

      ht.write("""
      <!doctype html>
      <html>
        <head>
          <script src="https://scratchblocks.github.io/js/scratchblocks-v3.5.2-min.js"></script>
        </head>
        <body>
          <p class="blocks">
      """)

      for k in targets[i]['blocks']:
        opcode = targets[i]['blocks'][k]['opcode']
        root = targets[i]['blocks'][k]
        fnd = targets[i]
        let = ''

        if opcode == 'event_whenflagclicked':
          let += 'when flag clicked:'
        if opcode == 'event_broadcast':
          let += 'broadcast [{} v]'.format(root['inputs']['BROADCAST_INPUT'][1][1])
        if opcode == 'event_whenbroadcastreceived':
          br = root['fields']['BROADCAST_OPTION'][0]
          let += 'when i receive [{} v]'.format(br)
        if opcode == 'looks_seteffectto':
          ef = root['fields']['EFFECT'][0]
          num = root['inputs']['VALUE'][1][1]

          let += 'set [{}] effect to ({})'.format(ef.lower(),num)
        if opcode == 'control_create_clone_of':
          mn = root['inputs']['CLONE_OPTION'][1]
          opt = targets[i]['blocks'][mn]['fields']['CLONE_OPTION'][0].replace('_','')
          
          let += 'create clone of [{} v]'.format(opt)
        if opcode == 'control_wait_until':
          cond = root['inputs']['CONDITION'][1]
          if targets[i]['blocks'][cond]['opcode'] == 'sensing_keypressed':
            k = targets[i]['blocks'][cond]['inputs']['KEY_OPTION'][1]
            key = targets[i]['blocks'][k]['fields']['KEY_OPTION'][0]
          let += 'wait until &lt;key [{} v] pressed&gt;'.format(key)
        if opcode == 'sensing_askandwait':
          let += 'ask [{} v] and wait'.format(root['inputs']['QUESTION'][1][1])
        if opcode == 'control_forever':
          let += 'forever'
        if opcode == 'motion_gotoxy':
          try:
            x = root['inputs']['X'][2][0]
            y = root['inputs']['Y'][2][1]
          except IndexError:
            x = root['inputs']['X'][1][0]
            y = root['inputs']['Y'][1][1]
          
          let += 'go to x ({}) y ({})'.format(x,y)
        if opcode == 'motion_changeyby':
          y = root['inputs']['DY'][2][1]

          let += 'change y by ({})'.format(y)
        if opcode == 'motion_glidesecstoxy':
          secs = root['inputs']['SECS'][1][1]
          
          try:
            x = root['inputs']['X'][2][1]
            y = root['inputs']['Y'][2][1]
          except IndexError:
            x = root['inputs']['X'][1][1]
            y = root['inputs']['Y'][1][1]
          
          let += 'glide ({}) secs to x ({}) y ({})'.format(secs,x,y)
        if opcode == 'looks_switchcostumeto':
          cos = root['inputs']['COSTUME'][1]

          try:
            let += 'switch costume to [{} v]'.format(targets[i]['blocks'][cos]['fields']['COSTUME'][0])
          except KeyError:
            let += 'switch costume to (not found)'
        if opcode == 'looks_switchbackdropto':
          bid = root['inputs']['BACKDROP'][1]
          bg = targets[i]['blocks'][bid]['fields']['BACKDROP'][0]

          let += 'switch backdrop to [{} v]'.format(bg)
        if opcode == 'looks_switchbackdroptoandwait':
          bid = root['inputs']['BACKDROP'][1]
          bg = targets[i]['blocks'][bid]['fields']['BACKDROP'][0]

          let += 'switch backdrop to [{} v] and wait'.format(bg)
        if opcode == 'looks_changeeffectby':
          cha = root['inputs']['CHANGE'][1][1]
          ef = root['fields']['EFFECT'][0]

          let += 'change [{} v] effect by ({})'.format(ef.lower(), cha)
        if opcode == 'looks_show':
          let += 'show '
        if opcode == 'looks_hide':
          let += 'hide '
        if opcode == 'data_setvariableto':
          var = root['fields']['VARIABLE'][0]
          val = root['inputs']['VALUE'][1][1]

          let += 'set [{}] to [{}]'.format(var,val)
        if opcode == 'data_hidevariable':
          var = root['fields']['VARIABLE'][0]
          let += 'hide variable [{}]'.format(var)
        if opcode == 'data_showvariable':
          var = root['fields']['VARIABLE'][0]
          let += 'show variable [{}]'.format(var)
        if opcode == 'sound_playuntildone':
          d = root['inputs']['SOUND_MENU'][1]
          val = targets[i]['blocks'][d]['fields']['SOUND_MENU'][0]

          let += 'play sound [{} v] until done'.format(val)

        fh.write(let+'\n')
        ht.write(let+'\n')

      ht.write("""
      </p>
      <script type="text/javascript">
      scratchblocks.renderMatching("p.blocks", {
          style: 'scratch3'
      })
      </script>
      """)

def serveHTML():
  '''
  Serve generated HTML code
  '''
  app = flask.Flask('__main__')

  @app.get('/<f>')
  def getf(f):
    return open(f+'.html').read().replace('\n\n\n','\n')

  app.run(host='0.0.0.0')
