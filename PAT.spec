# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['PAT.py'],
             pathex=[],
             binaries=[],
             datas=[('sounds/*.mp3','sounds/'),('images/background/desc.png','images/background'),('configs/levelconfigs/end_game_questions.json','configs/levelconfigs'),('configs/levelconfigs/after_block_questions.json','configs/levelconfigs'),('images/objects/coin.png','images/objects'),('images/objects/p1.png','images/objects'),('images/objects/p2.png','images/objects'),('images/objects/p3.png','images/objects'),('images/objects/p4.png','images/objects'),('images/background/1.png','images/background'),('images/background/2.png','images/background'),('images/background/3.png','images/background'),('images/background/start.png','images/background'),('images/background/instructions.png','images/background'),('images/background/pacman.png','images/background'),('fonts/ARIAL.TTF','fonts'),('configs/structure.json','configs'),('configs/levelconfigs/neutral.json','configs/levelconfigs'),('configs/levelconfigs/questions.json','configs/levelconfigs'),('configs/levelconfigs/questions2.json','configs/levelconfigs'),('configs/levelconfigs/goodSpeed.json','configs/levelconfigs'),('configs/levelconfigs/goodCoin.json','configs/levelconfigs'),('configs/levelconfigs/goodAll.json','configs/levelconfigs'),('configs/levelconfigs/badSpeed.json','configs/levelconfigs'),('configs/levelconfigs/badAll.json','configs/levelconfigs'),('configs/levelconfigs/badCoin.json','configs/levelconfigs'),('configs/levelconfigs/test.json','configs/levelconfigs')],
             hiddenimports=['pygame'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          a.binaries,
          a.zipfiles,
          a.datas, 
          [],
          exclude_binaries=True,
          name='PAT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PAT')
