"""Source-preserving typography repairs for the supplied Word math export."""
from copy import deepcopy
import hashlib
from lxml import etree
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

NS={'m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
GLYPHS={'⌀':'∅','*':'∗','\\':'∖','\u200b':''}

def normalize_math(doc):
    repairs=[]
    for index,math in enumerate(doc.element.xpath('//m:oMath')):
        before=etree.tostring(math,method='c14n')
        operations=[]
        for node in math.xpath('.//m:t',namespaces=NS):
            if node.text=='|':
                run=node.getparent();props=run.find(qn('m:rPr'))
                if props is None:props=OxmlElement('m:rPr');run.insert(0,props)
                literal=OxmlElement('m:lit');literal.set(qn('m:val'),'1');props.append(literal)
                operations.append({'kind':'format','symbol':'|','change':'Mark restriction bar literal so the converter does not parse an unmatched delimiter'})
            if node.text in GLYPHS:
                original=node.text;node.text=GLYPHS[original]
                operations.append({'kind':'glyph','before':original,'after':node.text})
        matrix=math.find(qn('m:m'))
        text=''.join(math.xpath('.//m:t/text()',namespaces=NS))
        if matrix is not None and text.startswith('F⋆=F∧'):
            children=[deepcopy(child) for row in matrix.findall(qn('m:mr')) for cell in row.findall(qn('m:e')) for child in cell]
            math.remove(matrix)
            for child in children:math.append(child)
            operations.append({'kind':'layout','equation':'9a','change':'Two aligned rows joined into one complete equation; token order unchanged'})
        elif matrix is not None and text.startswith('Ccorrection='):
            array=OxmlElement('m:eqArr')
            for row in matrix.findall(qn('m:mr')):
                entry=OxmlElement('m:e')
                for cell in row.findall(qn('m:e')):
                    for child in cell:entry.append(deepcopy(child))
                array.append(entry)
            math.remove(matrix);math.append(array)
            operations.append({'kind':'layout','equation':'C2','change':'Aligned matrix replaced by equation array; rows and token order unchanged'})
        after=etree.tostring(math,method='c14n')
        if before!=after:
            repairs.append({'math_object_index':index,'before_sha256':hashlib.sha256(before).hexdigest(),
                            'after_sha256':hashlib.sha256(after).hexdigest(),'operations':operations})
    return repairs
