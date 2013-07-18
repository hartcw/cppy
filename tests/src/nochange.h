#ifndef NOCHANGE_H
#define NOCHANGE_H

namespace test
{
#py value1 = 'this has no output'

struct test_t
{
    int value;
};
#py \
value2 = 'this has no output' \
value3 = 'this has no output'

}

#endif // NOCHANGE_H
