#ifndef MYLIB_H
#define MYLIB_H

// 导出符号（跨平台兼容）
#ifdef _WIN32
#define MYLIB_EXPORT __declspec(dllexport)
#else
#define MYLIB_EXPORT
#endif

extern "C" {
    MYLIB_EXPORT int add(int a, int b);
    MYLIB_EXPORT int multiply(int a, int b);
}

#endif
