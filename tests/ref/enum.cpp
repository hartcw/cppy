#include "enum.h"
#include <cstring>



example_t
str_to_example(const char *str)
{
    if (str == NULL) return EXAMPLE_Unknown;
    if (std::strcmp(str, "Inactive") == 0) return EXAMPLE_Inactive;
    if (std::strcmp(str, "Loading") == 0) return EXAMPLE_Loading;
    if (std::strcmp(str, "Ready") == 0) return EXAMPLE_Ready;
    if (std::strcmp(str, "Pending") == 0) return EXAMPLE_Pending;
    if (std::strcmp(str, "Running") == 0) return EXAMPLE_Running;
    if (std::strcmp(str, "Finished") == 0) return EXAMPLE_Finished;

    return EXAMPLE_Unknown;
}

const char *
example_to_string(example_t e)
{
    static const char *map[] =
    {
        "Inactive",
        "Loading",
        "Ready",
        "Pending",
        "Running",
        "Finished",
    };

    if (e >= 0 && e < EXAMPLE_Max)
        return map[e];

    return "Unknown";
}
