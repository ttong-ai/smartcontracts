// contracts/OurToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract AntiMatterToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("AntiMatter", "AMU") {
        _mint(msg.sender, initialSupply);
    }
}
