İlk iş yerimde çalışırken uygulama paketlerinin kurulum testlerini manuel yapmak çok yorucu olduğu için jenkins job'ı üzerinden yapmaya karar vermiştim.
Bu süreçte basic olarak vmware tarafında kullandığım scriptleri bu dizin altına ekliyorum.

Burda şu şekilde bir akış vardı önce getvmid ile test için kullandığımız sunucunun vmid'sini vmwarehostu üzerinden komut ile alıp vmid dosyasına yazıyoruz.
Sonrasında vmid'yi dosyadan okuyarak snapshot id'sini alıyoruz (getsnapshotid).Bu id ile de ilgili snapshot'a geri dönüyoruz ki,istediğimiz paketi kurmak için vm'i hazırlayabilelim.

