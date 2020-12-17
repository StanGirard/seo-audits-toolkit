
import subprocess
string="echo Hello world"
proc=subprocess.Popen("lighthouse --chrome-flags='--headless' https://primates.dev --output json", stdout=subprocess.PIPE, shell=True)
result = proc.stdout.read().decode("utf-8") 
print("result::: ",result)

f = open("results.json", "w")
f.write(result)
f.close()