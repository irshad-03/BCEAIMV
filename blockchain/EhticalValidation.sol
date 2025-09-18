// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EthicalValidation {
    struct ValidationResult {
        string question;
        string aiAnswer;
        bool isTruthful;
        uint256 timestamp;
    }

    ValidationResult[] public validations;

    event ValidationLogged(string question, string aiAnswer, bool isTruthful, uint256 timestamp);

    function logValidation(string memory question, string memory aiAnswer, bool isTruthful) public {
        ValidationResult memory newResult = ValidationResult({
            question: question,
            aiAnswer: aiAnswer,
            isTruthful: isTruthful,
            timestamp: block.timestamp
        });

        validations.push(newResult);

        emit ValidationLogged(question, aiAnswer, isTruthful, block.timestamp);
    }

    function getValidation(uint index) public view returns (string memory, string memory, bool, uint256) {
        ValidationResult memory result = validations[index];
        return (result.question, result.aiAnswer, result.isTruthful, result.timestamp);
    }

    function getTotalValidations() public view returns (uint) {
        return validations.length;
    }
}
