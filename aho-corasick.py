#
# Aho Corasick Automaton, python implementation
#

from collections import deque # For O(1) popleft
class TrieNode:
  def __init__(self, value):
    self.val = value # Not necessary
    self.output = []
    # I use a dictionary instead of a list of
    # alphabets to simplify things
    self.children = {}
    self.fail = None


class Trie:
  def __init__(self):
    self.root = TrieNode('*')

  # Classic trie insert word
  def insertWord(self, word):
    curr = self.root
    for char in word:
      if not char in curr.children:
        curr.children[char] = TrieNode(char)
      curr = curr.children[char]
    curr.output.append(word)

  # Build failure links
  # Idea: 1) All root child nodes fail to root
  #       2) Traverse trie in bfs and for each node:
  #          i) Fail each child to the identical child of the closest fail ancestor
  #             having the same character as that child
  #                            a
  #                         /  |  \
  #                        b   f   g
  #                       /
  #                      q 
  #                     /
  #                    g
  #       ASSUME b is originally the fail link for
  #       q, g (q's child) should fail to g (a's child) during the bfs
  def buildFail(self):
    queue = deque()
    for child in self.root.children:
      childNode = self.root.children[child]
      queue.append(childNode)
      childNode.fail = self.root
    while queue:
      curr = queue.popleft()
      # child is a char not a node
      for child in curr.children:
        childNode = curr.children[child]
        fail = curr.fail
        # go up fail links until root
        while fail:
          if child in fail.children:
            childNode.fail = fail.children[child]
            childNode.output.extend(childNode.fail.output)
            break
          fail = fail.fail
        # child was not found, fail to root
        if not childNode.fail:
          childNode.fail = self.root
        queue.append(childNode)
    self.root.fail = self.root
    
      

class AhoCorasick:
  def __init__(self):
    pass
  def build(self, patterns):
    self.trie = Trie()

    # build trie
    for word in patterns:
      self.trie.insertWord(word)
    
    # construct failure links
    self.trie.buildFail()

  # Actual search
  # Linear search throgh haystack while moving along trie
  # Idea: If we can move along child links, then do
  # else, move along failure link
  def search(self, word):
    matches = {}
    curr = self.trie.root
    i = 0
    while i < len(word) and curr:
      letter = word[i]
      if letter in curr.children:
        curr = curr.children[letter]
      else:
        if curr == self.trie.root:
          i += 1
        curr = curr.fail
        continue
      # output is empty if current node "is not a valid pattern"
      # i.e does not end a pattern
      # If not, output contains all the patterns that end here
      # (both from failure links and child links)
      for output in curr.output:
        if not output in matches:
          matches[output] = []
        matches[output].append(i - len(output) + 1)
      i += 1
    return matches

ac = AhoCorasick()
patterns = ['abc', 'def', 'ghi', 'i']
ac.build(patterns)
print(ac.search('abcdefsghwwrdsdefdifo4kjeffoeaedfijklgghi'))

# Hope it helps :)
