class SuperNode:
    def __init__(self, _id, _type, _hatchet_nid):
        self.id = _id
        self.type = _type
        self.hid = _hatchet_nid

    def get_name(self, idx, ntype):
        """
        Getter to get the node's name based on type.

        :param idx (int): node index
        :param ntype (str): node type (e.g., module, callsite)
        :return name (str)
        """
        if ntype == "callsite":
            return self.idx2callsite[idx]
        if ntype == "module":
            return self.idx2module[idx]
        assert 0

    def get_idx(self, name, ntype):
        """
        Getter to get the node's index based on type.

        :param name (str): node name
        :param ntype (str): node type (e.g., module, callsite)
        :return idx (int)
        """
        if ntype == "callsite":
            return self.callsite2idx[name]
        if ntype == "module":
            return self.module2idx[name]
        assert 0
    
