
import xml.etree.ElementTree as ET
from Util import Util
import CodeBox

print "##################################"

SEGUE_KIND_RELATIONShIP = "relationship"
SEGUE_RELATIONSHIP_ROOT = "rootViewController"
EXPRESS_TAG = "[[ROOT_CONTROLLER]]"
OC_SWIFT = "swift"

# custom controller
CUSTOM_CONTROLLER_TAG = "[[CUSTOM_CLASS]]"
CONTROLLER_OUTLETS_TAG = "[[OUTLETS]]"
CONTROLLER_SUBVIEWS_TAG = "[[SUBVIEWS]]"
CONTROLLER_ACTIONS_TAG = "[[ACTIONS]]"
SUBVIEW_TYPE_LIST = ["button", "label", "textfield", "textview", "tableview", "imageview"]


def parse_subviews(controllerTemplateText, customControllerEl, lang_type="swift"):
    # find other subviews
    # subviewEls = customControllerEl.findall(".//subviews/")
    subview_els = Util.find_all_element(customControllerEl, ".//subviews/")
    print "sub view tag " + subview_els[0].tag

    if subview_els is None:
        print("no element for subviews here")
        return

    for sEl in subview_els:
        #if subview is button
        if sEl.tag == "button":
            # buttonName = sEl.attrib["id"].replace("-", "")
            # generate a temp id for button
            buttonName = Util.generate_control_id(sEl.attrib["id"])
            print "button name " + buttonName

            # outlet1, subview1 = generate_button(buttonName, sEl)    # insert outlet & view did load attributes
            code_box = CodeBox.CodeBoxFactory.generate_code_box(CodeBox.LanguageType.Swift)
            outlet1, subview1 = code_box.generate_button(buttonName, sEl)
            outletPos = controllerTemplateText.find(CONTROLLER_OUTLETS_TAG)
            if outletPos < 0:
                print "no outlet position placeholder"
            else:
                controllerTemplateText = controllerTemplateText[:outletPos] + outlet1 + controllerTemplateText[
                                                                                        outletPos:]

            # insert subviews in viewDidLoad
            subviewPos = controllerTemplateText.find(CONTROLLER_SUBVIEWS_TAG)
            if subviewPos < 0:
                print "no subview position placeholder"
            else:
                controllerTemplateText = controllerTemplateText[:subviewPos] + subview1 + controllerTemplateText[
                                                                                          subviewPos:]
        elif sEl.tag == "":
            pass

        #TODO: replace placeholders when set all stuff right
    return controllerTemplateText


def main():
 
    tree = ET.parse("material/storyboard.xml")
    root = tree.getroot()

    print root.tag, root.attrib

    initControllerEl = root.attrib["initialViewController"]
    print initControllerEl

    initControllerElElem = './/*[@id=\'%s\']' % (initControllerEl)

    elemList = Util.find_all_element(root, initControllerElElem)
    if len(elemList) <= 0:
        print "initial viewcontroller does not exit"
        return

    initController = elemList[0]
    # print initController.tag

    # parse different kinds of initial controllers
    # first is navigation controller
    if initController.tag == "navigationController":
        '''
        read template file, here's the app delegate file
        '''
        fileHandler = open("templates/appDelegate.template.swift")
        try:
            templateText = fileHandler.read()
            # print templateText
            # connEls = initController.findall(".//connections/segue")

            connEls = Util.find_all_element(initController, ".//connections/segue")

            if connEls is None:
                print "no connections"
                return

            # for cel in connEls:
            # print cel.attrib["destination"]
            relationshipAttrib = connEls[0]

            # find the navigatoin controller's root viewcontroller
            if relationshipAttrib.attrib["kind"] == SEGUE_KIND_RELATIONShIP \
                    and relationshipAttrib.attrib["relationship"] == SEGUE_RELATIONSHIP_ROOT:
                destination = relationshipAttrib.attrib["destination"]

                controllerPath = './/*[@id=\'%s\']' %  (destination)
                # relationshipControllers = root.findall(controllerPath)
                relationshipControllers = Util.find_all_element(connEls[0], controllerPath)

                if len(relationshipControllers) is None:
                    print "no relationship controllers"
                    return

                print relationshipControllers[0].attrib["customClass"]
                customClass = relationshipControllers[0].attrib["customClass"]

                # generate swift code, else generate oc code
                if OC_SWIFT == "swift":
                    # here's swift stuff
                    # app delegate
                    controller1 = "controller1 = %s()" % customClass
                    root_controller = "var nav = UINavigationController(rootViewController: controller1)\n self.window?.rootViewController = nav"
                    insert_state = "%s\n%s" % (controller1, root_controller)
                    templateText = templateText.replace(EXPRESS_TAG, insert_state)

                    destFile = file('generated/appDelegate.swift', 'w+')
                    destFile.write(templateText)

                    # other controllers
                    controllerTemplateHandler = open("templates/ViewController.template.swift")
                    controllerTemplateText = controllerTemplateHandler.read()
                    controllerTemplateText = controllerTemplateText.replace(CUSTOM_CONTROLLER_TAG, customClass)

                    customControllerEl = relationshipControllers[0]
                    subViewEls = customControllerEl.findall(".//view[@key='view']")

                    if len(subViewEls) <= 0:
                        print "no self.view element"
                    else:
                        controllerTemplateText = parse_subviews(controllerTemplateText, customControllerEl)

                    print "custom controller: " + controllerTemplateText
                else:
                    print "your try to generate OC code, which is not implemented yet."
                    # here's oc stuff
            else:
                print "kind is not relationship. not a relationship segue."


            print "try"
        finally:
            print "finally"
    elif initController.tag == "tabBarController":  # tab bar controller as initial controller
        pass
    else:
        pass

if __file__ == "__main__":
    print "main file"
    main()