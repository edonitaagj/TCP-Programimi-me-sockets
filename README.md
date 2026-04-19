-> TCP Client-Server System me HTTP Monitoring
 Përshkrimi i projektit

Ky projekt implementon një sistem komunikimi Client-Server duke përdorur TCP sockets në Python. Serveri është në gjendje të menaxhojë disa klientë njëkohësisht, të kontrollojë aksesin në bazë të roleve dhe të ofrojë funksionalitete për manipulimin e file-ve në server.

Përveç komunikimit kryesor, projekti përfshin edhe një HTTP server të thjeshtë që punon paralelisht dhe mundëson monitorimin e gjendjes së serverit në kohë reale përmes një endpoint-i të dedikuar.

-> Funksionalitetet kryesore

1. Serveri pranon deri në katër klientë njëkohësisht dhe refuzon lidhjet e reja kur ky limit tejkalohet
2. Çdo klient autentikohet me ID dhe rol (admin ose user)
3. Lejohet vetëm një administrator në sistem
4. Serveri ruan dhe monitoron të gjitha mesazhet e klientëve
5. Implementohet timeout për klientët joaktivë dhe mbyllje automatike e lidhjes
6. Mbështet rikuperimin e sesionit kur klienti rilidhet
7. Diferencim i performancës: admin më i shpejtë, user me vonesë të vogël

-> HTTP Server për monitorim

1. Punon paralelisht me serverin TCP në një port të dytë
2. Ofron endpoint-in /stats për monitorim
3. Kthen të dhëna në format JSON
4. Përfshin numrin e lidhjeve aktive, mesazhet totale dhe klientët e lidhur
5. Ruajtja e statistikave bëhet në file-in stats.json

-> Funksionalitetet e klientit

1. Lidhet me serverin duke përdorur IP dhe portin përkatës
2. Rilidhet automatikisht nëse serveri është i fikur ose lidhja ndërpritet
3. Kryen autentikim me ID dhe rol
4. Dërgon mesazhe dhe komanda tek serveri
5. Lexon dhe shfaq përgjigjet nga serveri
6. Ruajnë file-t e shkarkuar në mënyrë lokale

-> Menaxhimi i file-ve

1. Admin ka qasje të plotë në file-t e serverit
2. Mund të listojë, lexojë, ngarkojë, shkarkojë dhe fshijë file
3. Mund të kërkojë file sipas fjalëve kyçe
4. Mund të shohë informacione si madhësia dhe data e krijimit
5. Të gjitha operacionet kryhen në folderin e serverit
6. User ka vetëm të drejtë leximi dhe nuk mund të modifikojë file

-> Menaxhimi i lidhjeve

1. Serveri përdor mekanizma për të menaxhuar shumë klientë njëkohësisht
2. Monitoron aktivitetin e klientëve në kohë reale
3. Mbyll lidhjet që janë idle për një periudhë të gjatë
4. Rikthen sesionin nëse klienti rilidhet me të njëjtin ID

-> Struktura e projektit

1. Serveri kryesor TCP
2. Klienti
3. HTTP server për monitorim
4. File për statistika (stats.json)
5. Folder për file-t e serverit

-> Testimi

1. Testuar me disa pajisje në një rrjet real
2. Testuar me shumë klientë paralelisht
3. Testuar timeout dhe rilidhje automatike
4. Testuar kufizimet e roleve dhe operacionet mbi file

-> Përfundim

1. Projekti demonstron përdorimin praktik të TCP sockets
2. Implementon menaxhim të shumë klientëve në mënyrë efikase
3. Ofron kontroll të aksesit bazuar në role
4. Integron monitorim në kohë reale përmes HTTP serverit
5. Përfshin mekanizma për stabilitet si timeout dhe reconnect
