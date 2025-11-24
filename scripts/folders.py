from exchangelib import Folder
from myapi import sign_into_account


account = sign_into_account()

# The folder structure is cached after first access to a folder hierarchy.
# This means that external changes to the folder structure will not show up
# until you clear the cache. Here’s how to clear the cache of each of
# the currently supported folder hierarchies:
account.root.refresh()
account.public_folders_root.refresh()

########################################################################

root = account.root
root.parent
root.children
root.absolute
root.total_count
root.child_folder_count
root.unread_count
print(root.tree())
for folder in root.walk():
    print(folder)

inbox = account.inbox
inbox.parent
inbox.children
inbox.absolute
inbox.total_count
inbox.unread_count
inbox.child_folder_count
print(inbox.tree())
for folder in inbox.walk():
    print(folder)

benefits = inbox // "benefits"
benefits.parent
benefits.children
benefits.absolute
benefits.total_count
benefits.unread_count
benefits.child_folder_count
print(benefits.tree())

responses = Folder(parent=inbox, name="responses")
responses.save()

query_set = inbox.filter(subject__startswith="RE:")
query_set.count()
query_set.copy(to_folder=responses)

responses.delete()
