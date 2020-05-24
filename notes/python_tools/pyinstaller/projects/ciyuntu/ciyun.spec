# -*- mode: python ; coding: utf-8 -*-

from wordcloud.wordcloud import FILE

block_cipher = None

added_files = [
    ("icon.ico", "."),
    #("images", "images"),
    ("fonts", "fonts"), 
    (os.path.join(FILE, 'stopwords'), "wordcloud"),
]

a = Analysis(['main.py'],
             pathex=['G:\\important\\pyinstaller_test_2'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
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
          name='ciyun',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='icon.ico')
