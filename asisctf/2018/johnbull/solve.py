#!/usr/bin/env python
from Crypto.Util.number import *
import gmpy

def make_key(k):
    while True:
        r = getRandomInteger(k) << 2
        p, q = r**2+r+1, r**2+3*r+1
        if gmpy.is_prime(p) * gmpy.is_prime(q):
            break
    pubkey = r**6 + 5*r**5 + 10*r**4 + 13*r**3 + 10*r**2 + 5*r + 1
    return pubkey

def encrypt(m, pubkey):
    return pow(bytes_to_long(m), pubkey, pubkey)

pubkey = 3415775651990117231114868059991823731694168391465118261123541073986397702947056759501589697018682285283905893102019391953165129250445987511496328390478214156138550568081360884795196720007402795178414072586445084589188812271144227913976270609786532206307549154139514246177504313696905220271023590900584622193476455815728425827517096143262953674043805121028581660274394493861460258597130188538332977679416970808454282017991307383835356188698891323239771333178860346825972405652914210954631134409600833327693593543421410732434281694454355747008933885889869077937880862749049074740126067215284910788706518425606114203333939656875871818894784079170292840540681948732880660003000926906333894065117345867196506856521542472349855590932301830372695420851264943795112040150205561483289746364835891125359307397506516272039186039783992620965800450343112765502550149168357851547665186618429181796721954012847077634388652598794182315250366936611355658686688939934516900009808518223359241944137277154786476218874224865037819222158865245588353031015122185374014406127446401298766736266831637852985756300017995390160761028057020573055543615912481389851812757348379419397130083208775789655825117981028241260930861007152057766814139170496584713321278626253968883276653358428036897577768739458725693447122759791961361097160265922640311146274535842798727318743122276126487545827596583971543880517021741131581309905790220398409615820785382645469996656013188425862658824568438227653902664968157149269346732859000330582545267782235066499139875211275390674091559851875853548905976806413521230016513322214240509217605309858575530246251875145909490471112222194075412324792050366838359937779806344187239056856471058353548936427916942194109609165854034767323294935701500110192365307711393371247166567444590592355257900093259599574780053937287600294098393324949090038950101
enc = 172254401616728337848224556256193294668254066768665624620573955921904663415844987360305683044269987528418379305124320147209588306619600641931717574384801086412717165043339754089854945269488039157031822759552038220243667748187712406870604130874288848961422658181035116276222087495309539815379227353704980160563111860011813283093207521575802100014408033039719223557618408913808906098293389776713037943338000210957134248117986210892735617670398002934139712508431588063592442750666131635721232279579114412057382482634199793027886476451072132799009262126068858578298283046601000880559403008084425323306037979617803443696059413247270929031458924282241105950888791411422687779723342754994324724737283365077742875322607687106058784350376580745162809296384205316865766883773721914203935128431492247985755204159286761485776182149007712492892483933270120585324692872062057327390303613634093538988078627329297217605056348331910353384255935457914956221810806802338940927281542361188610818936740209620052730118914762676848436107226923154169182628394200511074094416135594725057729803618271672713265182266181460723433237689954353512385555171399460870707449024037962690482864822971633650492835486036834553508571232609988066578567702464349018675580536990329927725573108328721614238899767792645665535623446031410358844459259283846182131541439033837736746980370117933542817231688533759434901524622912254499686908606070397662874360407075300248727974071742299708009048853008697832021516188431289704110567432234451743516365186915321744582268642673156685090283640357282428092579506635927396169516769103184205482482269342855874163597222301484981530193824960936155581252590505096646005478378577133665334258562017564658379524993172647857018916805201682065829122503078635804169426240558643597061660475712949155431727872200202869508621492240387907991955060578185917725771

l, r = 0, 1<<1024
while l + 1 < r:
    m = (l + r) // 2
    if m ** 6 + 5 * m ** 5 + 10 * m ** 4 + 13 * m ** 3 + 10 * m ** 2 + 5 * m + 1 <= pubkey:
        l = m
    else:
        r = m
p, q = l ** 2 + l + 1, l ** 2 + 3 * l + 1
assert p * p * q == pubkey

totient = (p ** 2 - p) * (q - 1)
e = pubkey % totient
mp = pow(enc, gmpy.invert(q, totient), p)
mq = pow(enc % q, gmpy.invert(p * p, q - 1), q)
print long_to_bytes(mp)
