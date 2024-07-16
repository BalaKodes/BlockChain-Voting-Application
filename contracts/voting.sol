// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract voting {
  
  uint[3] _votes=[0,0,0];

  mapping(string=>bool) _voters;


  function castVote(uint id,string memory adhar) public {
    require(!_voters[adhar]);
    if(id==0)
      _votes[0]++;
    else if(id==1)
      _votes[1]++;
    else if(id==2)
      _votes[2]++;
    _voters[adhar]=true;
  }

  function displayVotes() public view returns(uint[3] memory){
    return _votes;
  }
}
