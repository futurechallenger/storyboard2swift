
import xml.etree.ElementTree as ET

print "##################################"

SEGUE_KIND_RELATIONShIP = "relationship"
SEGUE_RELATIONSHIP_ROOT = "rootViewController"
EXPRESS_TAG = "[[ROOT_CONTROLLER]]"
OC_SWIFT = "swift"

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
                        controller1 = "controller1 = %s()" % (customClass)
                        root_controller = "var nav = UINavigationController(rootViewController: controller1)\n self.window?.rootViewController = nav"
                        insert_state = "%s\n%s" %(controller1, root_controller)
                        templateText = templateText.replace(EXPRESS_TAG, insert_state)
                        
                        destFile = file('generated/appDelegate.swift', 'w+')
                        destFile.write(templateText)
                    else:
                        pass
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