__author__ = 'uncle_charlie'


class Util(object):
    @classmethod
    def find_all_element(cls, el, xpath_expr):
        el_list = el.findall(xpath_expr)

        if len(el_list) <= 0:
            return None
        else:
            return el_list

    @classmethod
    def generate_control_id(cls, raw_id):
        new_id = raw_id.replace("-", "")
        return new_id