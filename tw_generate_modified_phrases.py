__author__ = 'alisdair'

import itertools
import pprint

from tw_original_phrase_data import tw_original_phrases as p

def main():
    tangrams = itertools.product(("A","B"),(str(x) for x in range(1,13)))

    result = {}

    for tg_set, tg_number in tangrams:
        tangram = tg_set+tg_number
        for d in range(1,5):
            k = tangram+"_{}".format(d)
            result.update({
                k+"VF": "The first card is "+p[k],
                k+"VN": "The next card is "+p[k],
                k+"VZ": "The last card is "+p[k],
                k+"V": "It also looks like "+p[k],
                k+"TF": "First, "+p[k],
                k+"TN": "Next, "+p[k],
                k+"TZ": "Finally, "+p[k],
                k+"T": p[k],
                k+"Y": "Yes, "+p[k]

            })
    f = open("tw_descriptions.py","w")
    f.write("# Automatically generated by tw_generate_modified_phrases.py\n\n")
    f.write("tw_descriptions = {\n")
    def tg_tuple(x):
        tg, desc = x.split('_')
        card_set, card_number = tg[0], int(tg[1:])
        return card_set, card_number, desc

    def cmp0(a,b):
        return cmp(tg_tuple(a),tg_tuple(b))

    for k in sorted(result.keys(),cmp=cmp0):
        f.write("    '{}': '{}',\n".format(k,result[k]))
    f.write("}\n")

if __name__ == "__main__":
    main()