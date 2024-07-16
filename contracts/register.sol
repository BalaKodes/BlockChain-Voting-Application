// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {
  string[] _names;
  string[] _adhars;
  string[] _mobiles;
  string[] _dobs;
  string[] _states;
  string[] _districts;
  string[] _pincodes;
  uint[] _statuses;

  mapping(string=>bool) _users;

  function addUser(string memory name,string memory adhar,string memory mobile,string memory dob,string memory state,string memory district,string memory pincode) public {
    require(!_users[adhar]);
    _names.push(name);
    _adhars.push(adhar);
    _mobiles.push(mobile);
    _dobs.push(dob);
    _states.push(state);
    _districts.push(district);
    _pincodes.push(pincode);
    _statuses.push(0);
    _users[adhar]=true;
  }

  function validateUser(string memory adhar,uint status) public {
    uint i;

    for(i=0;i<_adhars.length;i++){
      if(keccak256(abi.encodePacked(adhar)) == keccak256(abi.encodePacked(_adhars[i]))){
        _statuses[i]=status;
      }
    }
  }

  function viewUsers() public view returns(string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,uint[] memory) {
    return(_names,_adhars,_mobiles,_dobs,_states,_districts,_pincodes,_statuses);
  }
}
