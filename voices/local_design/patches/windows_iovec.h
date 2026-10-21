#pragma once
#include <cstddef>
#ifdef _WIN32
// The upstream Windows read path uses this POSIX data layout but omits its
// declaration. No POSIX readv syscall is used on Windows.
struct iovec {
    void *iov_base;
    std::size_t iov_len;
};
#endif
