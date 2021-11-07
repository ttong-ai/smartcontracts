// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {

    AggregatorV3Interface internal priceFeed;
    address public owner;
    address[] funders;
    
    constructor() {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
    }

    
    mapping(address => uint256) public addressToAmountFunded;
    
    function fund() public payable {
        // $50
        uint256 minimumUSD = 10;
        require(getConversionRate(msg.value) >= minimumUSD, "Need a min of $10 of ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function withdraw() payable onlyOwner public {
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++) {
            address funderAddress = funders[funderIndex];
            addressToAmountFunded[funderAddress] = 0;
        }
    }

    function getVersion() public view returns(uint256) {
        return priceFeed.version();
    }

    function getETHPrice() public view returns(uint256) {
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return uint256(price);
    }
    
    function getConversionRate(uint256 weiAmount) public view returns(uint256) {
        uint256 ethPrice = getETHPrice();
        uint256 ethAmountInUsd = (ethPrice * weiAmount) / 10**26;
        return ethAmountInUsd;
    }
    
    function getUSDValue() public view returns(uint256) {
        return getConversionRate(address(this).balance);
    }
}
