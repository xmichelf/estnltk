from estnltk.text import Text
from estnltk.taggers import SentenceTokenizer

def test_merge_mistakenly_split_sentences_1():
    # Tests that mistakenly split sentences have been properly merged
    # 1: splits related to numeric ranges, dates and times
    test_texts = [ 
        #   Merge case:   {Numeric_range_start} {period} + {dash} {Numeric_range_end}
        { 'text': 'Tartu Muinsuskaitsepäevad toimusid 1988. a 14. - 17. aprillil. Tegelikult oli soov need teha nädal hiljem.', \
          'expected_sentence_texts': ['Tartu Muinsuskaitsepäevad toimusid 1988. a 14. - 17. aprillil.', 'Tegelikult oli soov need teha nädal hiljem.'] }, \
        { 'text': 'Bioloogiaolümpiaadi lõppvoor gümnaasiumile, mis algselt oli planeeritud 15. — 16.aprillile, on ümber tõstetud 28. –29.aprillile.', \
          'expected_sentence_texts': ['Bioloogiaolümpiaadi lõppvoor gümnaasiumile, mis algselt oli planeeritud 15. — 16.aprillile, on ümber tõstetud 28. –29.aprillile.'] }, \
        { 'text': 'Seekordne Mulgi konverents plaanitakse pidada 20. – 21. aprill 2012. Esimesel päeval toimub konverents Karksi Valla Kultuurimajas.', \
          'expected_sentence_texts': ['Seekordne Mulgi konverents plaanitakse pidada 20. – 21. aprill 2012.', 'Esimesel päeval toimub konverents Karksi Valla Kultuurimajas.'] }, \
        { 'text': 'USA teadlased tegid uuringu, milles võeti aluseks 1950. – 2008. aasta temperatuurid ning sellel ajavahemikul korda saadetud kuritööd.', \
          'expected_sentence_texts': ['USA teadlased tegid uuringu, milles võeti aluseks 1950. – 2008. aasta temperatuurid ning sellel ajavahemikul korda saadetud kuritööd.'] }, \

        #   Merge case:   {Numeric_year} {period} {|a|} + {lowercase}
        { 'text': '04.02.2001.a. kell 00.40 tuli väljakutse Tallinnas ühte korterisse.', \
          'expected_sentence_texts': ['04.02.2001.a. kell 00.40 tuli väljakutse Tallinnas ühte korterisse.'] }, \
        { 'text': 'Luunja sai vallaõigused 1991.a. kevadel.', \
          'expected_sentence_texts': ['Luunja sai vallaõigused 1991.a. kevadel.'] }, \
        { 'text': 'Manifest 2, mis kinnitati 2011.a. mais Budapestis.', \
          'expected_sentence_texts': ['Manifest 2, mis kinnitati 2011.a. mais Budapestis.'] }, \
        { 'text': 'Samas ujutatakse turg üle võlgnike varaga.\n Praegune 2009.a. riigieelarve tulude maht on prognoositud 97,8 miljardit EEK.', \
          'expected_sentence_texts': ['Samas ujutatakse turg üle võlgnike varaga.', 'Praegune 2009.a. riigieelarve tulude maht on prognoositud 97,8 miljardit EEK.'] }, \
        { 'text': 'Samas teatas investeeringute suurenemisest rohkem ettevõtteid kui aasta tagasi (2005.a. 46%, 2004.a. 35%).', \
          'expected_sentence_texts': ['Samas teatas investeeringute suurenemisest rohkem ettevõtteid kui aasta tagasi (2005.a. 46%, 2004.a. 35%).'] }, \
        { 'text': 'Uuringu esialgsed tulemused muutuvad kättesaadavaks 2002.a. maikuus.', \
          'expected_sentence_texts': ['Uuringu esialgsed tulemused muutuvad kättesaadavaks 2002.a. maikuus.'] }, \

        #   Merge case:   {Date_with_year} {period} + {time}
        { 'text': 'Gert 02.03.2009. 14:40 Tahaks kindlalt sinna kooli:P', \
          'expected_sentence_texts': ['Gert 02.03.2009. 14:40 Tahaks kindlalt sinna kooli:P'] }, \
        #   Merge case:   {|kell|} {time_HH.} + {MM}
        { 'text': 'Kell 15 . 50 tuli elekter Tallinna tagasi .', \
          'expected_sentence_texts': ['Kell 15 . 50 tuli elekter Tallinna tagasi .'] }, \
        { 'text': 'Kell 22 . 00\nTV 3\n“ Thelma\n” ,\nUSA 1991\nRežii : Ridley Scott\n', \
          'expected_sentence_texts': ['Kell 22 . 00\nTV 3\n“ Thelma\n” ,\nUSA 1991\nRežii : Ridley Scott'] }, \

        #   Merge case:   {Numeric_year} {period} + {|aasta|}
        { 'text': 'BRK-de traditsioon sai alguse 1964 . aastal Saksamaal Heidelbergis.', \
          'expected_sentence_texts': ['BRK-de traditsioon sai alguse 1964 . aastal Saksamaal Heidelbergis.'] }, \
        { 'text': 'Tartu Teaduspargil valmib 2005/2006. aastal uus maja.', \
          'expected_sentence_texts': ['Tartu Teaduspargil valmib 2005/2006. aastal uus maja.'] }, \
        { 'text': 'Alates 2008/2009. õppeaastast õpivad kõik 10-nda õpilased C-võõrkeelena saksa keelt.', \
          'expected_sentence_texts': ['Alates 2008/2009. õppeaastast õpivad kõik 10-nda õpilased C-võõrkeelena saksa keelt.'] }, \
        { 'text': 'Kui meie majandus on langenud 2004.–2005. aasta tasemele, peavad sinna tagasi langema ka sissetulekud.', \
          'expected_sentence_texts': ['Kui meie majandus on langenud 2004.–2005. aasta tasemele, peavad sinna tagasi langema ka sissetulekud.'] }, \
        { 'text': '2000. aastal Sydneyst võideti kuldmedal,2004. aastal Ateenas teenisid nad koos hõbeda.', \
          'expected_sentence_texts': ['2000. aastal Sydneyst võideti kuldmedal,2004. aastal Ateenas teenisid nad koos hõbeda.'] }, \
        { 'text': 'Sügisel kaotas naine töö ja ka mehe äri hakkas allamäge veerema. «2009. aasta jaanuaris võtsin ennast töötuna arvele.', \
          'expected_sentence_texts': ['Sügisel kaotas naine töö ja ka mehe äri hakkas allamäge veerema.', '«2009. aasta jaanuaris võtsin ennast töötuna arvele.'] }, \
          
        #   Merge case:   {Numeric|Roman_numeral_century} {period} {|sajand|} + {lowercase}
        { 'text': 'Kui sealt alla sammusin siis leitsin 15. saj. pärit surnuaia .\nVõi oli isegi pikem aeg , 19. saj. lõpust , kusagilt lugesin .', \
          'expected_sentence_texts': ['Kui sealt alla sammusin siis leitsin 15. saj. pärit surnuaia .', 'Või oli isegi pikem aeg , 19. saj. lõpust , kusagilt lugesin .'] }, \
        { 'text': 'Ioonia filosoofia Mileetose koolkonnd (VI-V saj. e. Kr.) olid esimene kreeka filosoofiakoolkond.', \
          'expected_sentence_texts': ['Ioonia filosoofia Mileetose koolkonnd (VI-V saj. e. Kr.) olid esimene kreeka filosoofiakoolkond.'] }, \
        { 'text': 'Otsimisega oli hädas juba Vana-Hiina suurim ajaloolane Sima Qian (II—I saj. e. m. a.). Ta kaebab allikate vähesuse ja vastuolulisuse üle.', \
          'expected_sentence_texts': ['Otsimisega oli hädas juba Vana-Hiina suurim ajaloolane Sima Qian (II—I saj. e. m. a.).', 'Ta kaebab allikate vähesuse ja vastuolulisuse üle.'] }, \
        #   Merge case:   {BCE_or_ACE} {period} + {lowercase}
        { 'text': 'Aastaks 325 p.Kr. olid erinevad kristlikud sektid omavahel tülli läinud.', \
          'expected_sentence_texts': ['Aastaks 325 p.Kr. olid erinevad kristlikud sektid omavahel tülli läinud.'] }, \
        { 'text': 'Suur rahvasterändamine oli avanud IV-nda sajandiga p. Kr. segaduste ja sõdade ajastu.', \
          'expected_sentence_texts': ['Suur rahvasterändamine oli avanud IV-nda sajandiga p. Kr. segaduste ja sõdade ajastu.'] }, \

        #   Merge case:   {Numeric_date} {period} + {month_name_long}
        { 'text': 'Aga selgust ei pruugi enne 15 . augustit tulla .', \
          'expected_sentence_texts': ['Aga selgust ei pruugi enne 15 . augustit tulla .'] }, \
        { 'text': 'Järgarvud selgeks !\nLoomulikult algab uus aastatuhat 1 . jaanuaril 2001 .', \
          'expected_sentence_texts': ['Järgarvud selgeks !', 'Loomulikult algab uus aastatuhat 1 . jaanuaril 2001 .'] }, \
        { 'text': 'Kirijenko on sündinud 26 . juulil 1962 . aastal .\nTa on lõpetanud Gorki veetraspordiinseneride instituudi.', \
          'expected_sentence_texts': ['Kirijenko on sündinud 26 . juulil 1962 . aastal .', 'Ta on lõpetanud Gorki veetraspordiinseneride instituudi.'] }, \
        { 'text': 'Erastamisväärtpabereid aga saab kasutada kuni 1998 . aasta 31 . detsembrini .', \
          'expected_sentence_texts': ['Erastamisväärtpabereid aga saab kasutada kuni 1998 . aasta 31 . detsembrini .'] }, \
        { 'text': '1.–10. oktoobrini näeb erinevates Eesti teatrites väga head Vene teatrit.', \
          'expected_sentence_texts': ['1.–10. oktoobrini näeb erinevates Eesti teatrites väga head Vene teatrit.'] }, \
        { 'text': 'Nad tähistavad oma sünnipäeva töiselt – 3 . septembril on Vanemuise kontserdimajas galakontsert . Ning juubeliaasta lõppkontsert toimub 22 . oktoobril Sakala keskuses .', \
          'expected_sentence_texts': ['Nad tähistavad oma sünnipäeva töiselt – 3 . septembril on Vanemuise kontserdimajas galakontsert .', 'Ning juubeliaasta lõppkontsert toimub 22 . oktoobril Sakala keskuses .'] }, \
          
        #   Merge case:   {Numeric_date} {period} + {month_name_short}
        { 'text': 'Riik on hoiatanud oma liitlasi ja partnereid äritegemise eest Teheraniga ( NYT , 5 . okt . ) .\n', \
          'expected_sentence_texts': ['Riik on hoiatanud oma liitlasi ja partnereid äritegemise eest Teheraniga ( NYT , 5 . okt . ) .'] }, \
        { 'text': '" Ma ei tunne Laidoneri , " vastas Ake .\n5 . sept .', \
          'expected_sentence_texts': ['" Ma ei tunne Laidoneri , " vastas Ake .', '5 . sept .'] }, \

        #   Merge case:   {First_10_Roman_numerals} {period} + {lowercase_or_dash}
        { 'text': 'Rooma ja Kartaago vahel III. - II. sajandil enne meie ajastut Vahemeremaade valitsemise pärast toimunud sõjad.', \
          'expected_sentence_texts': ['Rooma ja Kartaago vahel III. - II. sajandil enne meie ajastut Vahemeremaade valitsemise pärast toimunud sõjad.'] }, \
        { 'text': 'Konkursitöid võetakse vastu 7. - 18. detsembrini aadressil Malmi 8, III. korrus, ruum 37.', \
          'expected_sentence_texts': ['Konkursitöid võetakse vastu 7. - 18. detsembrini aadressil Malmi 8, III. korrus, ruum 37.'] }, \
        
        #   Merge case:   {Number} {period} + {lowercase}
        { 'text': '6 . augustil mängitakse ette sügisringi 4 . vooru kohtumine.', \
          'expected_sentence_texts': ['6 . augustil mängitakse ette sügisringi 4 . vooru kohtumine.'] }, \
        { 'text': '28 . novembril 1918 ründas Nõukogude Vene 6 . diviis Narvat .', \
          'expected_sentence_texts': ['28 . novembril 1918 ründas Nõukogude Vene 6 . diviis Narvat .'] }, \
        { 'text': 'Esimene kobar moodustub üheksanda lehe kohal , teised iga 2. –3 . lehe kohal .', \
          'expected_sentence_texts': ['Esimene kobar moodustub üheksanda lehe kohal , teised iga 2. –3 . lehe kohal .'] }, \
        { 'text': '3 . koht - Anna Jarek ( Poola ) , 2 . koht - Sarah Johnnson ( Rootsi ) , 1 . koht - Elva Björk Barkardottir', \
          'expected_sentence_texts': ['3 . koht - Anna Jarek ( Poola ) , 2 . koht - Sarah Johnnson ( Rootsi ) , 1 . koht - Elva Björk Barkardottir'] }, \
          
        #   Merge case:   {Number} {period} + {hyphen}
        { 'text': '« mootorratta raam , hind 2000. - EEK »', \
          'expected_sentence_texts': ['« mootorratta raam , hind 2000. - EEK »'] }, \
        { 'text': 'Siiski tahavad erinevad tegelejad asja eest nii 1500. - kuni 3000. - krooni saada.', \
          'expected_sentence_texts': ['Siiski tahavad erinevad tegelejad asja eest nii 1500. - kuni 3000. - krooni saada.'] }, \
        { 'text': 'Meelis\nelusees ei ostaks , kui siis 1000. - eest , ja vaenlasele ka ei soovita', \
          'expected_sentence_texts': ['Meelis\nelusees ei ostaks , kui siis 1000. - eest , ja vaenlasele ka ei soovita'] }, \
        { 'text': 'Samas jaga inffi kus saaks SCS 2000. - , ise olen odavaimat näinud ca 2400-2500. - .', \
          'expected_sentence_texts': ['Samas jaga inffi kus saaks SCS 2000. - , ise olen odavaimat näinud ca 2400-2500. - .'] }, \

    ]
    for test_text in test_texts:
        text = Text( test_text['text'] )
        # Perform analysis
        text.tag_layer(['words', 'sentences'])
        # Collect results 
        sentence_texts = \
            [sentence.enclosing_text for sentence in text['sentences'].spans]
        #print(sentence_texts)
        # Check results
        assert sentence_texts == test_text['expected_sentence_texts']



def test_merge_mistakenly_split_sentences_2():
    # Tests that mistakenly split sentences have been properly merged
    # 2: splits related to sentence parts in parentheses
    test_texts = [ 
        #   Merge case:   {period_ending_content_of_parentheses} + {lowercase_or_comma}
        { 'text': 'Lugesime Menippose (III saj. e.m.a.) satiiri...', \
          'expected_sentence_texts': ['Lugesime Menippose (III saj. e.m.a.) satiiri...'] }, \
        { 'text': 'Eestlastest jõudsid punktikohale Tipp ( 2. ) ja Täpp ( 4. ) ja Käpp ( 7. ) .', \
          'expected_sentence_texts': ['Eestlastest jõudsid punktikohale Tipp ( 2. ) ja Täpp ( 4. ) ja Käpp ( 7. ) .'] }, \
        { 'text': 'Murelik lugeja kurdab ( EPL 31.03. ) , et valla on pääsenud kolmas maailmasõda .', \
          'expected_sentence_texts': ['Murelik lugeja kurdab ( EPL 31.03. ) , et valla on pääsenud kolmas maailmasõda .'] }, \
        { 'text': 'Eesti Päevalehes ( 21.01. ) ilmunud uudisnupuke kuulub kahjuks libauudiste rubriiki .', \
          'expected_sentence_texts': ['Eesti Päevalehes ( 21.01. ) ilmunud uudisnupuke kuulub kahjuks libauudiste rubriiki .'] }, \
        { 'text': 'Teine kysimus : kas kohanime ajaloolises tekstis ( nt . 18. saj . ) kirjutada tolleaegse nimetusega v6i tänapäevase ?', \
          'expected_sentence_texts': ['Teine kysimus : kas kohanime ajaloolises tekstis ( nt . 18. saj . ) kirjutada tolleaegse nimetusega v6i tänapäevase ?'] }, \
        { 'text': 'Keiser Taianuse ( 93-117 p .\nKr . ) basseinist Colosseumi lähedal kraapis üks tööline sel kevadel välja huvitava leiu.', \
          'expected_sentence_texts': ['Keiser Taianuse ( 93-117 p .\nKr . ) basseinist Colosseumi lähedal kraapis üks tööline sel kevadel välja huvitava leiu.'] }, \
        { 'text': 'Ja kui ma sain 40 , olin siis Mikuga ( Mikk Mikiveriga - Toim. ) abi-elus .', \
          'expected_sentence_texts': ['Ja kui ma sain 40 , olin siis Mikuga ( Mikk Mikiveriga - Toim. ) abi-elus .'] }, \
        { 'text': 'Originaalis on joogis arrak ( riisiviin - toim. ) , rumm , tee , vesi ja suhkur ,\nseletab Demjanov .', \
          'expected_sentence_texts': ['Originaalis on joogis arrak ( riisiviin - toim. ) , rumm , tee , vesi ja suhkur ,\nseletab Demjanov .'] }, \
        { 'text': '“Praktiline töö läbib kontrolli DVSi (Saksamaa Keevitusliit – toim.) laboris ja selle alusel väljastatakse sertifikaat,” rääkis Einla.', \
          'expected_sentence_texts': ['“Praktiline töö läbib kontrolli DVSi (Saksamaa Keevitusliit – toim.) laboris ja selle alusel väljastatakse sertifikaat,” rääkis Einla.'] }, \
        { 'text': 'Lõpuks otsustasingi kandideerida ning tänane ( reede õhtul - toim. ) võit tuli mulle küll täieliku üllatusena .', \
          'expected_sentence_texts': ['Lõpuks otsustasingi kandideerida ning tänane ( reede õhtul - toim. ) võit tuli mulle küll täieliku üllatusena .'] }, \

        #   Merge case:   {parentheses_start} {content_in_parentheses} + {content_in_parentheses} {parentheses_end}
        { 'text': '( " Easy FM , soft hits ! " ) .', \
          'expected_sentence_texts': ['( " Easy FM , soft hits ! " ) .'] }, \
        { 'text': '( " Mis siis õieti tahetakse ? " , 1912 ) .', \
          'expected_sentence_texts': ['( " Mis siis õieti tahetakse ? " , 1912 ) .'] }, \
        { 'text': 'Kirjandusel ( resp. raamatul ) on läbi aegade olnud erinevaid funktsioone .', \
          'expected_sentence_texts': ['Kirjandusel ( resp. raamatul ) on läbi aegade olnud erinevaid funktsioone .'] }, \
        { 'text': 'Bisweed on alles 17aastane (loe: ta läheb sügisel 11. klassi!) ja juba on tema heliloomingut välja andnud mitmed plaadifirmad.', \
          'expected_sentence_texts': ['Bisweed on alles 17aastane (loe: ta läheb sügisel 11. klassi!) ja juba on tema heliloomingut välja andnud mitmed plaadifirmad.'] }, \
        { 'text': 'Riik on hoiatanud oma liitlasi ja partnereid äritegemise eest Teheraniga ( NYT , 5 . okt . ) .\n', \
          'expected_sentence_texts': ['Riik on hoiatanud oma liitlasi ja partnereid äritegemise eest Teheraniga ( NYT , 5 . okt . ) .'] }, \
        { 'text': 'Varustage aabits oma nimega ning tooge see selle nädala jooksul (23 . – 26. 08) oma rühmaõpetaja kätte!', \
          'expected_sentence_texts': ['Varustage aabits oma nimega ning tooge see selle nädala jooksul (23 . – 26. 08) oma rühmaõpetaja kätte!'] }, \
          
        #   Merge case:   {content_in_parentheses} + {single_sentence_ending_symbol}          
        { 'text': 'Pani eestvedajaks mõne rahvasportlasest poliitiku ( kui neid ikka on ? ) .', \
          'expected_sentence_texts': ['Pani eestvedajaks mõne rahvasportlasest poliitiku ( kui neid ikka on ? ) .'] }, \
        { 'text': 'See oli siis see 60 krooni ( või rubla ? ) .\nMiks on see põletav küsimus ?', \
          'expected_sentence_texts': ['See oli siis see 60 krooni ( või rubla ? ) .', 'Miks on see põletav küsimus ?'] }, \
        { 'text': 'Vähk ( 20.07. - 09.08. ) .\nVähkkasvajana vohav horoskoobihullus on nakatanud Sindki .', \
          'expected_sentence_texts': ['Vähk ( 20.07. - 09.08. ) .', 'Vähkkasvajana vohav horoskoobihullus on nakatanud Sindki .'] }, \
        { 'text': 'Yerlikaya oli protesti sisse andnud ja see rahuldati ( ? ! ) . \nMöllu oli saalis tublisti .', \
          'expected_sentence_texts': ['Yerlikaya oli protesti sisse andnud ja see rahuldati ( ? ! ) .', 'Möllu oli saalis tublisti .'] }, \
        { 'text': 'CD müüdi 400 krooniga ( alghind oli 100 kr. ) .\nOsteti viis tööd , neist üks õlimaal .', \
          'expected_sentence_texts': ['CD müüdi 400 krooniga ( alghind oli 100 kr. ) .', 'Osteti viis tööd , neist üks õlimaal .'] }, \
        { 'text': 'Neenetsi rahvusringkonnas ( kõlab juba ise sürrealistlikult ! ) .\nVähem kummaline polnud tema tegevus Küsimuste ja Vastuste toimetajana .', \
          'expected_sentence_texts': ['Neenetsi rahvusringkonnas ( kõlab juba ise sürrealistlikult ! ) .', 'Vähem kummaline polnud tema tegevus Küsimuste ja Vastuste toimetajana .'] }, \
    ]
    for test_text in test_texts:
        text = Text( test_text['text'] )
        # Perform analysis
        text.tag_layer(['words', 'sentences'])
        # Collect results 
        sentence_texts = \
            [sentence.enclosing_text for sentence in text['sentences'].spans]
        #print(sentence_texts)
        # Check results
        assert sentence_texts == test_text['expected_sentence_texts']



def test_merge_mistakenly_split_sentences_3():
    # Tests that mistakenly split sentences have been properly merged
    # 3: splits related to double quotes
    test_texts = [ 
        #   Merge case:   {sentence_ending_punct} {ending_quotes}? + {comma_or_semicolon} {lowercase_letter}
        { 'text': 'ETV-s esietendub homme " Õnne 13 ! " , mis kuu aja eest jõudis lavale Ugalas .', \
          'expected_sentence_texts': ['ETV-s esietendub homme " Õnne 13 ! " , mis kuu aja eest jõudis lavale Ugalas .'] }, \
        { 'text': 'Naise küsimusele : " Kes on tema uus sekretär ? " , vastas Jaak suure entusiasmiga .', \
          'expected_sentence_texts': ['Naise küsimusele : " Kes on tema uus sekretär ? " , vastas Jaak suure entusiasmiga .'] }, \
        { 'text': 'Lavale astuvad jõulise naissolistiga Conflict OK ! , kitarripoppi mängivad Claires Birthday ja Seachers .', \
          'expected_sentence_texts': ['Lavale astuvad jõulise naissolistiga Conflict OK ! , kitarripoppi mängivad Claires Birthday ja Seachers .'] }, \
        { 'text': 'Tolle taha jääb xxxx miljoni krooni eest nn. " varjatud ainet " .', \
          'expected_sentence_texts': ['Tolle taha jääb xxxx miljoni krooni eest nn. " varjatud ainet " .'] }, \
        { 'text': 'kui sokratese " segav " kohalolek on " välistatud " ja nn. " ellimineeritud " ...', \
          'expected_sentence_texts': ['kui sokratese " segav " kohalolek on " välistatud " ja nn. " ellimineeritud " ...'] }, \
        { 'text': 'Enne " Romeo ja Juliat " koostasid kaks inkvisiitorit " Malleus Maleficarumi " nn. " nöiavasara "', \
          'expected_sentence_texts': ['Enne " Romeo ja Juliat " koostasid kaks inkvisiitorit " Malleus Maleficarumi " nn. " nöiavasara "'] }, \
          
        #   Merge case:   {sentence_ending_punct} + {only_ending_quotes}
        { 'text': 'Mitte meie rühmas , vaid terves polgus ! ”', \
          'expected_sentence_texts': ['Mitte meie rühmas , vaid terves polgus ! ”'] }, \
        { 'text': '“ Tuleb kasutada lund ja jääd , kuni neid veel on . ”', \
          'expected_sentence_texts': ['“ Tuleb kasutada lund ja jääd , kuni neid veel on . ”'] }, \
        { 'text': '“ Akendega on nüüd klaar .\nKas värvin ka raamid ära ? ”', \
          'expected_sentence_texts': ['“ Akendega on nüüd klaar .', 'Kas värvin ka raamid ära ? ”'] }, \
        { 'text': '« See amet on nii raske ! »', \
          'expected_sentence_texts': ['« See amet on nii raske ! »'] }, \
        { 'text': '« Ma sõin tavaliselt kolm hamburgerit päevas , kujutate ette ? »', \
          'expected_sentence_texts': ['« Ma sõin tavaliselt kolm hamburgerit päevas , kujutate ette ? »'] }, \
        { 'text': 'Küsisin mõistlikku summat , arvan .\nNüüd ootan nende pakkumist . »', \
          'expected_sentence_texts': ['Küsisin mõistlikku summat , arvan .', 'Nüüd ootan nende pakkumist . »'] }, \
    ]
    for test_text in test_texts:
        text = Text( test_text['text'] )
        # Perform analysis
        text.tag_layer(['words', 'sentences'])
        # Collect results 
        sentence_texts = \
            [sentence.enclosing_text for sentence in text['sentences'].spans]
        #print(sentence_texts)
        # Check results
        assert sentence_texts == test_text['expected_sentence_texts']


def test_merge_mistakenly_separated_sentence_ending_punctuation():
    # Tests that mistakenly separated sentence ending punctuation will be properly attached to the sentence
    test_texts = [
        #   Merge case:   {sentence_ending_punct} + {only_sentence_ending_punct}
        { 'text': 'SEE EI OLNUD TSIKLI ÕLI ! ! ! ! ! ! !', \
          'expected_sentence_texts': ['SEE EI OLNUD TSIKLI ÕLI ! ! ! ! ! ! !'] }, \
        { 'text': 'see on kindel meteroloogiline fakt\n. .\n!', \
          'expected_sentence_texts': ['see on kindel meteroloogiline fakt\n. .\n!'] }, \
        { 'text': 'Issand Jumal , Sa näed ja ei mürista ! ! ! ? ? ?', \
          'expected_sentence_texts': ['Issand Jumal , Sa näed ja ei mürista ! ! ! ? ? ?'] }, \
        { 'text': 'Aga äkki ongi nümfomaanid reaalselt olemas ? ? ?', \
          'expected_sentence_texts': ['Aga äkki ongi nümfomaanid reaalselt olemas ? ? ?'] }, \
        { 'text': "loodetavasti läheb KE jaoks üle… Jeez… lahe..…", \
          'expected_sentence_texts': ['loodetavasti läheb KE jaoks üle…', 'Jeez… lahe..…'] }, \
        { 'text': 'arvati , et veel sellel aastal j6uab kohale ; yess ! ! !', \
          'expected_sentence_texts': ['arvati , et veel sellel aastal j6uab kohale ; yess ! ! !'] }, \
        { 'text': 'müüks ära sellise riista nagu IZ- Planeta 5 ! ?\nEtte tänades aivar .', \
          'expected_sentence_texts': ['müüks ära sellise riista nagu IZ- Planeta 5 ! ?', 'Ette tänades aivar .'] }, \
        { 'text': 'teine võimalus: elektrikud saavad karistatud voolu läbi.!!!!!!!!!!! !\n', \
          'expected_sentence_texts': ['teine võimalus: elektrikud saavad karistatud voolu läbi.!!!!!!!!!!! !'] }, \
        { 'text': 'Mis ajast Odüsseus ja Caesar KESKAJAL elasid ? ! ?\nOlex võinud väiksest peast vähe rohkem antiikmütoloogiat lugeda.', \
          'expected_sentence_texts': ['Mis ajast Odüsseus ja Caesar KESKAJAL elasid ? ! ?', 'Olex võinud väiksest peast vähe rohkem antiikmütoloogiat lugeda.'] }, \
        { 'text': 'Kiirusta ja osta kohe , kui sul veel pole ! !\nKvaliteettoodang !', \
          'expected_sentence_texts': ['Kiirusta ja osta kohe , kui sul veel pole ! !', 'Kvaliteettoodang !'] }, \
        { 'text': 'Seaduse täitmist reguleerib meil esmaselt siiski politsei. . . Ja ma ei loe kuskilt välja teemast et sa oled üritanud temaga vestelda.', \
          'expected_sentence_texts': ['Seaduse täitmist reguleerib meil esmaselt siiski politsei. . .', 'Ja ma ei loe kuskilt välja teemast et sa oled üritanud temaga vestelda.'] }, \
        { 'text': 'See oli meenutus tänastest eelmistest aaretest. Mari . . aarde leidsime, logisime ja peitsime tagasi.', \
          'expected_sentence_texts': ['See oli meenutus tänastest eelmistest aaretest.', 'Mari . .', 'aarde leidsime, logisime ja peitsime tagasi.'] }, \
        { 'text': 'grafiit määrdega tald muutub kuivaks\n? ? . . kuidas sellest = aru saada kui see nii on ?', \
          'expected_sentence_texts': ['grafiit määrdega tald muutub kuivaks\n? ? . .', 'kuidas sellest = aru saada kui see nii on ?'] }, \
        { 'text': "Teha “ viimane suur rööv ” ( milline klišee . . .\n ! ! ) , ajada ligi 5 miljoni dollari väärtuses kalliskividele . . .", \
          'expected_sentence_texts': ['Teha “ viimane suur rööv ” ( milline klišee . . .\n ! ! ) , ajada ligi 5 miljoni dollari väärtuses kalliskividele . . .'] }, \
          
        #  NB! Problematic stuff:
        { 'text': 'Ja kui süda pole puhas... ??? ??? ??? aiai.', \
          'expected_sentence_texts': ['Ja kui süda pole puhas... ??? ??? ??? aiai.'] }, \
        { 'text': 'Seal on forum kust saab osta , müüa , vahetada , rääkida ja ...... !!\nkÕik sInna !', \
          'expected_sentence_texts': ['Seal on forum kust saab osta , müüa , vahetada , rääkida ja ...... !!\nkÕik sInna !'] }, \

        #   Merge case:   {sentence_ending_punct} {ending_quotes} + {only_sentence_ending_punct}
        { 'text': '" See pole ju üldse kallis .\nNii ilus ! " . \nNõmmel elav pensioniealine Maret .', \
          'expected_sentence_texts': ['" See pole ju üldse kallis .', 'Nii ilus ! " .', 'Nõmmel elav pensioniealine Maret .'] }, \
        { 'text': 'Marjana küsis iga asja kohta " Kak eta porusski ? " . \nKuidas ma keele selgeks sain', \
          'expected_sentence_texts': ['Marjana küsis iga asja kohta " Kak eta porusski ? " .', 'Kuidas ma keele selgeks sain'] }, \
        { 'text': 'Tal polnud aimugi , kust ta järgmise kaustiku saab .\n" . . . jätkan tolle esimese päeva taastamist .', \
          'expected_sentence_texts': ['Tal polnud aimugi , kust ta järgmise kaustiku saab .\n" . . .', 'jätkan tolle esimese päeva taastamist .'] }, \
        { 'text': '" Kuidas saada miljonäriks ? " . \nSelge see , et miljonimängus peavad olema kõige raskemad küsimused .', \
          'expected_sentence_texts': ['" Kuidas saada miljonäriks ? " .', 'Selge see , et miljonimängus peavad olema kõige raskemad küsimused .'] }, \
        { 'text': '" Ega siin ei maksa tooste oodata , hakkama aga kohe võtma ! " . \nMa ei taha seda ärajäänud kohtumist presidendi kaela ajada .', \
          'expected_sentence_texts': ['" Ega siin ei maksa tooste oodata , hakkama aga kohe võtma ! " .', 'Ma ei taha seda ärajäänud kohtumist presidendi kaela ajada .'] }, \
    ]
    for test_text in test_texts:
        text = Text( test_text['text'] )
        # Perform analysis
        text.tag_layer(['words', 'sentences'])
        # Collect results 
        sentence_texts = \
            [sentence.enclosing_text for sentence in text['sentences'].spans]
        #print(sentence_texts)
        # Check results
        assert sentence_texts == test_text['expected_sentence_texts']


def test_split_mistakenly_merged_sentences_1():
    # Tests that mistakenly merged sentences are properly split
    # 1: merges related to missing whitespace between words and punctuation
    test_texts = [ 
        { 'text': 'Kas on ikka niipalju vaja ?Ei ole ju .', \
          'expected_sentence_texts': ['Kas on ikka niipalju vaja ?', 'Ei ole ju .'] }, \
        { 'text': 'Totaalne ülemõtlemine!Ei julge ka väita, et oleks kuivaks jäänud:)', \
          'expected_sentence_texts': ['Totaalne ülemõtlemine!', 'Ei julge ka väita, et oleks kuivaks jäänud:)'] }, \
        { 'text': 'milles üldse seisneb selle ravimi toime?Mida ta teeb ja kuidas/kuhu toimib?Mis juhtub kui ma võtaksin alkoholi?', \
          'expected_sentence_texts': ['milles üldse seisneb selle ravimi toime?', 'Mida ta teeb ja kuidas/kuhu toimib?', 'Mis juhtub kui ma võtaksin alkoholi?'] }, \
        { 'text': 'Iga päev teeme valikuid.Valime kõike alates pesupulbrist ja lõpetades autopesulatega.Jah, iga päev teeme valikuid.', \
          'expected_sentence_texts': ['Iga päev teeme valikuid.', 'Valime kõike alates pesupulbrist ja lõpetades autopesulatega.', 'Jah, iga päev teeme valikuid.'] }, \
    ]
    for test_text in test_texts:
        text = Text( test_text['text'] )
        # Perform analysis
        text.tag_layer(['words', 'sentences'])
        # Collect results 
        sentence_texts = \
            [sentence.enclosing_text for sentence in text['sentences'].spans]
        #print(sentence_texts)
        # Check results
        assert sentence_texts == test_text['expected_sentence_texts']


def test_use_emoticons_as_sentence_endings():
    # Tests that emoticons are used as sentence boundaries
    test_texts = [ 
        # Emoticons as sentence boundaries: a simple case
        { 'text': 'Minu esimene blogi.... kõlab hästi:P Aga tegelikult on paberile vist parem kirjutada....', \
          'expected_sentence_texts': ['Minu esimene blogi.... kõlab hästi:P', \
                                      'Aga tegelikult on paberile vist parem kirjutada....'] }, \
        { 'text': 'Nii habras, ilus ja minu oma :) Kõige parem mis kunagi juhtuda saab :):) Magamata öid mul muidugi ei olnud.', \
          'expected_sentence_texts': ['Nii habras, ilus ja minu oma :)', \
                                      'Kõige parem mis kunagi juhtuda saab :):)',\
                                      'Magamata öid mul muidugi ei olnud.'] }, \
        { 'text': 'Aga lihtsalt puid läheb 10 korda vähem :D Nii lihtne see ongi :D!!', \
          'expected_sentence_texts': ['Aga lihtsalt puid läheb 10 korda vähem :D', \
                                      'Nii lihtne see ongi :D!!'] }, \
        { 'text': 'Mosse M2140 on ka ägedam masin kui see bemm :DD Nõsutun siin eelpoolkommenteerijaga', \
          'expected_sentence_texts': ['Mosse M2140 on ka ägedam masin kui see bemm :DD', \
                                      'Nõsutun siin eelpoolkommenteerijaga'] }, \
        { 'text': 'Dataprojektorit peeti ilmselt silmas, usun :-) See selleks.', \
          'expected_sentence_texts': ['Dataprojektorit peeti ilmselt silmas, usun :-)', \
                                      'See selleks.'] }, \
        { 'text': 'Linalakast eesti talutütar:P Ausõna, nagu meigitud Raja Teele :D', \
          'expected_sentence_texts': ['Linalakast eesti talutütar:P', \
                                      'Ausõna, nagu meigitud Raja Teele :D'] }, \
        # Emoticons as sentence boundaries: a case of repeated emoticons
        { 'text': 'KUUSKÜMMEND KOLM KÕRVITSAT???? :O :O :O See on ju iga koka õudusunenägu :)', \
          'expected_sentence_texts': ['KUUSKÜMMEND KOLM KÕRVITSAT???? :O :O :O', \
                                      'See on ju iga koka õudusunenägu :)'] }, \
        { 'text': 'ikkagi maailmas 2. koht joogipaneku poolest ju.. :D:D:D', \
          'expected_sentence_texts': ['ikkagi maailmas 2. koht joogipaneku poolest ju.. :D:D:D'] }, \
        # Emoticons as sentence boundaries: a case of emoticons following sentence punctuation
        { 'text': 'Appi milline loll jutt... :D Ma ei joo eini', \
          'expected_sentence_texts': ['Appi milline loll jutt... :D', 'Ma ei joo eini'] }, \
        # Emoticons as sentence boundaries: if emoticons are following sentence-ending punctuation,
        # then assume they need to be attached to the previous sentence ...
        { 'text': 'Ma sihin rohkem neid sügismaratone! :D Aga muidu ma julgen Riiat soovitada küll!!!', \
          'expected_sentence_texts': ['Ma sihin rohkem neid sügismaratone! :D', 'Aga muidu ma julgen Riiat soovitada küll!!!'] }, \
        { 'text': 'Oled sa armunud praegu? :) Kui ei siis oli arvatavasti auravärv siiski.', \
          'expected_sentence_texts': ['Oled sa armunud praegu? :)', 'Kui ei siis oli arvatavasti auravärv siiski.'] }, \
        { 'text': 'ka tema ei tea sõnade pool ja pooled tähendust . :( Ehk on see siiski taas D e lfi kirjatsura vaimusünnitis.', \
          'expected_sentence_texts': ['ka tema ei tea sõnade pool ja pooled tähendust . :(', 'Ehk on see siiski taas D e lfi kirjatsura vaimusünnitis.'] }, \
        { 'text': 'aga las läks oma teed,nagunii august poleks läbi mahtunud. :))) Vot sääne äge päiva.\nMis asi see pumm pumm veel on?', \
          'expected_sentence_texts': ['aga las läks oma teed,nagunii august poleks läbi mahtunud. :)))', 'Vot sääne äge päiva.', 'Mis asi see pumm pumm veel on?'] }, \
    ]
    sentence_tokenizer = SentenceTokenizer(use_emoticons_as_endings=True)
    for test_text in test_texts:
        text = Text( test_text['text'] )
        # Perform analysis
        text.tag_layer(['words'])
        sentence_tokenizer.tag(text)
        # Collect results 
        sentence_texts = \
            [sentence.enclosing_text for sentence in text['sentences'].spans]
        #print(sentence_texts)
        # Check results
        assert sentence_texts == test_text['expected_sentence_texts']


def test_fix_repeated_sentence_ending_punctuation():
    # Tests that sentence endings are detected iff the ending punctuation is prolonged/repeated
    test_texts = [ 
        { 'text': 'Hispaanias tuli suur isu vaadata töömeile… Ja nii ma seal puhkasin, kuid samas tegin tööd… See oli lihtsalt nii-nii mõnus feeling :)', \
          'expected_sentence_texts': ['Hispaanias tuli suur isu vaadata töömeile…', \
                                      'Ja nii ma seal puhkasin, kuid samas tegin tööd…', \
                                      'See oli lihtsalt nii-nii mõnus feeling :)' ] }, \
        { 'text': 'Sõin küll tavalisest rohkem..Koguaeg oli tunne, et olen rase.', \
          'expected_sentence_texts': ['Sõin küll tavalisest rohkem..', \
                                      'Koguaeg oli tunne, et olen rase.'] }, \
        { 'text': 'Kas tõesti ??????!!!! Äi usu!', \
          'expected_sentence_texts': ['Kas tõesti ??????!!!!', \
                                      'Äi usu!'] }, \
        { 'text': 'Ja ikka ei usu!!!!?????? Äi usu!', \
          'expected_sentence_texts': ['Ja ikka ei usu!!!!??????', \
                                      'Äi usu!'] }, \
    ]
    for test_text in test_texts:
        text = Text( test_text['text'] )
        # Perform analysis
        text.tag_layer(['words', 'sentences'])
        # Collect results 
        sentence_texts = \
            [sentence.enclosing_text for sentence in text['sentences'].spans]
        #print(sentence_texts)
        # Check results
        assert sentence_texts == test_text['expected_sentence_texts']


def test_apply_sentence_tokenizer_on_empty_text():
    # Applying sentence tokenizer on empty text should not produce any errors
    text = Text( '' )
    text.tag_layer(['words', 'sentences'])
    assert len(text.words) == 0
    assert len(text.sentences) == 0

