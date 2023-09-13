if __name__ == '__main__':
    # with open("standard.sbn.alp", "w", encoding="utf-8") as w:
    #     with open("standard.sbn", "r", encoding="utf-8") as f:
    #         data = f.readlines()
    #         for d in data:
    #             w.write(d.split("\t")[0].strip() + "\n")

    with open("standard.sbn.drs.out1", "w", encoding="utf-8") as w:
        with open("standard.sbn.drs.out", "r", encoding="utf-8") as f:
            data = f.readlines()
            for i in range(len(data)):
                if i % 2 == 0:
                    w.write(data[i])
