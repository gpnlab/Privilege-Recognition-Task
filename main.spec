# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['__main__.py'],
             pathex=[],
             binaries=[],
             datas=[('images/objects/coin.png','images/objects'),('images/objects/p1.png','images/objects'),('images/objects/p2.png','images/objects'),('images/objects/p3.png','images/objects'),('images/objects/p4.png','images/objects'),('images/background/pacman.png','images/background'),('fonts/ARIAL.TTF','fonts'),('configs/structure.json','configs'),('configs/levelconfigs/neutral.json','configs/levelconfigs'),('configs/levelconfigs/questions.json','configs/levelconfigs'),('configs/levelconfigs/questions2.json','configs/levelconfigs'),('configs/levelconfigs/goodSpeed.json','configs/levelconfigs'),('configs/levelconfigs/goodCoin.json','configs/levelconfigs'),('configs/levelconfigs/goodAll.json','configs/levelconfigs'),('configs/levelconfigs/badSpeed.json','configs/levelconfigs'),('configs/levelconfigs/badAll.json','configs/levelconfigs'),('configs/levelconfigs/badCoin.json','configs/levelconfigs'),('configs/levelconfigs/test.json','configs/levelconfigs')],
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
          name='PAT',
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
          entitlements_file=None)

app = BUNDLE(exe,
    name='PAT.app',
    icon='pac-man.icns',
    bundle_identifier='com.GPN.PAT',
    info_plist={
      'CFBundleName': 'PAT',
      'CFBundleDisplayName': 'PAT',
      'CFBundleVersion': '1.0.1',
      'CFBundleShortVersionString': '1.0.0',
      'NSRequiresAquaSystemAppearance': 'No',
      'NSHighResolutionCapable': 'True',
    },
)
