from LTO.Transactions.RevokeAssociation import RevokeAssociation
from LTO.Transactions.Association import Association
from LTO.Transactions.Anchor import Anchor
from PublicNode import PublicNode
from LTO.Accounts.AccountFactoryED25519 import AccountED25519
import string
import random
from time import time

def random_string(length=16):
  return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

node = PublicNode('https://testnet.lto.network')
aliceSeed = 'prepare awake mule vital rescue when radio view sibling bread spatial abstract visual insane crisp'
alice = AccountED25519('T').createFromSeed(aliceSeed)
bobSeed= 'home visit certain universe adjust thing estate pyramid age puzzle update ensure fatal crucial hat'
bob = AccountED25519('T').createFromSeed(bobSeed)
anchor = random_string()
anchor = '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj'

address = '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj'
account = AccountED25519('T').createFromSeed('cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy')

#transaction = RevokeAssociation(recipient=address, associationType=10)
#transaction = Association(recipient=bob.address, associationType=3434, anchor=anchor)
transaction = Association(recipient=address, associationType=7, anchor='fkjnrefkjenr')
#transaction = Anchor(anchor)
transaction.signWith(account)
transaction.broadcastTo(node)







