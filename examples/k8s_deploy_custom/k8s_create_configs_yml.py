# ====== zone of config =====
ff = open('number of edges', 'r')
temp = ff.readline()
ff.close()
edgeNum = int(temp)
# ====== zone of config =====

if edgeNum < 1:
    edgeNum = 1

local_ip = 'harmonia-gitea'

# create aggregator config
text = 'apiVersion: v1\n' \
       'kind: ConfigMap\n' \
       'metadata:\n' \
       '  name: aggregator-config\n' \
       'data:\n' \
       '  aggregator-config.yml: |\n' \
       '    type: aggregator\n' \
       '    notification:\n' \
       '      type: push\n' \
       '    gitUserToken: 1qaz_WSX\n' \
       '    aggregatorModelRepo:\n' \
       '      gitHttpURL: http://aggregator@'+local_ip+':3000/gitea/global-model.git\n' \
       '    edgeModelRepos:\n'

for i in range(1, edgeNum+1):
    text += '      - gitHttpURL: http://aggregator@'+local_ip+':3000/gitea/local-model' + str(i) + '.git\n'
text += '    trainPlanRepo:\n' \
        '      gitHttpURL: http://aggregator@'+local_ip+':3000/gitea/train-plan.git\n\n---\n\n'

# create logserver config
text += 'apiVersion: v1\n' \
        'kind: ConfigMap\n' \
        'metadata:\n' \
        '  name: logserver-config\n' \
        'data:\n' \
        '  logserver-config.yml: |\n' \
        '    stewardServerURI: "0.0.0.0:9080"\n' \
        '    gitUserToken: 1qaz_WSX\n' \
        '    tensorboardDataRootDir: /tensorboard_data\n' \
        '    modelRepos:\n' \
        '      - gitHttpURL: http://logserver@'+local_ip+':3000/gitea/global-model.git\n'

for i in range(1, edgeNum+1):
    text += '      - gitHttpURL: http://logserver@'+local_ip+':3000/gitea/local-model' + str(i) + '.git\n'

for i in range(1, edgeNum+1):
    text += '\n---\n\n' \
            'apiVersion: v1\n' \
            'kind: ConfigMap\n' \
            'metadata:\n' \
            '  name: edge' + str(i) + '-config\n' \
            'data:\n' \
            '  edge-config.yml: |\n' \
            '    type: edge\n' \
            '    notification:\n' \
            '      type: push\n' \
            '    gitUserToken: 1qaz_WSX\n' \
            '    aggregatorModelRepo:\n' \
            '      gitHttpURL: http://edge' + str(i) + '@'+local_ip+':3000/gitea/global-model.git\n' \
            '    edgeModelRepo:\n' \
            '      gitHttpURL: http://edge' + str(i) + '@'+local_ip+':3000/gitea/local-model' + str(i) + '.git\n' \
            '    trainPlanRepo:\n' \
            '      gitHttpURL: http://edge' + str(i) + '@'+local_ip+':3000/gitea/train-plan.git\n'

f = open('configs.yml', 'w')
f.write(text)
f.close()





