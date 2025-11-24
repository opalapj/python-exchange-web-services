from exchangelib import Message
from exchangelib import Q
from myapi import sign_into_account


account = sign_into_account()

# The folder structure is cached after first access to a folder hierarchy.
# This means that external changes to the folder structure will not show up
# until you clear the cache. Here’s how to clear the cache of each of
# the currently supported folder hierarchies:
account.root.refresh()
account.public_folders_root.refresh()

########################################################################

# Not all fields on an item support searching. Here's the list of options for
# Message items.
print(*sorted(f.name for f in Message.FIELDS if f.is_searchable), sep="\n")
print(*sorted(Q.LOOKUP_TYPES), sep="\n")


inbox = account.inbox
# query_set = inbox.all()
query_set = inbox.filter(subject__startswith="RE:")

# first_item = query_set[0]
for item in query_set:
    print(
        item.datetime_received,
        item.author.email_address,
        item.author.name,
        item.subject,
    )
