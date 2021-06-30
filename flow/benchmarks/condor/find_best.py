import sys

base_dir = sys.argv[1]
gen = int(sys.argv[2])
genSize = int(sys.argv[3])

value_str = 'value_{}_i_{}.txt'
params_str = 'params_{}_i_{}.txt'


m_value = float('-inf')
m_index = 0

for i in range(genSize):
    try:
        with open(base_dir+'/' + value_str.format(gen, i)) as f:
            value = float(f.read())
            if value > m_value:
                m_index = i
                m_value = value
    except:
        print("could not find file")

with open(base_dir + '/' + params_str.format(gen, m_index)) as f:
    params = f.read()


print(m_index)
print(params, m_value)


