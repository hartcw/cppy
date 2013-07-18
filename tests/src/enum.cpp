#include "enum.h"
#include <cstring>

#py lines = open('values.txt').read().splitlines()

example_t
str_to_example(const char *str)
{
    if (str == NULL) return EXAMPLE_Unknown;
    #py \
    for line in lines: \
        print('if (std::strcmp(str, "' + line + '") == 0) return EXAMPLE_' + line + ';')

    return EXAMPLE_Unknown;
}

const char *
example_to_string(example_t e)
{
    static const char *map[] =
    {
        /* py
        for line in lines:
            print('"' + line + '",')
        */
    };

    if (e >= 0 && e < EXAMPLE_Max)
        return map[e];

    return "Unknown";
}
