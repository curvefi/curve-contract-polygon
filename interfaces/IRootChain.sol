pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

interface IRootChain {
    struct Tuple1 {
        bytes32 root;
        uint256 start;
        uint256 end;
        uint256 createdAt;
        address proposer;
    }

    function currentHeaderBlock() external view returns (uint256);

    function getLastChildBlock() external view returns (uint256);

    function headerBlocks(uint256 _arg0) external view returns (Tuple1 memory);
}
