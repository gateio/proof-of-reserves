var fs = require('fs');
var path = require('path');
var crypto = require('crypto');
const { MerkleTree } = require('merkletreejs');
const SHA256 = require('crypto-js/sha256');
const LEAVES_HASH_LEN = 16;
const DELIMITER = '\t';
const NEW_LINE = '\r\n';

let rawFile, merkleFile;
/**
 * interaction between HTML and js code
 */
$(function() {
	let TXT, VerifyTXT;
	// create Merkle tree with user inpur of a list of (userId, userBalance)
	$('.getMerkleTxtBox .btn').click(function() {
		createMerkle(TXT, rawFile);
	});

	// upload leave nodes of the Merkle tree
	$('.upLoadTxt').change(function(event) {
		var files = event.target.files;
		rawFile = files[0].name;
		var input = event.target;
		var reader = new FileReader();
		reader.onload = function() {
			if (reader.result) {
				// retrieve file content
				TXT = reader.result;
			}
		};
		reader.readAsText(input.files[0]);
	});

	// verify user input of (userId, userBalance) within the Merkle tree that constructed by the given leaf nodes
	$('.verifyBox .btn').click(function() {
		let obj = {
			uid: $('.upLoadTxtUid').val(),
			balance: $('.upLoadTxtBan').val(),
			rootHash: $('.upLoadTxtRootHash').val(),
			url: merkleFile,
		};
		verifyMerkle(VerifyTXT, obj);
	});

	// upload leaf nodes of the Merkle tree for verification
	$('.upLoadMerkle').change(function(event) {
		var files = event.target.files;
		merkleFile = files[0].name;
		var input = event.target;
		var reader = new FileReader();
		reader.onload = function() {
			if (reader.result) {
				// retrieve file content
				VerifyTXT = reader.result;
			}
		};
		reader.readAsText(input.files[0]);
	});
});

/**
 * convert given string into hex format
 * @param value
 * @returns {string}
 */
function bufferToString(value) {
	return value.toString('hex');
}

/**
 * build Merkle tree using input data, and save the data of leaf nodes in resTxt
 * @method merkle
 * @param {String} UserBalance content of input file
 * @param {String} name name of input file
 * @return {JSON} root userNums totalBalance
 */
function createMerkle(UserBalance, fileName) {
	if (!fileName || !UserBalance) {
		alert('Please choose a file with valid user balances!');
		return;
	}

	// process input file
	const content = UserBalance;
	var list = content.split(NEW_LINE); // read UID and balance from input file
	var balances_hash = [];
	var total_balance = 0;
	for (var i = 0; i < list.length; i++) {
		var row = list[i];
		if (row[0] == '#') continue;
		var data = row.split(',');
		if (data.length != 2) continue;
		var uid = data[0];
		var balance = data[1];
		total_balance += balance * 1; // calculate total balance

		//concatenate hashed uid and balance to form transaction data
		var uid_hash = SHA256(uid);
		var balance_hash = SHA256(balance);
		balances_hash.push(uid_hash + balance_hash); // underlying data to build Merkle tree

		if (i % 10000 == 0) {
			console.log("users:" + i + "; balances:" + total_balance);
		}
	}

	console.log('number of balances hash: ' + balances_hash.length);
	// construct leaves and shorten hashed value in leaves
	const leaves = balances_hash.map(x =>
		SHA256(x)
			.toString()
			.substring(0, LEAVES_HASH_LEN)
	);
	// build Merlke tree
	const tree = new MerkleTree(leaves, SHA256);

	let treeLevels = tree.getLayers().length;
	let leavesFromTree = tree.getLeaves();
	let output = 'Level' + DELIMITER + 'Hash' + NEW_LINE;
	for (let i = 0; i < leavesFromTree.length; i++) {
		// write only the leaf nodes of the Merkle tree into verification file, all letters in lower case
		output +=
			treeLevels +
			',' +
			i.toString() +
			DELIMITER +
			// shorten hashed value in leaves
			bufferToString(leavesFromTree[i]) +
			NEW_LINE;
	}
	console.log('Merkle tree complete');
	
	// save the Merkle tree data as verify file
	let resFileName = fileName.split('.')[0];
	resFileName += '_merkletree.txt';
	let file = new File([output], resFileName, { type: 'text/plain;charset=utf-8' });
	saveAs(file);

	$('.rootHash').html(bufferToString(tree.getRoot()));
	$('.userNums').html(leavesFromTree.length);
	$('.totalBalance').html(total_balance);
}

/**
 * validate user balance
 *
 * @method merkle
 * @param {String} VerifyTXT verification file with all hashed value
 * @param {String} params  containing a pair of (uid and balance) to be verified
 * @return {JSON} checkRes (validation result, boolean)  nodesLocation（location of user node） {"checkRes":true,"nodesLocation":"4,0"}
 */

function verifyMerkle(VerifyTXT, params) {
	if (!VerifyTXT) {
		alert('Please choose a file with valid content!');
		return;
	}
	if (!params.uid || !params.balance) {
		alert('Please input uid and balance for verification');
		return;
	}

	// compute the hashed value with given uid and balance
	let uid = params.uid;
	let balance = params.balance;
	var uid_hash = SHA256(uid);
	var balance_hash = SHA256(balance);
	let leafStr = SHA256(uid_hash + balance_hash)
		.toString()
		.substring(0, LEAVES_HASH_LEN);

	// process input value
	var content = VerifyTXT;
	var list = content.split(NEW_LINE);
	list.splice(0, 1); // remove header row
	let leaves = [];
	let nodesLocation = undefined;
	for (var i = 0; i < list.length; i++) {
		var l = list[i];
		if (l[0] == '#') continue;
		var c = l.split('\t');
		if (c.length != 2) continue;
		var hash = c[1].trim();
		leaves.push(hash);
		if (leafStr === hash) {
			nodesLocation = i;
		}
	}
	if (nodesLocation == undefined) {
		alert('Could not find your information in the Merkle Tree.');
		return;
	}

	// start Merkle tree verification
	let options = {
		hashLeaves: false,
	};

	// construct Merkle tree without hashing the leaves
	const tree = new MerkleTree(leaves, SHA256, options);
	const root = bufferToString(tree.getRoot());
	$('.computedRootHash').html(root);

	const proof = tree.getProof(leafStr);

	let depth = tree.getLayers().length;
	let resObj = {
		checkRes: tree.verify(proof, leafStr, root),
		level: depth.toString(),
		position: nodesLocation.toString(),
	};
	if (resObj.checkRes) {
		$('.result').html(
			'Successful! Found your information in the Merkle Tree at Level: ' +
				resObj.level +
				', Position: ' +
				resObj.position
		);
	} else {
		$('.result').html('Could not find your information in the Merkle Tree.');
	}
}
