#!/bin/bash
export KUBECONFIG="/root/.kube/gcpconfig" #Cloud credentiallarını başka bir config dosyasında tutmak için Kubeconfig env variable'ını tanımlıyoruz.
#GKE credentiallarını alıyoruz.
gcloud container clusters get-credentials ${clustername} --zone europe-west3-c --project ${projectname} 
#proje'yi set ediyoruz.
gcloud config set project ${projectname} 
#önce açılmasını istediğim makinelerin hostnamelerine göre filtremele yapıp ilk olarak onları start ediyorum.
zkvmname=$(gcloud compute instances list --filter="STATUS:TERMINATED" --filter="name~'^.*${firststartingmachinename}.*'" --format="value(NAME)")
for name in $zkvmname; do echo $name; gcloud compute instances start $name --zone=${zone} ; done
#sonrasında daha öncesinde node'larını sıfıra çektiğim node poolların node sayılarını arttırıyorum.					
yes Y | gcloud container clusters resize ${clustername} --num-nodes=3 --node-pool ${nodepool1} --zone=${zone}
yes Y | gcloud container clusters resize ${clustername} --num-nodes=1 --node-pool ${nodepool2} --zone=${zone} 
sleep 15
#status'u terminated olan sunucuları start ediyorum.
vmname=$(gcloud compute instances list --filter="STATUS:TERMINATED" --format="value(NAME)")
for name in $vmname; do echo $name; gcloud compute instances start $name --zone=${zone} ; done
unset KUBECONFIG
