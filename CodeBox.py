__author__ = 'uncle_charlie'

from Util import Util


# enum
class LanguageType:
    Swift = 10
    ObjC = 100

    def __init__(self):
        pass


class CodeBoxFactory(object):
    code_box_dic = {
        LanguageType.Swift: CodeBoxSwift(),
        LanguageType.ObjC: CodeBoxObjC(),
    }

    '''
        default is swift code generator
    '''
    @staticmethod
    def generate_code_box(lang_type):
        return CodeBoxFactory.code_box_dic.get(lang_type, CodeBoxSwift())


class CodeBox(object):
    def __init__(self):
        pass

    def generate_button(self):
        pass

    def generate_table(self):
        pass


class CodeBoxSwift(CodeBox):

    def __init__(self):
        pass

    def generate_button(self, button_name, elem):

        outlet1 = 'var %s = UIButton! \n' % button_name
        subview1 = ""  # if there's value for frame, this will set some value
        # rectEls = sEl.findall(".//rect[@key='frame']")
        rectEls = Util.find_all_element(elem, ".//rect[@key='frame']")
        if rectEls is None:
            print "no rect for %s" % button_name
            return

        rectEl = rectEls[0]
        rectAttr = rectEl.attrib
        subview1 = '%s.frame = CGRectMake(%s, %s, %s, %s) \n' % \
                   (button_name, rectAttr["x"], rectAttr["y"], rectAttr["width"], rectAttr["height"])

        # stateEls = sEl.findall(".//state[@title]")
        stateEls = Util.find_all_element(elem, ".//state[@title]")
        if stateEls is None:
            print "no state which is used on title value"
        # else:
        stateAttr = stateEls[0].attrib
        subview1 += ('%s.setTitle("%s"1, forState: %s)\n' % (button_name, stateAttr["title"], "UIControlState.Normal"))

        return outlet1, subview1

    def generate_table(self):
        pass


class CodeBoxObjC(CodeBox):

    def __init__(self):
        pass

    def generate_button(self, button_name, elem):
        pass

    def generate_table(self):
        pass