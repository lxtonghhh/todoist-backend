
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'NUMBER STATE TOKHEAT TOKTARGET TOKTEMPRATUREcommands : empty\n                            | commands command\n    command : heatswitch\n                            | targetsetheatswitch : TOKHEAT STATEtargetset : TOKTARGET TOKTEMPRATURE NUMBERempty :'
    
_lr_action_items = {'TOKHEAT':([0,1,2,3,4,5,8,10,],[-7,6,-1,-2,-3,-4,-5,-6,]),'TOKTARGET':([0,1,2,3,4,5,8,10,],[-7,7,-1,-2,-3,-4,-5,-6,]),'$end':([0,1,2,3,4,5,8,10,],[-7,0,-1,-2,-3,-4,-5,-6,]),'STATE':([6,],[8,]),'TOKTEMPRATURE':([7,],[9,]),'NUMBER':([9,],[10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'commands':([0,],[1,]),'empty':([0,],[2,]),'command':([1,],[3,]),'heatswitch':([1,],[4,]),'targetset':([1,],[5,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> commands","S'",1,None,None,None),
  ('commands -> empty','commands',1,'p_commands','exam3parser.py',9),
  ('commands -> commands command','commands',2,'p_commands','exam3parser.py',10),
  ('command -> heatswitch','command',1,'p_command','exam3parser.py',15),
  ('command -> targetset','command',1,'p_command','exam3parser.py',16),
  ('heatswitch -> TOKHEAT STATE','heatswitch',2,'p_heatswitch','exam3parser.py',20),
  ('targetset -> TOKTARGET TOKTEMPRATURE NUMBER','targetset',3,'p_targetset','exam3parser.py',25),
  ('empty -> <empty>','empty',0,'p_empty','exam3parser.py',30),
]
