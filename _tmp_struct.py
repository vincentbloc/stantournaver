import json,re,sys,glob
for f in sys.argv[1:]:
    p=json.load(open(f));print(f)
    print(re.findall(r'<(h2|ul class="\w+"|ol class="\w+"|div class="\w+"|table|p class="\w+")',p['body']))
    print([i['type'] for i in p['x']['imgs']], p['x'].get('scene'))
print([json.load(open(g))['slug'] for g in sorted(glob.glob('data/posts/*.json'))])
