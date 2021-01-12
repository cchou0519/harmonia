# ====== zone of config =====
ff = open('number of edges', 'r')
edgeNum = int(ff.readline())
ff.close()
# ====== zone of config =====

if edgeNum < 1:
    edgeNum = 1

# Create admin
# Create users
text = '# Create admin\n\n' \
       'gitea admin user create --admin --username gitea --password password --email admin@admin.com\n\n' \
       '# Create users\n\n' \
       'gitea admin user create --username aggregator --password 1qaz_WSX --email aggregator@aggregator.com --must-change-password=false\n\n' \
       'gitea admin user create --username logserver --password 1qaz_WSX --email logserver@logserver.com --must-change-password=false\n\n'

for i in range(1, edgeNum+1):
    text += 'gitea admin user create --username edge{num} --password 1qaz_WSX --email edge{num}@edge{num}.com --must-change-password=false\n\n'.format(num=i)

# Create repositories
text += '# Create repositories\n\n' \
        'curl -X POST -H "accept: application/json" -H "Content-Type: application/json" -d \'{"name": "train-plan", "auto_init": true}\' ' \
        'http://gitea:password@127.0.0.1:3000/api/v1/user/repos\n\n' \
        'curl -X POST -H "accept: application/json" -H "Content-Type: application/json" -d \'{"name": "global-model", "auto_init": true}\' ' \
        'http://gitea:password@127.0.0.1:3000/api/v1/user/repos\n\n'

for i in range(1, edgeNum+1):
    text += 'curl -X POST -H "accept: application/json" -H "Content-Type: application/json" -d \'{"name": "local-model' \
            + str(i) + '", "auto_init": true}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/user/repos\n\n'


# Create permissions
# train-plan
text += '# Create permissions\n\n' \
        '# train-plan\n\ncurl -X PUT -H "accept: application/json" -H "Content-Type: application/json" -d \'{"permission": "read"}\' ' \
        'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/train-plan/collaborators/aggregator\n\n'
for i in range(1, edgeNum+1):
    text += 'curl -X PUT -H "accept: application/json" -H "Content-Type: application/json" -d \'{"permission": "read"}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/train-plan/collaborators/edge' + str(i) + '\n\n'


# global-model
text += '# global-model\n\ncurl -X PUT -H "accept: application/json" -H "Content-Type: application/json" -d \'{"permission": "write"}\' ' \
        'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/global-model/collaborators/aggregator\n\n' \
        'curl -X PUT -H "accept: application/json" -H "Content-Type: application/json" -d \'{"permission": "read"}\' ' \
        'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/global-model/collaborators/logserver\n\n'
for i in range(1, edgeNum+1):
    text += 'curl -X PUT -H "accept: application/json" -H "Content-Type: application/json" -d \'{"permission": "read"}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/global-model/collaborators/edge' + str(i) + '\n\n'

# local-models
for i in range(1, edgeNum+1):
    text += '# local-model' + str(i) + '\n\n' \
            'curl -X PUT -H "accept: application/json" -H "Content-Type: application/json" -d \'{"permission": "read"}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/local-model' + str(i) + '/collaborators/aggregator\n\n' \
            'curl -X PUT -H "accept: application/json" -H "Content-Type: application/json" -d \'{"permission": "write"}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/local-model' + str(i) + '/collaborators/edge' + str(i) + '\n\n' \
            'curl -X PUT -H "accept: application/json" -H "Content-Type: application/json" -d \'{"permission": "read"}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/local-model' + str(i) + '/collaborators/logserver\n\n'

# Create webhooks
# train-plan
text += '# Create webhooks\n\n# train-plan\n\n' \
        'curl -X POST -H "accept: application/json" -H "Content-Type: application/json" ' \
        '-d \'{"active": true, "config": {"content_type": "json", "url": "http://aggregator:9080"}, "events": ["push"], "type": "gitea"}\' ' \
        'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/train-plan/hooks\n\n'
for i in range(1, edgeNum+1):
    text += 'curl -X POST -H "accept: application/json" -H "Content-Type: application/json" ' \
            '-d \'{"active": true, "config": {"content_type": "json", "url": "http://edge' + str(i) + ':9080"}, "events": ["push"], "type": "gitea"}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/train-plan/hooks\n\n'

# global-model
text += '# global-model\n\n' \
        'curl -X POST -H "accept: application/json" ' \
        '-H "Content-Type: application/json" ' \
        '-d \'{"active": true, "config": {"content_type": "json", "url": "http://logserver:9080"}, "events": ["push"], "type": "gitea"}\' ' \
        'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/global-model/hooks\n\n'

for i in range(1, edgeNum+1):
    text += 'curl -X POST ' \
            '-H "accept: application/json" ' \
            '-H "Content-Type: application/json" ' \
            '-d \'{"active": true, "config": {"content_type": "json", "url": "http://edge' + str(i) + ':9080"}, "events": ["push"], "type": "gitea"}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/global-model/hooks\n\n'

# local-models
for i in range(1, edgeNum+1):
    text += '# local-model' + str(i) + '\n\n' \
            'curl -X POST ' \
            '-H "accept: application/json" ' \
            '-H "Content-Type: application/json" ' \
            '-d \'{"active": true, "config": {"content_type": "json", "url": "http://aggregator:9080"}, "events": ["push"], "type": "gitea"}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/local-model' + str(i) + '/hooks\n\n' \
            'curl -X POST ' \
            '-H "accept: application/json" ' \
            '-H "Content-Type: application/json" ' \
            '-d \'{"active": true, "config": {"content_type": "json", "url": "http://logserver:9080"}, "events": ["push"], "type": "gitea"}\' ' \
            'http://gitea:password@127.0.0.1:3000/api/v1/repos/gitea/local-model' + str(i) + '/hooks\n\n'

# print(text)

f = open('custom_gitea_setup.sh', 'w')
f.write(text)
f.close()
