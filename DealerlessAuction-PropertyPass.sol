// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DealerlessAuction {

    address public deployer;
    address payable public beneficiary;
    address public highestBidder;
    uint public highestBid;
    mapping (address => uint) public pendingReturns;
    bool public ended;

    event HighestBidIncreased(address bidder, uint amount);
    event AuctionEnded(address winner, uint amount);

    constructor(address payable _beneficiary) {
        deployer = msg.sender;
        beneficiary = _beneficiary;
    }

    function bid() external payable {
        require(msg.value > highestBid, "There already is a higher bid.");
        require(!ended, "auctionEnd has already been called.");

        if (highestBid != 0) {
            pendingReturns[highestBidder] += highestBid;
        }
        
        highestBidder = msg.sender;
        highestBid = msg.value;
        emit HighestBidIncreased(msg.sender, msg.value);
    }

    function withdraw() external returns (bool) {
        uint amount = pendingReturns[msg.sender];
        require(amount > 0, "No funds to withdraw.");

        pendingReturns[msg.sender] = 0;

        if (!payable(msg.sender).send(amount)) {
            pendingReturns[msg.sender] = amount;
            return false;
        }
        
        return true;
    }

    function pendingReturn(address _sender) external view returns (uint) {
        return pendingReturns[_sender];
    }

    function auctionEnd() external {
        require(!ended, "auctionEnd has already been called.");
        require(msg.sender == deployer, "You are not the auction deployer!");

        ended = true;
        emit AuctionEnded(highestBidder, highestBid);

        beneficiary.transfer(highestBid);
    }
}


// USAGE OF THE ABOVE CODE: 
//The provided Solidity code represents a smart contract designed for conducting a decentralized auction related to property purchases on the Ethereum blockchain. 
// This DealerlessAuction contract allows interested parties to place bids (bid function) on a property they intend to purchase. 
// The contract maintains crucial information such as the highest bid value and the address of the highest bidder,
// permitting participants to bid an amount higher than the current highest bid.
// Users have the option to withdraw their bid (withdraw function) if they're not the winning bidder. 
// The auction can be concluded by invoking the auctionEnd function, facilitating the transfer of the highest bid amount to the beneficiary designated for the property sale. 
// To ensure fairness and prevent potential vulnerabilities, the contract employs secure mechanisms against re-entry attacks and provides transparency by 
// allowing bidders to verify the pending amount available for withdrawal via the pendingReturn function. This smart contract serves as a secure and transparent
// platform for conducting property purchase auctions, fostering trust among potential buyers and ensuring a fair bidding process.