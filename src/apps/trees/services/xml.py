
class XmlListConfig(list):
    def __init__(self, aList):
        super().__init__()
        for element in aList:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    def __init__(self, parent_element):
        super().__init__()
        if parent_element.items():
            self.update_shim(dict(parent_element.items()))
        for element in parent_element:
            if len(element):
                a_dict = XmlDictConfig(element)
                if element.items():
                    a_dict.update_shim(dict(element.items()))
                self.update_shim({element.tag: a_dict})
            elif element.items():
                self.update_shim({element.tag: dict(element.items())})
            else:
                self.update_shim({element.tag: element.text.strip()})

    def update_shim(self, a_dict):
        for key in a_dict.keys():
            if key in self:
                value = self.pop(key)
                if type(value) is not list:
                    list_of_dicts = [value, a_dict[key]]
                    self.update({key: list_of_dicts})
                else:
                    value.append(a_dict[key])
                    self.update({key: value})
            else:
                self.update(a_dict)
