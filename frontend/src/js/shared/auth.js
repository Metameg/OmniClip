// Function to hash a string using SHA-256 algorithm
export async function sha256(str) {
    // Convert the string to a Uint8Array (byte array)
    const buffer = new TextEncoder().encode(str);

    // Use the crypto.subtle API to create a SHA-256 hash
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    // Convert the hash buffer to a hexadecimal string
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
    console.log(hashHex);
    return hashHex;
}
