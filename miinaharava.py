import haravasto as h
import random
import time

"""
määritellään globaalit sanakirjat jotka ovat listoja sisältäviä listoja
miinakenttä = kenttä jossa miinat ovat
pelikenttä = kenttä joka näytetää pelaajalle
tilasto sisältää muuttujia mitä esim käsittelijäfunktio tarvitsee mutta ei voi saada parametrinä
pelaaja = pelaajan nimi
ruudukko_x = pelialueen leveys ruutuina
ruudukko_y = pelialueen korkeus ruutuina
ekakerta = jos True niin käsittelijäfunktio tietää aloittaa uuden pelin
miinoja = miinojen lukumäärä
aika = päivämäärä sekä kellonaika
kesto = pelin kesto ajallisesti
vuorot = pelin kesto vuoroissa
lopputulos = joko Voitto, Häviö tai Keskeytti
ruutuja_jaljella = laskee jaljella olevat avaamattomat tyhjä ruudut ja päättelee sillä milloin pelin voittaa
loppu = jos True käsittelijäfunktio sulkee grafiikat
"""
miinakentta = {"kentta": None}
pelikentta = {"kentta": None}
tilasto = {
	"pelaaja": None,
	"ruudukko_x": 0,
	"ruudukko_y": 0,
	"ekakerta": True,
	"miinoja": 0,
	"aika": None,
	"kesto": 0,
	"vuorot": 0,
	"lopputulos": "Keskeytti",
	"ruutuja_jaljella": 0,
	"loppu": False
}

def kysy_ruudukon_koko():
	"""
	kysyy pelaajaltya halutun pelialueen koon
	return = pelattavan alueen koko tuplena
	"""
	while True:
		syote = input("Anna pelialueen koko ruuduissa, esim 20x20: ")

		if "x" in syote:
			ruudukon_koko = syote.split("x", 1)
			try: 
				ruudukon_koko[0] = int(ruudukon_koko[0])
				ruudukon_koko[1] = int(ruudukon_koko[1])
			except ValueError:
				print("Anna ruudukon koko kokonaislukuina")
			except TypeError:
				print("Anna kaksi lukua x:llä erotettuna, esim 20x20")
			else:
				return ruudukon_koko
		else:
			print("Anna kaksi lukua x:llä erotettuna, esim 20x20")


def kysy_miinat(ruudukko):
	"""
	kysyy pelaajalta monellako minalla halutaan pelata
	param = pelialueen koko ruuduissa
	"""
	while True:
		try:
			syote = int(input("Anna miinojen määrä: "))
		except ValueError:
			print("Anna miinojen määrä kokonaislukuna")
		else:
			if syote > 0 and syote < ruudukko:
				tilasto["miinoja"] = syote
				return
			else:
				print("Miinojen määrä pitää olla suurempi kuin 0 ja pienempi kuin ruudukon koko")


def luo_ruudukot(ruudukko):
	"""
	määrittää globaaleihin kenttä sanakirjoihin kentän koon
	param = pelialueen koko tuplena
	"""
	mkentta = []
	pkentta = []
	for rivi in range(ruudukko[0]):
		mkentta.append([])
		pkentta.append([])
		for sarake in range(ruudukko[1]):
			mkentta[-1].append(" ")
			pkentta[-1].append(" ")

	miinakentta["kentta"] = mkentta
	pelikentta["kentta"] = pkentta


def miinoita(miinat, kentta, aloituskohta):
	"""
	Tekee kentän ja asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
	param1 = miinojen lukumäärä
	param2 = miinoitettava kenttä listoja sisältävänä listana
	param3 = ensimmäisenä klikattu kohdan x,y arvo tuplena johon ei tule miinaa
	"""
	tilasto["ruutuja_jaljella"] = (len(kentta) * len(kentta[0]) - miinat)

	jaljella = []
	for x in range(len(kentta[0])):
		for y in range(len(kentta)):
			jaljella.append((x, y))

	jaljella.remove(aloituskohta)

	while miinat > 0:
		x = random.randint(0,len(kentta)-1)
		y = random.randint(0, len(kentta[0])-1)
		if (x, y) in jaljella:
			jaljella.remove((x, y))
			kentta[x][y] = "x"
			miinat -= 1


def kasittele_hiiri(x, y, painike, muokkaus):
	"""
	Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
	Tarkistelee mitä kohtaa painetaan ja tilanteen mukaan tekee muutoksia
	param1 = klikattu x arvo
	param2 = klikattu y arvo
	param3 = klikattu hiiren painike
	param4 = tarpeeton arvo mutta pakollinen parametri
	"""
	
	x = int(x/40)
	if x > tilasto["ruudukko_x"]:
		x -= 1
	y = int(y/40)
	if y > tilasto["ruudukko_y"]:
		y -= 1

	if tilasto["loppu"] == True:
		h.lopeta()
		return


	if painike == h.HIIRI_VASEN:
		"""
		Vasenta hiiren painikketta painaessa:
		jos kohdassa on miina, peli loppuu
		jos kohta on tyhjä ja ekakerta == True, luodaan uusi peli
		kun kohta on tyhjä kutsutaan tulvatayttofunktiota paljastamaan lähialueen tyhjät
		"""
		
		if miinakentta["kentta"][y][x] == "x" and pelikentta["kentta"][y][x] != "f":
			tilasto["lopputulos"] = "Häviö"
			pelikentta["kentta"][y][x] = "x"
			h.aseta_piirto_kasittelija(piirra_kentta)
			tilasto["loppu"] = True
			print("Hävisit pelin")
		if miinakentta["kentta"][y][x] == " " and pelikentta["kentta"][y][x] != "f":
			if tilasto["ekakerta"] == True:
				miinoita(tilasto["miinoja"], miinakentta["kentta"], (x,y))
				tilasto["ekakerta"] = False
			tulvataytto(x, y)
			h.aseta_piirto_kasittelija(piirra_kentta)
			tilasto["vuorot"] += 1
			if tilasto["ruutuja_jaljella"] == 0:
				tilasto["lopputulos"] = "Voitto"
				tilasto["loppu"] = True
				print("Voitit pelin")


	if painike == h.HIIRI_OIKEA:
		"""
		Oikeaa hiiren painiketta painaessa:
		Jos kohta on tyhjä laitetaan lippu
		Jos kohdassa on lippu laitetaan tyhjä
		"""
		if pelikentta["kentta"][y][x] == " ":
			pelikentta["kentta"][y][x] = "f"
			
		elif pelikentta["kentta"][y][x] == "f":
			pelikentta["kentta"][y][x] = " "
			
		h.aseta_piirto_kasittelija(piirra_kentta)


def tulvataytto(x, y):
	"""
	Funktio tarkistaa on annetun kohdan vieresssä miinoja ja paljastaa lähialueen tyhjät kohdat
	merkitsee käsiteltyyn kohtaan montako miinaa ympärillä on tai tyhjän avatun ruudun jos ei yhtään
	laskee myös kuinka monta tyhjää kohtaa on vielä jäljellä
	param1 = annetun kohdan x arvo
	param2 = annetun kohdan y arvo
	"""
	tulva = [(x, y)]

	while tulva:
		x, y = tulva.pop()
		miinat = 0

		minX = x - 1
		if (minX < 0):
			minX = 0
		maxX = x + 1
		if (maxX >= tilasto["ruudukko_x"]):
			maxX = tilasto["ruudukko_x"] - 1
		minY = y - 1
		if (minY < 0):
			minY = 0
		maxY = y + 1
		if (maxY >= tilasto["ruudukko_y"]):
			maxY = tilasto["ruudukko_y"] - 1
		
		for j in range(minY, maxY + 1):
			for i in range(minX, maxX + 1):
				if (i == x and j == y):
					continue

				if miinakentta["kentta"][j][i] == 'x':
					miinat += 1
					
		for j in range(minY, maxY + 1):
			for i in range(minX, maxX + 1):
				if (i == x and j == y):
					continue

				if miinakentta["kentta"][j][i] == " " and miinat == 0:
					tulva.append((i, j))

		if miinakentta["kentta"][y][x] == " ":
			tilasto["ruutuja_jaljella"] -= 1

		
		miinakentta["kentta"][y][x] = str(miinat)
		pelikentta["kentta"][y][x] = str(miinat)


def piirra_kentta():
	"""
	Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän ruudut näkyviin peli-ikkunaan.
	Funktiota kutsutaan aina kun pelimoottori pyytää ruudun näkymän päivitystä.
	"""
	h.tyhjaa_ikkuna()
	h.piirra_tausta()
	h.aloita_ruutujen_piirto()
	for j in range(len(pelikentta["kentta"])):
		for i, avain in enumerate(pelikentta["kentta"][j]):
			h.lisaa_piirrettava_ruutu(avain, i * 40, j * 40)

	h.piirra_ruudut()


def tulokset(muoto):
	"""
	Funktio kirjoittaa tekstitiedostoon tilastoa pelatuista peleistä tai lukee sieltä pelatut pelit
	param1 = muoto jolla määritetään halutaanko funktiota käyttää lukemiseen vai kirjoittamiseen
	"""

	if muoto == "kirjoitus":
		"""
		kirjoittaa tiedostoon pilkulla erotettuna:
		pelaajan nimi, pvm ja klo, montako minuttia pelattiin, monta sekunttia minuuttien lisäksi, montako vuoroa, pelialueen koko, miinojen määrä ja lopputulos
		"""
		try:
			with open("tulokset.txt", "a") as kohde:
				aika = time.strftime("%d.%m.%Y %H:%M", tilasto["aika"])
				sekunnit = int(tilasto["kesto"]%60)
				minuutit = int(tilasto["kesto"]/60)
				kohde.write("{},{},{},{},{},{},{},{},{}\n".format(tilasto["pelaaja"], aika, minuutit, sekunnit, tilasto["vuorot"], tilasto["ruudukko_x"], tilasto["ruudukko_y"], tilasto["miinoja"], tilasto["lopputulos"]))
		except IOError:
			print("Kohdetiedostoa ei voitu avata. Tulosten tallentaminen epäonnistui")

	if muoto == "luku":
		"""
		luetaan tiedostosta aiemmat pelitulokset ja printataan ne nätimmin muotoillen
		"""
		try:
			with open("tulokset.txt", "r") as kohde:
				for rivi in kohde:
					tulos = rivi.rstrip()
					lista = tulos.split(",")
					print("Pelaaja {} alkoi pelaamaan {}, peli kesti {} minuuttia {} sekunttia ja {} vuoroa. ".format(lista[0], lista[1], lista[2], lista[3], lista[4]))
					print("Peliä pelattiin {}x{} ruudukolla ja {} miinalla. Lopputulos oli {}".format(lista[5], lista[6], lista[7], lista[8]))
		except IOError:
			print("Tilastoja ei vielä ole")


def valikko():
	"""
	pelivalikko jossa kysellä pelin alussa mitä halutaan tehdä
	return = vaihtoehto joka kertoo aloitetaanko uusi, katsotaanko tuloksia vai lopetetaanko pelaaminen
	"""

	print("\nValitse vaihtoehto:")
	print("1. Aloita uusi peli")
	print("2. Katso tilastot")
	print("3. Lopeta pelaaminen")
	while True:
		try:
			vaihtoehto = int(input("Anna vaihtoehtoa vastaava numero: "))
		except ValueError:
			print("Anna pelkkä vaihtoehtoa vastaava numero")
		else:
			if vaihtoehto > 0 and vaihtoehto < 4:
				return vaihtoehto


def main():
	"""
	pääohjelma jossa lähinnä kutsutaan muita funktioita ja alustetaan tietoja aina kun palataan takaisin
	"""

	print("Tervetuloa pelaamaan miinaharavaa!")
	tilasto["pelaaja"] = input("Anna pelaajan nimi: ")
	while True:
		vaihtoehto = valikko()
		if vaihtoehto == 1:
			tilasto["ekakerta"] = True
			tilasto["miinoja"] = 0
			ruudukon_koko = kysy_ruudukon_koko()
			tilasto["ruudukko_x"] = ruudukon_koko[1]
			tilasto["ruudukko_y"] = ruudukon_koko[0]
			kysy_miinat(ruudukon_koko[0]*ruudukon_koko[1])
			luo_ruudukot(ruudukon_koko)
			h.lataa_kuvat("spritet")
			h.luo_ikkuna(ruudukon_koko[1]*40, ruudukon_koko[0]*40)
			h.aseta_piirto_kasittelija(piirra_kentta)
			h.aseta_hiiri_kasittelija(kasittele_hiiri)
			tilasto["aika"] = time.localtime()
			tilasto["kesto"] = time.time()
			tilasto["vuorot"] = 0
			tilasto["lopputulos"] = "Keskeytti"
			h.aloita()
			tilasto["kesto"] = time.time() - tilasto["kesto"]
			tulokset("kirjoitus")
			tilasto["loppu"] = False

		elif vaihtoehto == 2:
			tulokset("luku")

		else:
			break

if __name__ == "__main__":
	main()