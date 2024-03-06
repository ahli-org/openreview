import getpass
from openreview.api import OpenReviewClient

username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

BASE_API_URL = "https://api2.openreview.net"

client = OpenReviewClient(
    baseurl=BASE_API_URL,
    username=username,
    password=password
)

# How to Undo Deployed Assignments
# See: https://docs.openreview.net/how-to-guides/paper-matching-and-assignment/how-to-undo-deployed-assignments
domain = 'chilconference.org/CHIL/2024/Conference'
notes = client.get_notes(invitation=f'{domain}/Senior_Area_Chairs/-/Assignment_Configuration')

# for reviewers
# notes = client.get_notes(invitation=f'{domain}/Reviewers/-/Assignment_Configuration')

for note in notes:
    if note.content['status']['value'] == 'Deployed':
        configuration_note = note
        break

client.post_note_edit(invitation=f'{domain}/-/Edit',
signatures=['~Tom_Pollard1'],
note=openreview.api.Note(
  id=configuration_note.id,
  content={
     'status': { 'value': 'Complete' }
  }
))
print('The deployment has been undone.')
