// SPDX-License-Indentifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private favoriteNumber;
    
    struct People {
        uint256 id;
        string name;
    }
    
    People[] public people;
    
    // mapping function
    mapping(string => uint256) public nameToId;

    function addPerson(uint256 _id, string memory _name) public {
        people.push(People({id: _id, name: _name}));
        nameToId[_name] = _id;
    }    
    
    function store(uint256 _favorateNumber) public returns(uint256) {
        favoriteNumber = _favorateNumber;
        return favoriteNumber;
    }
    
    // view, pure
    function retrieve_view() public view returns(uint256) {
        return favoriteNumber;
    }
    
    function retrieve_pure(uint256 _favoriteNumber) public pure returns(uint256) {
        return _favoriteNumber*2;
    }

    
}
