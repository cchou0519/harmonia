import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--edgeNum", help="number of edge", type=int, dest="edgeNum")
parser.add_argument("-imr", "--imageRegistry", help="your image registry", type=str, dest="imr")

cmd_args = parser.parse_args()

edgeNum = cmd_args.edgeNum
if edgeNum < 1:
    edgeNum = 1
imr = cmd_args.imr
# Aggregator
text = '# Aggregator\n' \
       'apiVersion: apps/v1\n' \
       'kind: Deployment\n' \
       'metadata:\n' \
       '  name: aggregator\n' \
       '  labels:\n' \
       '    app: aggregator\n' \
       'spec:\n' \
       '  replicas: 1\n' \
       '  selector:\n' \
       '    matchLabels:\n' \
       '      app: aggregator\n' \
       '  template:\n' \
       '    metadata:\n' \
       '      labels:\n' \
       '        app: aggregator\n' \
       '    spec:\n' \
       '      containers:\n' \
       '      - name: operator\n' \
       '        image: ' + imr + '/harmonia-operator\n' \
       '        imagePullPolicy: Always \n' \
       '        ports:\n' \
       '        - containerPort: 9080\n' \
       '          name: steward\n' \
       '        volumeMounts:\n' \
       '        - name: config\n' \
       '          mountPath: /app/config.yml\n' \
       '          subPath: aggregator-config.yml\n' \
       '        - name: shared-repos\n' \
       '          mountPath: /repos\n' \
       '      - name: application\n' \
       '        image: ' + imr + '/harmonia-fedavg\n' \
       '        imagePullPolicy: Always \n' \
       '        volumeMounts:\n' \
       '        - name: shared-repos\n' \
       '          mountPath: /repos\n' \
       '        - name: mnist-data\n' \
       '          mountPath: /mnist_data\n' \
       '      volumes:\n' \
       '      - name: mnist-data\n' \
       '        hostPath:\n' \
       '          path: /mnist_data/2Parties\n' \
       '          type: Directory\n' \
       '      - name: config\n' \
       '        configMap:\n' \
       '          name: aggregator-config\n' \
       '      - name: shared-repos\n' \
       '        emptyDir: {}\n' \
       '      nodeSelector:\n' \
       '        role: aggregator\n\n' \
       '---\n\n' \
       'kind: Service\n' \
       'apiVersion: v1\n' \
       'metadata:\n' \
       '  name: mnist-aggregator\n' \
       'spec:\n' \
       '  selector:\n' \
       '    app: aggregator\n' \
       '  ports:\n' \
       '  - name: aggregator\n' \
       '    port: 9080\n' \
       '    targetPort: 9080\n' \
       '  type: NodePort\n\n' \
       '---\n\n'

# Edges
for i in range(1, edgeNum+1):
    text += '# Edge' + str(i) + '\n' \
            'apiVersion: apps/v1\n' \
            'kind: Deployment\n' \
            'metadata:\n' \
            '  name: edge' + str(i) + '\n' \
            '  labels:\n' \
            '    app: edge' + str(i) + '\n' \
            'spec:\n' \
            '  replicas: 1\n' \
            '  selector:\n' \
            '    matchLabels:\n' \
            '      app: edge' + str(i) + '\n' \
            '  template:\n' \
            '    metadata:\n' \
            '      labels:\n' \
            '        app: edge' + str(i) + '\n' \
            '    spec:\n' \
            '      containers:\n' \
            '      - name: operator\n' \
            '        image: ' + imr + '/harmonia-operator\n' \
            '        imagePullPolicy: Always \n' \
            '        ports:\n' \
            '        - containerPort: 9080\n' \
            '          name: steward\n' \
            '        volumeMounts:\n' \
            '        - name: config\n' \
            '          mountPath: /app/config.yml\n' \
            '          subPath: edge-config.yml\n' \
            '        - name: shared-repos\n' \
            '          mountPath: /repos\n' \
            '      - name: application\n' \
            '        image: ' + imr + '/mnist_edge\n' \
            '        imagePullPolicy: Always \n' \
            '        volumeMounts:\n' \
            '        - name: shared-repos\n' \
            '          mountPath: /repos\n' \
            '        - name: mnist-data\n' \
            '          mountPath: /mnist_data\n' \
            '      volumes:\n' \
            '      - name: mnist-data\n' \
            '        hostPath:\n' \
            '          path: /mnist_data/' + str(edgeNum) + 'Parties/party' + str(i) + '\n' \
            '          type: Directory\n' \
            '      - name: config\n' \
            '        configMap:\n' \
            '          name: edge' + str(i) + '-config\n' \
            '      - name: shared-repos\n' \
            '        emptyDir: {}\n' \
            '      nodeSelector:\n' \
            '        role: edge' + str(i) + '\n\n' \
            '---\n\n' \
            'kind: Service\n' \
            'apiVersion: v1\n' \
            'metadata:\n' \
            '  name: mnist-edge' + str(i) + '\n' \
            'spec:\n' \
            '  selector:\n' \
            '    app: edge' + str(i) + '\n' \
            '  ports:\n' \
            '  - name: edge' + str(i) + '\n' \
            '    port: 9080\n' \
            '    targetPort: 9080\n' \
            '  type: NodePort\n\n' \
            '---\n\n'

# Logserver
text += '# Logserver\n' \
        'apiVersion: apps/v1\n' \
        'kind: Deployment\n' \
        'metadata:\n' \
        '  name: logserver\n' \
        '  labels:\n' \
        '    app: logserver\n' \
        'spec:\n' \
        '  replicas: 1\n' \
        '  selector:\n' \
        '    matchLabels:\n' \
        '      app: logserver\n' \
        '  template:\n' \
        '    metadata:\n' \
        '      labels:\n' \
        '        app: logserver\n' \
        '    spec:\n' \
        '      containers:\n' \
        '      - name: operator\n' \
        '        image: ' + imr + '/harmonia-logserver\n' \
        '        imagePullPolicy: Always \n' \
        '        ports:\n' \
        '        - containerPort: 9080\n' \
        '          name: logserver\n' \
        '        volumeMounts:\n' \
        '        - name: config\n' \
        '          mountPath: /app/config.yml\n' \
        '          subPath: logserver-config.yml\n' \
        '        - name: shared-tensorboard-data\n' \
        '          mountPath: /tensorboard_data\n' \
        '      - name: tensorboard\n' \
        '        image: tensorflow/tensorflow\n' \
        '        ports:\n' \
        '        - containerPort: 6006\n' \
        '          name: tensorboard\n' \
        '        volumeMounts:\n' \
        '        - name: shared-tensorboard-data\n' \
        '          mountPath: /tensorboard_data\n' \
        '        command: ["tensorboard"]\n' \
        '        args: ["--logdir=/tensorboard_data", "--bind_all"]\n' \
        '      volumes:\n' \
        '      - name: config\n' \
        '        configMap:\n' \
        '          name: logserver-config\n' \
        '      - name: shared-tensorboard-data\n' \
        '        emptyDir: {}\n' \
        '      nodeSelector:\n' \
        '        role: aggregator\n\n' \
        '---\n\n' \
        'kind: Service\n' \
        'apiVersion: v1\n' \
        'metadata:\n' \
        '  name: logserver\n' \
        'spec:\n' \
        '  selector:\n' \
        '    app: logserver\n' \
        '  ports:\n' \
        '  - name: logserver\n' \
        '    port: 9080\n' \
        '    targetPort: 9080\n' \
        '  - name: tensorboard\n' \
        '    port: 6006\n' \
        '    targetPort: 6006\n' \
        '  type: NodePort'

f = open('mnist-deployment.yml', 'w')
f.write(text)
f.close()
print('create mnist-deployment.yml success!')
