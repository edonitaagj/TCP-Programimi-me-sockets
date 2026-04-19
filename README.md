📡 TCP Client-Server System me HTTP Monitoring
🧾 Përshkrimi i projektit

Ky projekt implementon një sistem komunikimi Client-Server duke përdorur TCP sockets në Python. Serveri është në gjendje të menaxhojë disa klientë njëkohësisht, të kontrollojë aksesin në bazë të roleve dhe të ofrojë funksionalitete për manipulimin e file-ve në server.

Përveç komunikimit kryesor, projekti përfshin edhe një HTTP server të thjeshtë që punon paralelisht dhe mundëson monitorimin e gjendjes së serverit në kohë reale përmes një endpoint-i të dedikuar.

✨ Funksionalitetet kryesore

🔹 Serveri pranon deri në katër klientë njëkohësisht dhe refuzon lidhjet e reja kur ky limit tejkalohet
🔹 Çdo klient autentikohet me ID dhe rol (admin ose user)
🔹 Lejohet vetëm një administrator në sistem
🔹 Serveri ruan dhe monitoron të gjitha mesazhet e klientëve
🔹 Implementohet timeout për klientët joaktivë dhe mbyllje automatike e lidhjes
🔹 Mbështet rikuperimin e sesionit kur klienti rilidhet
🔹 Diferencim i performancës: admin më i shpejtë, user me vonesë të vogël

🌐 HTTP Server për monitorim

🔹 Punon paralelisht me serverin TCP në një port të dytë
🔹 Ofron endpoint-in /stats për monitorim
🔹 Kthen të dhëna në format JSON
🔹 Përfshin numrin e lidhjeve aktive, mesazhet totale dhe klientët e lidhur
🔹 Ruajtja e statistikave bëhet në file-in stats.json

💻 Funksionalitetet e klientit

🔹 Lidhet me serverin duke përdorur IP dhe portin përkatës
🔹 Rilidhet automatikisht nëse serveri është i fikur ose lidhja ndërpritet
🔹 Kryen autentikim me ID dhe rol
🔹 Dërgon mesazhe dhe komanda tek serveri
🔹 Lexon dhe shfaq përgjigjet nga serveri
🔹 Ruajnë file-t e shkarkuar në mënyrë lokale

📂 Menaxhimi i file-ve

🔹 Admin ka qasje të plotë në file-t e serverit
🔹 Mund të listojë, lexojë, ngarkojë, shkarkojë dhe fshijë file
🔹 Mund të kërkojë file sipas fjalëve kyçe
🔹 Mund të shohë informacione si madhësia dhe data e krijimit
🔹 Të gjitha operacionet kryhen në folderin e serverit
🔹 User ka vetëm të drejtë leximi dhe nuk mund të modifikojë file

🔄 Menaxhimi i lidhjeve

🔹 Serveri përdor mekanizma për të menaxhuar shumë klientë njëkohësisht
🔹 Monitoron aktivitetin e klientëve në kohë reale
🔹 Mbyll lidhjet që janë idle për një periudhë të gjatë
🔹 Rikthen sesionin nëse klienti rilidhet me të njëjtin ID

📁 Struktura e projektit

🔹 Serveri kryesor TCP
🔹 Klienti
🔹 HTTP server për monitorim
🔹 File për statistika (stats.json)
🔹 Folder për file-t e serverit

🧪 Testimi

🔹 Testuar me disa pajisje në një rrjet real
🔹 Testuar me shumë klientë paralelisht
🔹 Testuar timeout dhe rilidhje automatike
🔹 Testuar kufizimet e roleve dhe operacionet mbi file

📌 Përfundim

🔹 Projekti demonstron përdorimin praktik të TCP sockets
🔹 Implementon menaxhim të shumë klientëve në mënyrë efikase
🔹 Ofron kontroll të aksesit bazuar në role
🔹 Integron monitorim në kohë reale përmes HTTP serverit
🔹 Përfshin mekanizma për stabilitet si timeout dhe reconnect
