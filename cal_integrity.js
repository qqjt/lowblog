const crypto = require('crypto');
const fs = require('fs');
const args = process.argv.slice(2);

function calculateSHA256(filePath) {
  const fileBuffer = fs.readFileSync(filePath);
  const hashSum = crypto.createHash('sha256');
  hashSum.update(fileBuffer);

  return hashSum.digest('hex');
}

const sha256Hash = calculateSHA256(args[0]);
console.log(`SHA-256: ${sha256Hash}`);

function hexToBase64(hexString) {
  const byteArray = Buffer.from(hexString, 'hex');
  return byteArray.toString('base64');
}

const base64Hash = hexToBase64(sha256Hash);
console.log(`Base64 Encoded SHA-256: ${base64Hash}`);