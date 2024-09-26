text = "file, file2, opt, rew"

print("\n".join([f"\t{k.strip()}".expandtabs(4) for k in text.split(",") if k]))

