# map Morningstar company ID to company name
# because some pages don't show company name anymore
file_to_name = {
    "0P0001DIM8": "2CRSI SA",
    "0P00009W9O": "Acteos",
    "0P00009W9P": "Actia Group",
    "0P0000XDQA": "Activium Group",
    "0P0001BP5I": "Adeunis",
    "0P0000DKYW": "Adthink",
    "0P00009WAD": "Alpha Mos",
    "0P00009WAH": "Alten",
    "0P00009WAJ": "Altran Technologies SA",
    "0P0001357J": "Anevia SA",
    "0P00009WAT": "Archos",
    "0P0000DKY4": "Assima PLC",
    "0P00009WJG": "Atari SA",
    "0P00013LNT": "Ateme SA",
    "0P00009WB0": "Atos SE",
    "0P00009WB2": "Aubay",
    "0P0001DZ6U": "Audiovalley SA",
    "0P00009WBD": "Avenir Télécom",
    "0P00012OZY": "Awox SA",
    "0P0000TI1C": "Axway Software"
    "0P00009WBV": "Bigben Interactive",
    "0P0000DKU1": "Bilendi SA",
    "0P0000ZT95": "Blue Solutions SA",
    "0P00009WCN": "Capgemini SE",
    "0P00009WCT": "Cast",
    "0P00009WCY": "Cegedim SA",
    "0P0000DKYP": "Cheops Technology France SA",
    "0P00009WD8": "Cibox Inter@active",
    "0P00009WBB": "Claranova SA",
    "0P00009WDK": "Cofidur SA",
    "0P0001DG9I": "Cogelec SA",
    "0P00009WDN": "Coheris",
    "0P000148AC": "Condor Technologies NV",
    "0P00009WDF": "Dalet SA",
    "0P0000DKTP": "Damaris SA",
    "0P00009WEN": "Dassault Systemes",
    "0P00016MLW": "Datbim SA",
    "0P00009WEU": "Devoteam SA",
    "0P00009WEY": "Digigram",
    "0P0001D92A": "DONTNOD Entertainment SA",
    "0P00015UOE": "Drone Volt SA",
    "0P0000DKWS": "EasyVista SA",
    "0P00009WFI": "Egide SA",
    "0P0000YLOO": "Ekinops SA",
    "0P0001DCAT": "Enensys Technologies SA",
    "0P0000DKYH": "Entreparticuliers SA",
    "0P0000DKX0": "Envea SA",
    "0P0000DKZX": "Equipements Audiovisuels &Systemes",
    "0P00009WFR": "Esi Group SA",
    "0P00009WFS": "Esker SA",
    "0P00009WG7": "Eutelsat Communications",
    "0P0000DKWN": "FILAE SA",
    "0P00015A1H": "Focus Home Interactive SA",
    "0P00009WZQ": "Generix Group FCE",
    "0P00009WHQ": "Gérard Perrier Industrie",
    "0P0000NIZG": "Green Energy 4 Seasons SA",
    "0P00009WGR": "Groupe George SA",
    "0P00009WI7": "Groupe Open SA",
    "0P0000DKZY": "Groupe Plus Values",
    "0P00009WID": "Guillemot Corp SA",
    "0P0000DKWG": "Harvest SA",
    "0P00009WIL": "HF Co",
    "0P00016675": "Hipay Group SA",
    "0P0000DKY7": "HiTechPros SA",
    "0P00019973": "Horizontal Software SA",
    "0P00009WIT": "Proactis SA",
    "0P0000DKPP": "Hydr Exploitations SA",
    "0P0000EOZ6": "i2S Corp SA",
    "0P0000DKU3": "IDS",
    "0P00009WJ4": "IGE Plus XAO SA",
    "0P0001782A": "Immersion SA",
    "0P0000XQUB": "Infoclip",
    "0P00009WJH": "Infotel SA",
    "0P00009WJM": "Innelec Multimedia SA",
    "0P0000VG53": "Verimatrix",
    "0P0000VGHC": "Intrasense",
    "0P00009WJV": "IT Link",
    "0P00009WJW": "Itesoft",
    "0P00009WJX": "ITS Group SA",
    "0P0001DEZG": "Kalray SA",
    "0P00017YTS": "Kerlink SA",
    "0P00009WK6": "Keyrus",
    "0P00009WKD": "Lacroix SA",
    "0P00009WKR": "Lectra",
    "0P00009WKW": "Lexibook Linguistic Electronic Systems SA",
    "0P00009WKX": "Linedata Services",
    "0P0000DKSC": "Locasystem international SA",
    "0P0000DKUQ": "Logic Instrument SA",
    "0P00013NPS": "Lucibel SA",
    "0P0000NIV4": "M2i SAS",
    "0P0000NJ7X": "Magillem Design Services",
    "0P00009WLE": "Mecelec Composites SA",
    "0P00009WLF": "Dedalus France",
    "0P0001CXB8": "Media Lab SpA",
    "0P00009WLL": "Memscap SA",
    "0P00009WCO": "Mersen SA",
    "0P0000DKU8": "Microwave Vision",
    "0P000153GV": "Mulann SA",
    "0P00019NQB": "Multimicrocloud SA",
    "0P0000DKP7": "Neocom Multimedia",
    "0P00009WM8": "Netgem SA",
    "0P00009WMB": "Neurones",
    "0P0000EWMY": "Nokia Oyj",
    "0P0000DKV4": "Novatech Industries",
    "0P0000DKVH": "NSE Industries",
    "0P000156V0": "Oceasoft SA",
    "0P0001CSOV": "Octopus Robots SA",
    "0P0000UAKG": "Onlineformapro",
    "0P0001DKRU": "Ordissimo SA",
    "0P0001D3BN": "Oxatis",
    "0P0000DKTR": "Pacte Novation SA",
    "0P00013FW7": "Paragon ID",
    "0P00009WNB": "Parrot SA",
    "0P00009WNJ": "Pharmagest Interactive",
    "0P0000NR2Y": "Photonike Capital SA",
    "0P0000DKWL": "Planet Media",
    "0P00009WNS": "Precia SA",
    "0P0000DKXD": "Prodware SA",
    "0P00009WNY": "Prologue SA",
    "0P00012PO4": "Proventure Gold Inc",
    "0P0000NJ6V": "Reworld Media",
    "0P00009WO9": "Rexel SA",
    "0P00009WOB": "Riber",
    "0P0000DKVE": "Scientific Brain Training",
    "0P0000DKSI": "Securinfor",
    "0P000154IB": "Semplicemente S.p.A",
    "0P00009WQM": "SES-imagotag SA",
    "0P0000DKWH": "Sidetrade SA",
    "0P0000DKWQ": "Societe O2I",
    "0P00009WPI": "Societe Pour LInformatique Industrielle",
    "0P00009WQ1": "Sodifrance",
    "0P00009WQ8": "Soitec SA",
    "0P00009WN6": "Solocal Group SA",
    "0P0000DKWY": "Solutions 30 SE",
    "0P00009WQB": "Sopra Stevia Group",
    "0P00009WPR": "SQLI SA",
    "0P00009WQL": "STMicroElectronics SA",
    "0P0000DL00": "Streamwide",
    "0P00009WQQ": "Sword Group",
    "0P00009WR7": "Tessi",
    "0P0000DKRC": "Altran Technologies SA",
    "0P0000E6AI": "Travel Technology Interactive SA",
    "0P000159VC": "Tronics Microsystems",
    "0P0000TE8D": "Txcom",
    "0P00009WRU": "Ubisoft Entertainment",
    "0P00009WRW": "Umanis NR",
    "0P00009WS0": "Union Technologies Interactive Group",
    "0P00013498": "Visiativ SA",
    "0P00009WSE": "Visiodent SA",
    "0P0001F3D2": "VOGO SA",
    "0P0001DCAR": "Voluntis SA",
    "0P000163XE": "Wallix Group SA",
    "0P00009WQ9": "Wavestone SA",
    "0P0000DKXR": "Weborama SA",
    "0P0000P373": "Wedia",
    "0P00017Q77": "Witbe SA",
    "0P0001A178": "X-FAB Silicon Foundries SE"
}
