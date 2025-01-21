from django.core.management.base import BaseCommand, CommandError
import os
import xml.etree.ElementTree as ET
from addressBook.contacts.models import Contact
from django.conf import settings


class Command(BaseCommand):
    help = "Import contacts from an XML file"

    def handle(self, *args, **options):
        file_path = os.path.join(settings.MEDIA_ROOT, 'import_files', 'importContacts.xml')
        if not os.path.exists(file_path):
            raise CommandError(f"File not found: {file_path}")

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            contacts_to_create = []
            contacts_to_update = []

            for contact_elem in root.findall('Contact'):
                contact_id = int(contact_elem.find('id').text)
                contact_data = {
                    'first_name': contact_elem.find('first_name').text or '',
                    'last_name': contact_elem.find('last_name').text or '',
                    'image': contact_elem.find('image').text or None,
                    'company_name': contact_elem.find('company_name').text or '',
                    'address': contact_elem.find('address').text or '',
                    'company_phone': contact_elem.find('company_phone').text or '',
                    'email': contact_elem.find('email').text or '',
                    'fax_number': contact_elem.find('fax_number').text or '',
                    'phone_number': contact_elem.find('phone_number').text or '',
                    'comment': contact_elem.find('comment').text or '',
                    'user_id': int(contact_elem.find('user_id').text),
                }

                # Check if the contact exists
                contact = Contact.objects.filter(id=contact_id).first()
                if contact:
                    # Update existing contact
                    for key, value in contact_data.items():
                        setattr(contact, key, value)
                    contacts_to_update.append(contact)
                else:
                    # Create a new contact
                    contacts_to_create.append(Contact(id=contact_id, **contact_data))

            # Perform bulk operations
            if contacts_to_create:
                Contact.objects.bulk_create(contacts_to_create)
            if contacts_to_update:
                Contact.objects.bulk_update(
                    contacts_to_update,
                    ['first_name', 'last_name', 'image', 'company_name', 'address',
                     'company_phone', 'email', 'fax_number', 'phone_number', 'comment', 'user_id']
                )

        except Exception as e:
            raise CommandError(f"Failed to import contacts: {e}")

        self.stdout.write(self.style.SUCCESS(f'Successfully imported contacts from "{file_path}".'))
