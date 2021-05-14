#!/bin/bash
export KUBECONFIG="/root/.kube/gcpconfig" #Cloud credentiallarını başka bir config dosyasında tutmak için Kubeconfig env variable'ını tanımlıyoruz.
#GKE credentiallarını alıyoruz.
gcloud container clusters get-credentials ${clustername} --zone ${zone}  --project ${projectname} 
#proje'yi set ediyoruz.
gcloud config set project ${projectname} 
#önce node isimlerini alıp sonrasında onları cordon işlemi uygulayarak unschedulable olarak işaretliyoruz. Böylece node'lar üzerinde pod oluşumunu engellemiş oluyoruz.
#daha sonrada node-pool'ların node sayılarını sıfıra çekiyoruz.
nodename=$(kubectl get nodes -o=custom-columns=NAME:.metadata.name | grep -v NAME)
for name in $nodename; do kubectl cordon $name;   done
yes Y | gcloud container clusters resize ${clustername} --num-nodes=0 --node-pool ${nodepool1} --zone=${zone}
yes Y | gcloud container clusters resize ${clustername} --num-nodes=0 --node-pool ${nodepool2} --zone=${zone} 
sleep 15
#Bu adımda da running olan tüm sunucuları kapatıyoruz.
vmname=$(gcloud compute instances list --filter="STATUS:RUNNING" --format="value(NAME)")
for name in $vmname; do echo $name; gcloud compute instances stop $name --zone=${zone}  ; done
#benim burda set ettiğim config dosyasını unset etmemin nedeni openshift üzerinde de işlem yapıyor olmamdır.
unset KUBECONFIG