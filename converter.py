
import xml.etree.ElementTree as ET

tree = ET.parse("material/Main.storyboard")
root = tree.getroot()

print(root.tag)

if __file__ == "__main__":
    print "main file"