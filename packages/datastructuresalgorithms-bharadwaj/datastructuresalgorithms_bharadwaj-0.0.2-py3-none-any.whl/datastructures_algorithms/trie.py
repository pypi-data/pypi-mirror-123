class TrieNode:
    def __init__(self):
        self.nodes = dict()
        self.is_leaf = False


class Trie:
    def __init__(self):
        self.root_node = TrieNode()
        self.__word_list = ""

    """
        def delete(self, word: str):

            def _delete(curr: TrieNode, word: str, index: int):
                if index == len(word):
                    # If word does not exist
                    if not curr.is_leaf:
                        return False
                    curr.is_leaf = False
                    return len(curr.nodes) == 0
                char = word[index]
                char_node = curr.nodes.get(char)
                # If char not in current trie node
                if not char_node:
                    return False
                # Flag to check if node can be deleted
                delete_curr = _delete(char_node, word, index + 1)
                if delete_curr:
                    del curr.nodes[char]
                    return len(curr.nodes) == 0
                return delete_curr

        _delete(self, word, 0)
    """

    def insert_many(self, words: [str]):
        for word in words:
            self.insert(word)

    def insert(self, word: str):
        curr = self.root_node
        for char in word:
            if char not in curr.nodes:
                curr.nodes[char] = TrieNode()
            curr = curr.nodes[char]
        curr.is_leaf = True

    def find(self, word: str):
        curr = self.root_node
        for char in word:
            if char not in curr.nodes:
                return False
            curr = curr.nodes[char]
        return curr.is_leaf

    def __collect_words(self, curr_node: TrieNode, word: str):

        if curr_node.is_leaf:
            self.__word_list = self.__word_list + word + " "

        for key, value in curr_node.nodes.items():
            self.__collect_words(value, word + key)

    def return_words(self):
        self.__collect_words(self.root_node, "")
        return self.__word_list
