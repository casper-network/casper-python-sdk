import enum


class TagOfRequestType(enum.Enum):
    Get = 0
    TryAcceptTransaction = 1
    TrySpeculativeExec = 2


class TagOfRequestTypeGet(enum.Enum):
    Record = 0;
    Information = 1;
    State = 2;


class TagOfRequestTypeGetInformation(enum.Enum):
    BlockHeader = 0
    SignedBlock = 1
    Transaction = 2
    Peers = 3
    Uptime = 4
    LastProgress = 5
    ReactorState = 6
    NetworkName = 7
    ConsensusValidatorChanges = 8
    BlockSynchronizerStatus = 9
    AvailableBlockRange = 10
    NextUpgrade = 11
    ConsensusStatus = 12
    ChainspecRawBytes = 13
    NodeStatus = 14
    LatestSwitchBlockHeader = 15
    Reward = 16


class TagOfRequestTypeGetRecord(enum.Enum):
    BlockHeader = 0
    BlockBody = 1
    ApprovalsHashes = 2
    BlockMetadata = 3
    Transaction = 4
    ExecutionResult = 5
    Transfer = 6
    FinalizedTransactionApprovals = 7


class TagOfRequestTypeGetState(enum.Enum):
    Item = 0
    AllItems = 1
    Trie = 2
    DictionaryItem = 3
    Balance = 4
    ItemsByPrefix = 5
