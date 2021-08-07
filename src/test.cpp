#include <iostream>
#include <string>
#include <unistd.h>

int main() {
    std::string test;
    std::cout << "Hello linux!\n";
    std::cin >> test;
    std::cout << test << std::endl;
    sleep(0xFFFFFFFF);
}