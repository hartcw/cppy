#ifndef ENUM_H
#define ENUM_H

enum example_t
{
    #py \
    for line in open('values.txt'): \
        print('EXAMPLE_' + line.strip() + ',')
    EXAMPLE_Max,
    EXAMPLE_Unknown
};

example_t str_to_example(const char *str);

const char * example_to_str(example_t e);

#endif // ENUM_H
