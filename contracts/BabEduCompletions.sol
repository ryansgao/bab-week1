// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

/// @title Blockchain at Berkeley education: completion records
/// @notice One public record per (wallet, week) for the six B@B education notebooks.
/// The record is a completion claim: answers are checked inside the notebook, not here.
/// It stores only the wallet address, the week number and the time. No names, no answers.
contract BabEduCompletions {
    /// @notice Emitted once per wallet per week.
    event Completed(address indexed learner, uint8 indexed week, uint256 timestamp);

    /// @notice Unix time a wallet recorded a week, or 0 if it has not.
    mapping(address => mapping(uint8 => uint256)) public completedAt;

    /// @notice Record that msg.sender finished `week` (1 to 6). Reverts if already recorded.
    function recordCompletion(uint8 week) external {
        require(week >= 1 && week <= 6, "week must be 1-6");
        require(completedAt[msg.sender][week] == 0, "already recorded");
        completedAt[msg.sender][week] = block.timestamp;
        emit Completed(msg.sender, week, block.timestamp);
    }
}
