import struct
from app.utils.helpers import left_rotate
from app.config.database import mongodb
from app.responses.hash import Sha1HashItem
from fastapi import HTTPException


async def create_hash(data):
    original_message = data.message  # Extract the message from the request body
    if isinstance(original_message, str):
        data = original_message.encode()  # Convert to bytes if it's a string

    # Initialize variables:
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Pre-processing:
    original_byte_len = len(data)
    original_bit_len = original_byte_len * 8
    data += b'\x80'  # Append a single '1' bit
    while (len(data) + 8) % 64 != 0:
        data += b'\x00'  # Pad with '0' bits

    data += struct.pack('>Q', original_bit_len)

    # Process the message in successive 512-bit chunks:
    for i in range(0, len(data), 64):
        chunk = data[i:i+64]
        w = list(struct.unpack('>16L', chunk)) + [0]*64

        for j in range(16, 80):
            w[j] = left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)

        a, b, c, d, e = h0, h1, h2, h3, h4

        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + w[j]) & 0xffffffff
            a, b, c, d, e = temp, a, left_rotate(b, 30), c, d

        # Add this chunk's hash to result so far:
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    hashed_data = '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)
    collection = mongodb["hashes"]
    result = await collection.insert_one({
        "original_message": original_message,
        "hash": hashed_data
    })

    if (not result.acknowledged):
        raise HTTPException(status_code=500, detail="Failed to save hash to database")
    if (result.acknowledged):
        print("Hash saved to database successfully")
    return {
        "hash": hashed_data,
        "original_message": original_message,
        "success": 'Successfully saved to the database',
    }



# Controller function
async def get_hash():
    collection = mongodb["hashes"]
    hashes = await collection.find().to_list(length=100)
    if not hashes:
        raise HTTPException(status_code=404, detail="No hashes found")

    hashes_list = [
        Sha1HashItem(
            hashes_message=hash['hash'],
            original_message=hash['original_message'],
            id=str(hash['_id'])
        )
        for hash in hashes
    ]

    
    return {
        "hashes": hashes_list,
        "success": 'Successfully fetched from the database',
    }