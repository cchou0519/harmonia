import os
# ====== zone of config =====
ff = open('number of edges', 'r')
temp = ff.readline()
ff.close()
edgeNum = int(temp)
# ====== zone of config =====

if edgeNum < 1:
    edgeNum = 1

# create aggregator.yml
text = 'type: aggregator\nnotification:\n  type: push\n  stewardServerURI: ":9080"\n' \
    'operatorGrpcServerURI: operator:8787\nappGrpcServerURI: app:7878\ngitUserToken: 1qaz_WSX\n' \
    'aggregatorModelRepo:\n  gitHttpURL: http://aggregator@gitea:3000/gitea/global-model.git\n' \
    'edgeModelRepos:\n'
for i in range(1, edgeNum+1):
    text += '  - gitHttpURL: http://aggregator@gitea:3000/gitea/local-model' + str(i) + '.git\n'
text += 'trainPlanRepo:\n  gitHttpURL: http://aggregator@gitea:3000/gitea/train-plan.git'

os.system('mkdir aggregator')
f = open('aggregator/config.yml', 'w')
f.write(text)
f.close()

for i in range(1, edgeNum+1):
    # create edges folder
    os.system('mkdir edge' + str(i))

    # create edge config.yml
    text = 'type: edge\n' \
           'notification:\n  type: push\n  stewardServerURI: ":9080"\n' \
           'operatorGrpcServerURI: operator:8787\n' \
           'appGrpcServerURI: app:7878\n' \
           'gitUserToken: 1qaz_WSX\n' \
           'aggregatorModelRepo:\n' \
           '  gitHttpURL: http://edge1@gitea:3000/gitea/global-model.git\n' \
           'edgeModelRepo:\n  ' \
           'gitHttpURL: http://edge1@gitea:3000/gitea/local-model' + str(i) + '.git\n' \
           'trainPlanRepo:\n' \
           '  gitHttpURL: http://edge1@gitea:3000/gitea/train-plan.git'
    f = open('edge' + str(i) + '/config.yml', 'w')
    f.write(text)
    f.close()

    # create edge docker-compose.yml
    text = 'version: "3.7"\nservices:\n  app:\n    image: mnist_edge\n    environment:\n' \
           '      OPERATOR_URI: operator:8787\n    volumes:\n      - type: volume\n' \
           '        source: shared\n        target: /repos\n  operator:\n' \
           '    image: harmonia/operator\n    volumes:\n      - ./config.yml:/app/config.yml\n' \
           '      - type: volume\n        source: shared\n        target: /repos\n' \
           '    networks:\n      mnist:\n        aliases:\n          - edge1\n      default:\n' \
           'networks:\n  mnist:\n    external:\n      name: mnist\nvolumes:\n  shared:'
    f = open('edge' + str(i) + '/docker-compose.yml', 'w')
    f.write(text)
    f.close()

# create logserver config.yml
text = 'stewardServerURI: "0.0.0.0:9080"\ngitUserToken: 1qaz_WSX\n' \
       'tensorboardDataRootDir: /tensorboard_data\nmodelRepos:\n' \
       '  - gitHttpURL: http://logserver@gitea:3000/gitea/global-model.git\n'
for i in range(1, edgeNum+1):
    text += '  - gitHttpURL: http://logserver@gitea:3000/gitea/local-model' + str(i) + '.git\n'

os.system('mkdir logserver')
f = open('logserver/config.yml', 'w')
f.write(text)
f.close()

