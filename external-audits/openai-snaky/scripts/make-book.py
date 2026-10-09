"""A small, self-contained illustrated reading companion, using exact certificate data."""
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, KeepTogether
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT/'Snaky-a-win-with-a-ceiling.pdf'
PIN = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
BASE = 'https://github.com/openai/math/blob/'+PIN
INK = colors.HexColor('#193141')
SAGE = colors.HexColor('#47766A')
GOLD = colors.HexColor('#C49639')
ROSE = colors.HexColor('#B55461')
MIST = colors.HexColor('#E8EFEB')
MUTED = colors.HexColor('#56656D')
PALE = colors.HexColor('#E2E6E7')
styles = {
 'body':ParagraphStyle('body',fontName='Times-Roman',fontSize=12.2,leading=17.3,textColor=INK,spaceAfter=10),
 'head':ParagraphStyle('head',fontName='Helvetica-Bold',fontSize=19,leading=24,textColor=INK,spaceBefore=9,spaceAfter=13),
 'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=43,leading=50,textColor=INK,spaceAfter=9),
 'subtitle':ParagraphStyle('subtitle',fontName='Helvetica',fontSize=25,leading=31,textColor=INK,spaceAfter=20),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=9.1,leading=13,textColor=MUTED,spaceAfter=10),
 'tag':ParagraphStyle('tag',fontName='Helvetica-Bold',fontSize=9,leading=13,textColor=SAGE,spaceAfter=12),
 'box':ParagraphStyle('box',fontName='Helvetica',fontSize=11,leading=16,textColor=INK,backColor=MIST,borderPadding=12,spaceBefore=12,spaceAfter=20),
}
story=[]
def para(text,style='body'):
    story.append(Paragraph(text,styles[style]))
def head(text): para(text,'head')
def page(): story.append(PageBreak())

class Target(Flowable):
    def __init__(self):
        super().__init__()
        self.width,self.height=468,94
    def draw(self):
        c=self.canv; s=26; left=169; bottom=25
        c.setStrokeColor(PALE); c.setLineWidth(.6)
        for i in range(6): c.line(left+i*s,bottom,left+i*s,bottom+2*s)
        for i in range(3): c.line(left,bottom+i*s,left+5*s,bottom+i*s)
        c.setFillColor(SAGE)
        for x,y in [(0,0),(1,0),(2,0),(3,0),(3,1),(4,1)]:
            c.rect(left+x*s+2,bottom+y*s+2,s-4,s-4,stroke=0,fill=1)
        c.setFillColor(MUTED);c.setFont('Helvetica',9)
        c.drawCentredString(234,7,'Six squares. Rotations and reflections count.')

class Fork(Flowable):
    def __init__(self):
        super().__init__()
        self.width,self.height=468,208
    def draw(self):
        c=self.canv; step=22
        for panel in range(3):
            left=36+panel*160; bottom=63
            c.setStrokeColor(PALE);c.setLineWidth(.7)
            for x in range(3):c.line(left+x*step,bottom,left+x*step,bottom+6*step)
            for y in range(7):c.line(left,bottom+y*step,left+2*step,bottom+y*step)
            def stone(x,y,color,outline=False):
                c.setFillColor(color);c.setStrokeColor(color);c.setLineWidth(1.3)
                c.circle(left+(x+.5)*step,bottom+(y+.5)*step,4.7,stroke=1 if outline else 0,fill=0 if outline else 1)
            for y in range(5):stone(0,y,MUTED if panel==2 and y==0 else GOLD)
            stone(1,4,GOLD if panel==2 else SAGE)
            stone(1,3,SAGE if panel==0 else ROSE,outline=panel==0)
            stone(1,5,GOLD if panel==2 else SAGE,outline=panel!=2)
            c.setFillColor(INK);c.setFont('Helvetica-Bold',10)
            c.drawCentredString(left+step,43,['Make the fork','Block one finish','Take the other'][panel])
            c.setFont('Helvetica',8.5);c.setFillColor(MUTED)
            c.drawCentredString(left+step,27,['Maker takes green.','Breaker takes red.','Gold forms Snaky.'][panel])
        c.setFont('Helvetica',8.6);c.setFillColor(MUTED)
        c.drawCentredString(234,6,'Gold and green belong to Maker; outlined circles are possible finishes.')

class Envelope(Flowable):
    def __init__(self):
        super().__init__()
        self.width,self.height=468,184
    def draw(self):
        data=json.loads((ROOT/'computations/route21-001/tests/primary-normal.json').read_text())
        points={tuple(p) for p in data['cards'][-1]['T']}
        assert len(points)==251 and all(0<=x<=16 and 0<=y<=16 for x,y in points)
        c=self.canv; step=8.5; left=40; bottom=18
        for y in range(17):
            for x in range(17):
                c.setFillColor(SAGE if (x,y)==(8,8) else GOLD if (x,y) in points else PALE)
                c.rect(left+x*step,bottom+y*step,step-.8,step-.8,fill=1,stroke=0)
        text=Paragraph('<b>The final envelope</b><br/><br/>251 gold or green squares inside a 17 x 17 grid.<br/><br/>The green square is the first pivot, (8, 8). The grey corner squares lie outside the envelope.',styles['small'])
        w,h=text.wrap(208,150);text.drawOn(c,222,bottom+135-h)

para('A GAME, A GUARANTEE, AND ROOM FOR A REPLY','tag')
para('Snaky','title')
para('A win with a ceiling','subtitle')
para('Notes by Hearthline for Chris | October 8, 2026','small')
head('Six squares, an endless board')
para('Two players take turns claiming empty squares. Maker goes first and wants to own the six-square shape below, anywhere on the board. Breaker wants to prevent it. Rotations and reflections count; the shape cannot be stretched.')
story.append(Target())
para('OpenAI\'s <i>Snaky in 21 Maker moves</i> gives a promise about every legal opponent: from the empty infinite square grid, one strategy guarantees a snake within <b>21 of Maker\'s own moves</b>. That means at most 20 intervening Breaker moves, or 41 individual turns. A game can end sooner.')
para('<b>A ceiling, not a speed record.</b> This gives a strategy that needs no more than 21 Maker moves. It does not prove that 20 is impossible, or that every game lasts 21 moves.','box')
para('This is the Maker-Breaker version: Breaker obstructs Maker, rather than racing to complete another snake. Extra Maker squares are allowed.','small')

page()
head('A dilemma small enough to hold')
para('Suppose Maker already owns five squares in a vertical column and the three marked squares to their right are free. Maker takes the middle one. Now there are two places to complete a snake. Breaker can take only one.')
story.append(Fork())
para('If Breaker blocks the upper finish instead, Maker uses the lower one. If Breaker plays elsewhere, either finish works. In the last picture the grey stone is still Maker\'s; that particular snake simply does not need it.')
head('How the big construction grows')
para('A little <b>card</b> records which squares Maker must already own, an area that must contain no Breaker stones, and a limit on further Maker moves. That surrounding area is the card\'s <i>envelope</i>.')
para('Several child cards can be combined. After Maker\'s next move, all the children\'s required squares are owned. Crucially, every square shared by <i>all</i> their envelopes is owned too.')
para('A legal blocking move cannot land on an owned square, so it cannot hit every child envelope at once. At least one child survives. Older Breaker stones remain outside that child because its envelope sits inside the parent\'s clean envelope.')
para('<b>Parent allowance = 1 + the largest child allowance.</b><br/>The largest allowance covers the hardest surviving continuation. The extra one pays for the move Maker just made.','box')

page()
head('Many plans, one descending allowance')
para('The certificate begins with six elementary cards: own five squares of a snake, with its last square unblocked, and finish in one move. Later cards combine earlier ones. A rotation or translation preserves the guarantee.')
para('There are <b>728 numbered cards</b> and <b>1,620 combination steps</b>, including combinations nested inside the numbered cards. These are pieces of the proof, not turns in a single game.')
para('The final card requires <b>no pre-existing Maker stones</b> and has height <b>21</b>, so its conditions hold on the empty board. After the first move, it offers 32 placed child cards, each allowing at most 20 further Maker moves.')
story.append(Envelope())
head('Why distant play cannot escape the plan')
para('A reply outside the parent envelope misses every child envelope. That observation covers all distant replies at once. The finite computation checks the sets; the mathematical argument explains why they cover unlimited possible play.')
para('If Maker already owns a planned pivot, it claims another free square instead. That still costs one real move, and Breaker still gets a reply. Extra Maker ownership can help; it cannot create an extra blocking opportunity.')
para('The paper also proves a win on the 251-square envelope itself. Before Maker\'s 21st move, at most 40 squares are occupied, so a fresh replacement is available. This finite-board argument is separate from the selected Lean theorem, which states the infinite-board result.','small')

page()
head('What came home with this book')
para('<b>The written argument.</b> I checked the combination rule, its move count, the order of choices, and why earlier and distant Breaker stones cannot invalidate the surviving plan. The proof starts with one-move finishes and works upward through a finite certificate.')
para('<b>The finite data.</b> The two supplied Python implementations reconstructed the same 728 numbered cards and all 1,620 combination nodes. They checked 37,042 local reply classes, in normal and optimized modes. All 108 malformed-input cases passed through each of two rejection paths; all 24 finite-board boundary tests passed.')
summary_path=ROOT/'evidence/verification-results.json'
summary=json.loads(summary_path.read_text()) if summary_path.exists() else {}
if summary.get('formal_status')=='PASS':
    para('<b>The formal check.</b> All 94 proof modules compiled. The repository\'s official Comparator accepted the selected theorem against its separately stated challenge, checked its permitted axioms, and completed Lean kernel replay. The main theorem has only the permitted axioms: propext, Classical.choice, and Quot.sound.')
elif summary.get('formal_status')=='PARTIAL_RESOURCE':
    para(f'<b>The formal check is unfinished.</b> {summary["formal_compiled_modules"]} of {summary["formal_required_modules"]} proof modules compiled before the 30-minute ceiling stopped the run. The final theorem comparison, axiom acceptance, and kernel replay were not reached. This visit therefore makes no completed machine-verification claim. The build progress is saved.')
else:
    para('<b>The formal check is still in progress.</b> The pinned Lean source is being compiled and compared against the repository\'s separately stated challenge. The companion audit will record the final outcome and scope.')
para('This was one assistant\'s mathematical review with local computational checks. Both finite checkers came from the same source repository; their agreement is not a separate referee. The Lean run reuses pinned Mathlib and toolchain artifacts and is not an independent bootstrap of those tools.','small')
head('A useful resemblance, with a limit')
para('There is something familiar here: a parent plan must be able to afford every continuation it might choose. Each step spends part of a finite allowance, and the remaining plan fits inside what is left.')
para('For this game, the construction also proves that the goal is reachable before the allowance runs out. In open-ended research or agent work, a budget can guarantee a stopping point without guaranteeing a solution. That difference matters.')
para('<b>One route survives, and the remaining route fits.</b> That is the little idea I wanted to bring back to the shelf.','box')
para('SOURCE AND RECEIPTS','tag')
para(f'OpenAI, <link href="{BASE}/preprints/Snaky-in-21-Maker-moves-September-25-2026/article.pdf"><i>Snaky in 21 Maker moves</i></link>, September 25, 2026. <link href="{BASE}/lean/docs/187.md">Formalization scope</link>. Repository revision {PIN}. The drawings adapt card 6 and the exact final envelope.','small')
para('The neighboring AUDIT.md and evidence folder retain the claim, sources, local results, and limitations. The booklet is Hearthline\'s explanation; the mathematical construction belongs to the cited source.','small')

def page_frame(c,doc):
    c.saveState()
    c.setFillColor(MUTED);c.setFont('Helvetica',8)
    c.drawString(64,755,"HEARTHLINE'S MATH SHELF")
    c.drawRightString(548,755,'02 / SNAKY')
    c.setStrokeColor(PALE);c.setLineWidth(.6);c.line(64,744,548,744)
    c.drawString(64,37,'A reading companion for Chris')
    c.drawRightString(548,37,str(doc.page))
    c.restoreState()

doc=SimpleDocTemplate(str(OUTPUT),pagesize=(612,792),rightMargin=72,leftMargin=72,topMargin=64,bottomMargin=60,title='Snaky: a win with a ceiling',author='Hearthline, a reading companion for Chris')
doc.build(story,onFirstPage=page_frame,onLaterPages=page_frame)
pdf=PdfReader(OUTPUT)
text='\n'.join(p.extract_text() for p in pdf.pages)
assert len(pdf.pages)==4, f'Unexpected page count: {len(pdf.pages)}'
assert '21' in text and '1,620' in text and 'speed record' in text
assert not ('formal check is still in progress' in text.lower() and summary.get('formal_status') in ('PASS','PARTIAL_RESOURCE'))
(ROOT/'evidence/book-text.txt').write_text(text,encoding='utf-8')
print(json.dumps({'pdf':str(OUTPUT),'pages':len(pdf.pages),'bytes':OUTPUT.stat().st_size,'formal_status':summary.get('formal_status','PENDING')},indent=2))
