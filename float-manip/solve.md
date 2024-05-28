the code is supposed to group the sign bits, exponent bits, and mantissa bits together.
oh yeah the floats come from the ascii values of the flag

I think this should solve the challenge but I haven't tested yet:
```cpp
void decodeFileToFloats(std::vector<float> &floats, std::string filename) {
    std::ifstream encodedFile(filename, std::ios::binary);

    // Get the size of the file
    encodedFile.seekg(0, std::ios::end);
    std::streamsize fileSize = encodedFile.tellg();
    encodedFile.seekg(0, std::ios::beg);

    // Read the bytes from the file into a vector
    std::vector<char> outputBytes(fileSize);
    encodedFile.read(outputBytes.data(), fileSize);
    encodedFile.close();
    int n = outputBytes.size() / 4;
    std::vector<char> floatBytes(4 * n);
    std::vector<bool> outputBits(32 * n);
    for (int i = 0; i < 4 * n; i++) {
        char c = outputBytes[i];
        for (int j = 0; j < 8; j++) {
            outputBits[8 * i + j] = (c & (0x80 >> j)) != 0;
        }
    }
    for (int i = 0; i < n; i++) {
        char byte1 = outputBits[i] << 7;
        for (int j = 0; j < 7; j++) {
            byte1 |= outputBits[n + 8 * i + j] << (6 - j);
        }
        char byte2 = outputBits[n + 8 * i + 7] << 7;
        for (int j = 0; j < 7; j++) {
            byte2 |= outputBits[n + 8 * n + 23 * i + j] << (6 - j);
        }
        char byte3 = 0;

        for (int j = 0; j < 8; j++) {
            byte3 |= outputBits[n + 8 * n + 23 * i + 7 + j] << (7 - j);
        }
        char byte4 = 0;
        for (int j = 0; j < 8; j++) {
            byte4 |= outputBits[n + 8 * n + 23 * i + 15 + j] << (7 - j);
        }
        floatBytes[4 * i] = byte1;
        floatBytes[4 * i + 1] = byte2;
        floatBytes[4 * i + 2] = byte3;
        floatBytes[4 * i + 3] = byte4;
    }
    for (int i = 0; i < n; i++) {
        float result;
        unsigned char *bytePtr = reinterpret_cast<unsigned char *>(&result);

        // Assuming bytes are stored in reverse order
        for (int j = 0; j < sizeof(float); j++) {
            bytePtr[sizeof(float) - 1 - j] = floatBytes[4 * i + j];
        }

        floats.push_back(result);
    }
}
```