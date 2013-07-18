#ifndef ENUM_H
#define ENUM_H

enum example_t
{
    EXAMPLE_Inactive,
    EXAMPLE_Loading,
    EXAMPLE_Ready,
    EXAMPLE_Pending,
    EXAMPLE_Running,
    EXAMPLE_Finished,
    EXAMPLE_Max,
    EXAMPLE_Unknown
};

example_t str_to_example(const char *str);

const char * example_to_str(example_t e);

#endif // ENUM_H
