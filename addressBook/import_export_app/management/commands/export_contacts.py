from django.core.management.base import BaseCommand, CommandError
import os
import django
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.dom import minidom
from django.conf import settings
from addressBook.contacts.models import Contact

class Command(BaseCommand):
    help = "Export all contacts to a CSV file"

    def handle(self, *args, **options):
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, 'export_files', 'exportContacts.xml')
            root = ET.Element('DataSet1')
            add_contacts_to_tree(root)
            pretty_contact_xml = prettify(root)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(pretty_contact_xml)
        except Exception as e:
            raise CommandError(f"Failed to export contacts: {e}")

        self.stdout.write(
            self.style.SUCCESS('XLM file with contact is create on that path: "%s"' % file_path)
        )


def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

# Function to handle contact creation in XML
def create_contact(contact, root):
    path_image = contact.image.url
    while 'media/' in path_image:
        path_image = path_image.replace('media/', '', 1)

    if path_image.startswith('/'):
        path_image = path_image[1:]

    contact_elem = ET.SubElement(root, 'Contact')
    SubElement(contact_elem, 'id').text = str(contact.id)
    SubElement(contact_elem, 'first_name').text = contact.first_name or ''
    SubElement(contact_elem, 'last_name').text = contact.last_name or ''
    SubElement(contact_elem, 'image').text = (
        path_image
    )
    SubElement(contact_elem, 'company_name').text = contact.company_name or ''
    SubElement(contact_elem, 'address').text = contact.address or ''
    SubElement(contact_elem, 'company_phone').text = contact.company_phone or ''
    SubElement(contact_elem, 'email').text = contact.email or ''
    SubElement(contact_elem, 'fax_number').text = contact.fax_number or ''
    SubElement(contact_elem, 'phone_number').text = contact.phone_number or ''
    SubElement(contact_elem, 'comment').text = contact.comment or ''
    SubElement(contact_elem, 'user_id').text = str(contact.user_id)

    # Adding labels (ManyToManyField)
    # labels_elem = ET.SubElement(contact_elem, 'labels')
    # for label in contact.labels.all():
    #     label_elem = ET.SubElement(labels_elem, 'label')
    #     label_elem.text = label.name
    return contact_elem

# Function to add all contacts to the XML tree
def add_contacts_to_tree(root):
    contacts = Contact.objects.all()
    for contact in contacts:
        create_contact(contact, root)

# Export function
def export_contacts(root_tag='DataSet1'):
    file_path = os.path.join(settings.MEDIA_ROOT, 'export_files', 'exportContacts.xml')
    root = ET.Element(root_tag)
    add_contacts_to_tree(root)
    pretty_contact_xml = prettify(root)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(pretty_contact_xml)
