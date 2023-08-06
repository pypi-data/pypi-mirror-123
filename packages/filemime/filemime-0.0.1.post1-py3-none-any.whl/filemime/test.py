from init import filemime

obj = filemime()

val = obj.load_file("./init.p")
print(val)

mime = obj.load_file("./init.py",mimeType=True)
print(mime)