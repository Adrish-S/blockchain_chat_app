pragma solidity ^0.8.0;

contract DecentralizedChat {
    struct Message {
        address sender;
        string content;
        uint timestamp;
    }
    
    mapping(uint => Message) public messages;
    uint public messageCount;

    event MessageSent(address sender, string content, uint timestamp);

    function sendMessage(string memory _content) public {
        messages[messageCount] = Message(msg.sender, _content, block.timestamp);
        messageCount++;
        emit MessageSent(msg.sender, _content, block.timestamp);
    }
}
