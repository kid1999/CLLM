// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Oracle合约接口
interface IOracle {
    function requestData(string memory question, string memory source) external returns (uint256 requestId);
    function fulfillData(uint256 requestId, string memory result) external;
}

// 用户合约接口
interface ICallback {
    function oracleCallback(uint256 requestId, string memory result) external;
}

// Oracle合约实现
contract Oracle is IOracle {
    address public owner;
    mapping(uint256 => Request) public requests;
    uint256 private nextRequestId = 1;

    struct Request {
        address requester;
        string question;
        string source;
        bool fulfilled;
        address fulfiller; // 记录返回数据的节点地址
    }

    // 数据请求事件
    event DataRequested(
        uint256 indexed requestId,
        address indexed requester,
        string question,
        string source
    );

    // 数据响应事件
    event DataFulfilled(
        uint256 indexed requestId,
        string result,
        address indexed fulfiller
    );

    constructor() {
        owner = msg.sender;
    }

    // 用户请求数据的接口
    function requestData(string memory question, string memory source) 
        external 
        override 
        returns (uint256) 
    {
        uint256 requestId = nextRequestId++;
        
        requests[requestId] = Request({
            requester: msg.sender,
            question: question,
            source: source,
            fulfilled: false,
            fulfiller: address(0)
        });

        // 发出事件通知链下节点
        emit DataRequested(requestId, msg.sender, question, source);
        
        return requestId;
    }

    // 链下节点回传数据的接口
    function fulfillData(uint256 requestId, string memory result) 
        external 
        override 
    {
        require(!requests[requestId].fulfilled, "Request already fulfilled");
        
        requests[requestId].fulfilled = true;
        requests[requestId].fulfiller = msg.sender; // 记录调用者地址

        // 发出数据已回传的事件
        emit DataFulfilled(requestId, result, msg.sender);
        
        // 回调用户合约
        ICallback(requests[requestId].requester).oracleCallback(requestId, result);
    }
}

// 用户合约示例
contract UserContract is ICallback {
    IOracle public oracle;
    mapping(uint256 => string) public results;
    
    constructor(address _oracle) {
        oracle = IOracle(_oracle);
    }
    //生成请求ID
    event RequestCreated(uint256 requestId);
    //返回请求结果
    event ReturnResult(uint256 requestId,string result);

    // 请求LLM数据
    function requestLLM(string memory question, string memory source) external returns (uint256) {
        uint256 requestId = oracle.requestData(question, source);
        require(requestId > 0, "Invalid request ID returned.");
        emit RequestCreated(requestId);
        return requestId;
    }

    // Oracle回调接口
    function oracleCallback(uint256 requestId, string memory result)
        external
        override
    {
        require(msg.sender == address(oracle), "Only oracle can call this function");
        results[requestId] = result;

        // 这里处理返回的数据...
        processResult(requestId, result);
    }

    // 处理返回数据的内部函数
    function processResult(uint256 requestId, string memory result) internal {
        emit ReturnResult(requestId,result);

    }

    // 查询结果
    function getResult(uint256 requestId) external view returns (string memory) {
        string memory resultStr = results[requestId];
        return resultStr;
    }
}
