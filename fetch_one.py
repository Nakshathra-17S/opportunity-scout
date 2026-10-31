import sys, json
from tinyfish import TinyFish

client = TinyFish()
url = sys.argv[1]
run = client.agent.run(
    url=url,
    goal="List the first 5 opportunities with name, deadline, prize and link. Return JSON.",
)
host = url.split("//")[1].split("/")[0]
with open("raw_" + host + ".txt", "w", encoding="utf-8") as f:
    f.write(repr(run.result))
print("RESULT_JSON:" + json.dumps(run.result, default=str))