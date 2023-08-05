def read_text_as_sentences(fp):
    with open(fp, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "": continue
            yield line
            # if "。" in line:
            #     lines = line.split("。")
            #     last_idx = len(lines) - 1
            #     for i, line in enumerate(lines):
            #         if i != last_idx: line += "。"
            #         if line == "": continue
            #         yield line
            # else:
                # yield line
