
import xml.etree.ElementTree as ET

print "##################################"

SEGUE_KIND_RELATIONShIP = "relationship"
SEGUE_RELATIONSHIP_ROOT = "rootViewController"
EXPRESS_TAG = "[[ROOT_CONTROLLER]]"
OC_SWIFT = "swift"

#custom controller
CUSTOM_CONTROLLER_TAG = "[[CUSTOM_CLASS]]"
CONTROLLER_OUTLETS_TAG = "[[OUTLETS]]"
CONTROLLER_SUBVIEWS_TAG = "[[SUBVIEWS]]"
CONTROLLER_ACTIONS_TAG = "[[ACTIONS]]"
SUBVIEW_TYPE_LIST = ["button", "label", "textfield", "textview", "tableview", "imageview"]
 
tree = ET.parse("material/storyboard.xml")
root = tree.getroot()

print root.tag, root.attrib

initControllerEl = root.attrib["initialViewController"]
print initControllerEl

initControllerElElem = './/*[@id=\'%s\']' % (initControllerEl)
print initControllerElElem

elemList = root.findall(initControllerElElem)

if len(elemList) <= 0:
    print "no such element"

initController = elemList[0]
print initController.tag

if initController.tag == "navigationController":
    '''
    read template file, here's the app delegate file
    '''
    fileHandler = open("templates/appDelegate.template.swift")
    try:
        templateText = fileHandler.read()
        # print templateText
        connEls = initController.findall(".//connections/segue")
        
        if len(connEls) <= 0:
            print "no connections"
        else:
            # for cel in connEls:
            # print cel.attrib["destination"]
            relationshipAttrib = connEls[0]
            
            if relationshipAttrib.attrib["kind"] == SEGUE_KIND_RELATIONShIP \
            and relationshipAttrib.attrib["relationship"] == SEGUE_RELATIONSHIP_ROOT:
                destination = relationshipAttrib.attrib["destination"]

                controllerPath = './/*[@id=\'%s\']' %  (destination)
                relationshipControllers = root.findall(controllerPath)

                if len(relationshipControllers) <= 0:
                    print "no relationship controllers"
                else:
                    print relationshipControllers[0].attrib["customClass"]
                    customClass = relationshipControllers[0].attrib["customClass"]
                    if OC_SWIFT == "swift":
                        # here's swift stuff
                        # app delegate
                        controller1 = "controller1 = %s()" % (customClass)
                        root_controller = "var nav = UINavigationController(rootViewController: controller1)\n self.window?.rootViewController = nav"
                        insert_state = "%s\n%s" %(controller1, root_controller)
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
                            #find other subviews
                            subviewEls = customControllerEl.findall(".//subviews/")
                            print "sub view tag " + subviewEls[0].tag
                            
                            for sEl in subviewEls:
                                #if subview is button
                                if sEl.tag == "button":
                                    buttonName = sEl.attrib["id"].replace("-", "")
                                    print "button name " + buttonName
                                    
                                    outlet1 = 'var %s = UIButton! \n' % (buttonName)
                                    subview1 = "" # if there's value for frame, this will set some value
                                    
                                    rectEls = sEl.findall(".//rect[@key='frame']")
                                    if len(rectEls) <= 0:
                                        print "no rect"
                                    else:
                                        rectEl = rectEls[0]
                                        rectAttr = rectEl.attrib
                                        subview1 = '%s.frame = CGRectMake(%s, %s, %s, %s) \n' % (buttonName, rectAttr["x"], rectAttr["y"],\
                                         rectAttr["width"], rectAttr["height"])
                                        
                                    stateEls = sEl.findall(".//state[@title]")
                                    if len(stateEls) <= 0:
                                        print "no state which is used on title value"
                                    else:
                                        stateAttr = stateEls[0].attrib
                                        subview1 = subview1 + ('%s.setTitle("%s", forState: %s)\n' % (buttonName, \
                                        stateAttr["title"], "UIControlState.Normal"))
                                        
                                    # insert outlet    
                                    outletPos = controllerTemplateText.find(CONTROLLER_OUTLETS_TAG)
                                    if outletPos < 0:
                                        print "no outlet position placeholder"
                                    else:
                                        controllerTemplateText = controllerTemplateText[:outletPos] + outlet1 + controllerTemplateText[outletPos:]
                                        
                                    # insert subviews in viewDidLoad
                                    subviewPos = controllerTemplateText.find(CONTROLLER_SUBVIEWS_TAG)
                                    if subviewPos < 0:
                                        print "no subview position placeholder"
                                    else:
                                        controllerTemplateText = controllerTemplateText[:subviewPos] + subview1 + controllerTemplateText[subviewPos:]
                                    
                                    #TODO: replace placeholders when set all stuff right
                                    
                        print "custom controller: " + controllerTemplateText
                    else:
                        print "your try to generate OC code, which is not implemented yet."
                        # here's oc stuff
            else:
                print "kind is not relationship. not a relationship segue."
            
            
        
        print "try"
    finally:
        print "finally"
else:
    pass

if __file__ == "__main__":
    print "main file"