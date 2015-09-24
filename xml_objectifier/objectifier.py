from lxml import objectify
from bunch import Bunch
import datetime


class MethodMixin(object):
    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
        self.rendering_hints[key] = self.rendering_hints[key].strip()

    def tag_type(self, tag_type):
        return {'{http://www.mrc-epid.cam.ac.uk/schema/common/epi}title': self.set_title, 
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}info': self.set_info,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}renderingHint': self.set_rendering_hint,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}externalPrograms': self.set_external_programs,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}option': self.set_options,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}restrictions': self.set_restrictions,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}textNode': self.set_text_node,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}question': self.set_question,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}questionGroup':self.set_question_group,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}variable': self.set_variable,
                '{http://www.mrc-epid.cam.ac.uk/schema/common/epi}rtConditions': self.set_rtConditions,
                }[tag_type]

    def __str__(self):
        return "%s: %s" % (self.title, self.position)

    def __unicode__(self):
        return "%s: %s" % (self.title, self.position)
        
    def set_rtConditions(self, item):
        pass

    def set_title(self, item):
        pass

    def set_variable(self, item):
        pass

    def set_options(self, item):
        pass

    def set_info(self, item):
        pass

    def set_external_programs(self, item):
        pass

    def set_text_node(self, item):
        pass

    def set_question(self, item):
        pass

    def set_question_group(self, item):
        pass

    def set_restrictions(self, item):
        pass


class Question(MethodMixin):
    def __init__(self, question_object, app_object, section_object):
        self.app_object = app_object
        self.question_objects = []
        self.section = section_object
        self.title = question_object.attrib['position']
        self.variable = question_object.variable.varName.text
        self.var_value = None
        self.var_id = None
        self.required = False
        self.dynamic = False
        self.maxlength = 0
        self.multi = False
        self.tests = []
        self.info = []
        self.data_type = {}
        self.pattern = ''
        self.id = question_object.attrib['ID']
        self.position = question_object.attrib['position']
        self.rendering_hints = {}
        self.restrictions = {}
        self.template = ''
        self.template_args = {'options': []}
        self.model = None
        self.build_question(question_object)
        self.validator_rules()
        self.app_object.validator[self.variable] = self

    def validator_rules(self):
        rules = {}
        try:
            rules['type'] = self.data_type['type']
            self.tests.append('type')
            try:
                self.pattern = self.data_type['pattern']
            except:
                pass
        except:
            pass
        if 'CheckMaxLength' in self.restrictions.keys():
            rules['CheckMaxLength'] = self.data_type['maxLength']
            self.maxlength = self.data_type['maxLength']
            self.tests.append('CheckMaxLength')
        if 'IsAnswered' in self.restrictions.keys():
            if self.restrictions['IsAnswered']['AllowError'] == 'false':
                rules['IsAnswered'] = True
                self.required = True
                self.tests.append('IsAnswered')
        return rules

    def get_template(self, selection):
        pass

    def set_template(self):
        pass

    def build_question(self, question_object):
        for item in question_object.getchildren():
            self.tag_type(item.tag)(item)
        self.set_template()

    def set_options(self, item):
        try:
            if item.optionText.text == 'dynamic':
                self.template_args['options'] = self.get_options(item.optionValue.text)
                self.dynamic = True
            else:
                self.template_args['options'].append({'text': item.optionText.text, 'value': item.optionValue.text})
        except:
            self.template_args['options'].append({'text': item.optionValue.text, 'value': item.optionValue.text})

    def get_options(self, item):
        pass

    def set_info(self, item):
        q_info = {}
        q_info['text'] = item.text
        q_info['cssClass'] = item.attrib['cssClass']
        try:
            q_info['cssClass'] = item.attrib['cssClass']
        except:
            q_info['cssClass'] = ''
        self.info.append(q_info)

    def set_restrictions(self, item):
        for rule in item.getchildren():
            parameters = {}
            for p in rule.getchildren():
                parameters[p.attrib['use']] = p.text
            self.restrictions[rule.attrib['name']] = parameters

    def set_variable(self, item):
        """Sets the variable data type.  Variable name has already been set."""
        try:
            for dt in item.dataType.getchildren():
                self.data_type['type'] = dt.tag.replace('{http://www.mrc-epid.cam.ac.uk/schema/common/epi}', '')
                for child in dt.getchildren():
                    self.data_type[child.tag.replace('{http://www.mrc-epid.cam.ac.uk/schema/common/epi}', '')] = child.text
        except:
            pass


class QuestionGroup(MethodMixin):
    def __init__(self, question_group_object, app_object, section_object):
        self.app_object = app_object
        self.section = section_object
        self.question_group_objects = []
        self.info = []
        self.title = question_group_object.title
        self.position = question_group_object.attrib['position']
        self.rendering_hints = {}
        self.build_question_group(question_group_object)

    def build_question_group(self, question_group_object):
        for item in question_group_object.getchildren():
            self.tag_type(item.tag)(item)

    def set_info(self, item):
        qg_info = {}
        qg_info['text'] = item.text
        try:
            qg_info['cssClass'] = item.attrib['cssClass']
        except:
            qg_info['cssClass'] = ''
        self.info.append(qg_info)

    def set_text_node(self, item):
        text_node = Bunch()
        text_node.rendering_hints = {}
        try:
            text_node['id'] = item.attrib['ID']
        except:
            text_node['id'] = None
        text_node['position'] = item.attrib['position']
        try:
            text_node['text'] = item.info.text
        except:
            text_node['text'] = ''
        try:
            for rh in item.renderingHint:
                key = rh.rhType.text
                text_node.rendering_hints[key] = ''
                for rhdata in rh.rhData:
                    text_node.rendering_hints[key] = text_node.rendering_hints[key] + ' ' + str(rhdata)
                text_node.rendering_hints[key] = text_node.rendering_hints[key].strip()
        except:
            pass
        self.question_group_objects.append(text_node)

    # @logger
    def set_question(self, item):
        question = Question(item, self.app_object, self.section)
        self.question_group_objects.append(question)

    def get_question(self, question):
        for q in self.question_group_objects:
            if q.position == question:
                return q


class Section(MethodMixin):
    def __init__(self, section_xml_object, app_object):
        """Initializes Section object."""
        self.app_object = app_object  # reference to parent
        self.section_xml_object = section_xml_object  # section xml
        self.title = section_xml_object.title
        self.position = section_xml_object.attrib['position']
        self.info = []
        self.api = {}
        self.question_groups = []
        self.errors = {}
        self.section_objects = []
        self.rendering_hints = {}
        self.build_section()

    def build_section(self):
        """sets Question Group instance's properties."""
        for item in self.section_xml_object.getchildren():
            self.tag_type(item.tag)(item)

    def set_info(self, item):
        """Sets properties with Info tag."""
        section_info = {}
        section_info['text'] = item.text
        try:
            section_info['cssClass'] = item.attrib['cssClass']
        except:
            section_info['cssClass'] = ''
        self.info.append(section_info)
        # self.section_objects.append(section_info)

    def set_question_group(self, item):
        """Creates Question Group instances."""
        question_group = QuestionGroup(item, self.app_object, self)
        self.question_groups.append(question_group)
        self.section_objects.append(question_group)

    def get_question_group(self, question_group):
        for qg in self.question_groups:
            if qg.position == question_group:
                return qg


class Application(object):
    def __init__(self, name, xml_path):
        """Initializes the Application object."""
        self.name = name
        self.xml = self.stringify(xml_path)
        self.validator = {}
        self.xml_object = objectify.fromstring(self.xml)
        self.id = self.xml_object.attrib['ID']
        self.author = self.xml_object.author
        self.version_number = self.xml_object.versionNumber
        self.version_date = self.xml_object.versionDate
        self.title = self.xml_object.title
        self.studyname = self.xml_object.studyName
        self.sections = self.get_sections()

    def stringify(self, xml_path):
        return open(xml_path, 'r').read()

    def tidy(self, data):
        for k in data.keys():
            if isinstance(data[k], datetime.date):
                data[k] = str(data[k])

    def get_sections(self):
        """Instantiates Section objects for each section."""
        sections = {}
        for section in self.xml_object.section:
            sections[section.attrib['position']] = Section(section, self)
        return sections

    def __str__(self):
        return """
        App Name: %s
        Author: %s
        Version Number: %s
        Version Date: %s
        Title: %s
        Study Name: %s
        """ % (self.name, self.author, self.version_number,
                self.version_date, self.title, self.studyname)