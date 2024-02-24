##I used this documentation to come up with a little script https://github.com/kubernetes-client/python

from kubernetes import client, config
import yaml

def create_or_update_configmap(configmap_name, namespace, config_file_path):
    config.load_kube_config()
    v1 = client.Corev1()

    #Read configuration
    with open(config_file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    config_map = client.V1ConfigMap(
        metadata=client.V1ObjectMeta(name=configmap_name),
        data=config_data
    )

    try:
        # Try to create the ConfigMap
        api_response = v1.create_namespaced_config_map(namespace, config_map)
        print("ConfigMap created successfully.")
    except client.rest.ApiException as e:
        if e.status == 409:
            # ConfigMap already exists; 
            api_response = v1.replace_namespaced_config_map(configmap_name, namespace, config_map)
            print("ConfigMap updated successfully.")
        else:
            print(f"Error updatin ConfigMap: {e}")

if __name__ == "__main__":
    configmap_name = "test-configmap"
    namespace = "default"
    config_file_path = "config.yaml"
    create_or_update_configmap(configmap_name, namespace, config_file_path)
