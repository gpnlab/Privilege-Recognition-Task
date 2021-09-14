# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['/Users/justinzhang/Privilege-Recognition-Task/PAT'],
             binaries=[],
             datas=[('images/objects/coin.png','images/objects'),('images/objects/p1.png','images/objects'),('images/objects/p2.png','images/objects'),('images/objects/p3.png','images/objects'),('images/objects/p4.png','images/objects'),('images/background/pacman.png','images/background'),('fonts/ARIAL.TTF','fonts'),('configs/test/config0.json','configs/test'),('configs/test/config1.json','configs/test'),('configs/test/config2.json','configs/test'),('configs/test/config3.json','configs/test'),('configs/test/config4.json','configs/test'),('configs/test/mainConfig.json','configs/test')],
             hiddenimports=[],
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
          name='__main__',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
