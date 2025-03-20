from transformers import T5ForConditionalGeneration, T5Tokenizer

small_model = T5ForConditionalGeneration.from_pretrained("./models/MRN_NMT_T5_small", from_tf=False)
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# helper function
def translate(model, tokenizer, src: str):
  tok = tokenizer(src, return_tensors="pt").input_ids
  res = model.generate(tok)
  decoded = tokenizer.decode(res[0])
  return decoded[6:-4] # remove sos and eos

# Sample

# Maranao to English
maranao = "Anda ka song?" # edit inside " " to maranao phrase/sentence and run cell again
src = "translate Maranao to English: " + maranao
print(f"Maranao: {maranao}\n")

res = translate(small_model, tokenizer, src)
print("Small")
print(f"English: {res}")