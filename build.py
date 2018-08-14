# Contributed by Retorillo on August 2018
# Licensed under CC0, No Rights Reserverd

import os
import sys
import math
import fontforge
import psMat

std = fontforge.font()
uni = fontforge.font()

src_a = fontforge.open('src/OCRA.pfa')
src_k = fontforge.open('src/OCR-BKxStd.otf')

# OCRA.pfa has bug unicode value of z is unset(-1)
src_a.selection.select('enc-122');
for g in src_a.selection.byGlyphs:
  g.unicode = 0x007a

def adjust(f, s, w):
  for g in f.glyphs():
    g.transform(psMat.scale(s, s));
    if g.width == 0:
      continue
    elif g.width != w:
      excess = g.width - w
      l = math.floor(excess / 2)
      r = excess - l
      g.left_side_bearing -= l
      g.right_side_bearing -= r
      g.width = w

def copy_glyphs(src, dest, sstart, send, dstart):
  src.selection.select(('ranges', None), sstart, send)
  src.copy()
  dest.selection.select(dstart)
  dest.paste()

name = 'OCR-AK'
copyright = 'OCR-AK, 2018 Retorillo (CC0)\n\
OCR-A, 2018 Jonh Sauter (Public Domain)\n\
OCR-BKxStd, 2010 force4u (CC0)'
version = '1.0'

std.encoding = 'UnicodeFull'
src_a.encoding = 'UnicodeFull'
src_k.encoding = 'UnicodeFull'
adjust(src_k, 1.15, 715)
copy_glyphs(src_a, std, 0x0020, 0x007f, 0x0020)
copy_glyphs(src_a, std, 0x00a3, 0x00fc, 0x00a3)
copy_glyphs(src_k, std, 0x00a1, 0x00df, 0xff61)
std.os2_version = 1
std.fontname = name
std.familyname = name
std.fullname = name
std.version = version
std.copyright = copyright
std.selection.all()
std.autoHint()
std.autoInstr()
std.sfnt_names = (( 'English (US)', 'Copyright', copyright ),
  ( 'English (US)', 'SubFamily', 'Regular' ),
  ( 'English (US)', 'Version', version ),
  ( 'English (US)', 'UniqueID', '%s;%s' % (name, version) ))
std.ascent = src_a.ascent
std.descent = src_a.descent
std.save('dist/OCR-AK.sfd')
std.generate('dist/OCR-AK.ttf')
std.generate('dist/OCR-AK.woff')
