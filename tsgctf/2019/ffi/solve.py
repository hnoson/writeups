#!/usr/bin/env python
# https://github.com/adobe-type-tools/afdko/
# ttx -t GSUB ffi.ttf

import xml.etree.ElementTree as ET
tree = ET.parse('ffi.ttx')
lookuplist = tree.getroot().find('GSUB/LookupList')
glyph = 'glyph00346'
flag = ''
while True:
    index = lookuplist.find('.//Substitution[@out="%s"]/../..' % glyph).get('index')
    flag = lookuplist.find('.//Substitution[@out="%s"]' % glyph).get('in') + flag
    if index == '0':
        break
    glyph = lookuplist.find('.//ChainContextSubst[@index="%s"]' % index).find('BacktrackCoverage/Glyph').get('value')
flag = 'T' + flag.replace('underscore', '_').replace('braceleft', '{').replace('braceright', '}')
print flag
