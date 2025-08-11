#include <iostream>
#include "mylib.h"  // 包含动态库头文件

int main() {
    int a = 5, b = 3;

    std::cout << "Addition: " << add(a, b) << std::endl;
    std::cout << "Multiplication: " << multiply(a, b) << std::endl;

    return 0;
}
