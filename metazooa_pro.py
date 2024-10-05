#!/usr/bin/env python3

#### LIBS ####
import taxopy
import random as rd
import os

#### FUNS ####
def name2taxid(taxdb):
	"""
	Prompts the user to input a taxon name and gets its taxid from the database. If the name is not found in the database, it keeps asking until it is a valid name or until the execution is stopped by Ctrl+D.

	Arguments:
		taxdb: A taxdb object from the taxopy library, contanining the NCBI taxonomy database or an equivalently formatted custom database.

	Returns:
		The proposed taxon's taxid.

	"""
	while 1:
		try:
			proposed_taxname = input("Enter a taxon name:\n")
			# Transform species name to taxid
			proposed_taxid = taxopy.taxid_from_name(proposed_taxname, taxdb)[0] # Note this will NOT work with homonyms, e.g. Pieris is a genus of both plants and butterflies
			return proposed_taxid
		except:
			del proposed_taxname
			print("That is not a valid species name. Please revise spelling an try again:")

def find_max_taxid(nodes_file):
	"""
	Givena a taxdb file, find the maximum taxid.

	Arguments:
		nodes_file: The name of the file containing the taxid nodes.

	Returns:
		The hights valid taxid in the file.
	"""

	command = "cut -f1 %s | tail -n1" % nodes_file
	max_taxid = int(os.popen(command).read().strip())
	return(max_taxid)

def generate_mystery_taxon(max_taxid, limit_taxid, taxdb):
	"""
	Given the maximum taxid possible and the taxid of which to limit the search, generate a random taxid that is a descendant of the limiting taxid (e.g. a species within a family).

	Arguments:
		max_taxid: integer indicating the maximum allowed taxid in the database.
		limit_taxid: the taxid which limits the search.
		taxdb: the taxonomy database form which to generate the taxid.
	
	Returns:
		A randomly generated taxon entry that is a descendant of the 'limit_taxon' taxid.
	"""
	limit_taxon = taxopy.Taxon(limit_taxid, taxdb)
	while 1:
		try:
			mystery_taxid = rd.randint(1, max_taxid)
			mystery_taxon = taxopy.Taxon(mystery_taxid, taxdb) # Need to change, BUT need to provide robustness against missing taxids that could appear
			assert mystery_taxon.rank == 'species'
			assert taxopy.find_lca([mystery_taxon, limit_taxon], taxdb).taxid == limit_taxon.taxid
			return mystery_taxon
		except:
			pass

def play_metazooa_pro(mystery_taxon, taxdb, attempts = 10):
	"""
	Given a mystery taxon, a taxonomy databse, and a number of attempts, let the user guess the correct species as many times as attempts.

	Arguments:
		mystery_taxon: a Taxopy.Taxon object of the species to guess.
		taxdb: the Taxopy.taxdb object containing the taxonomy database.
		attempts: integer indicating the number of rounds the user can play.

	Returns:
		None.
	"""
	# Ask for user input of species name
	print("Done! Now you can start guessing the species:")
	while attempts:
		proposed_taxid = name2taxid(taxdb)

		# Transform proposed taxid to taxon
		proposed_taxon = taxopy.Taxon(proposed_taxid, taxdb)

		# Find LCA of propsed taxon and mystery taxon
		lca_taxon = taxopy.find_lca([mystery_taxon, proposed_taxon], taxdb)

		# If LCA is the same as mystery taxon, they found the taxon
		if lca_taxon.taxid == mystery_taxon.taxid:
			print("Congratulations! You found the mystery species: %s" % mystery_taxon.name)
			exit("Thanks for playing!\n")
		else:
			attempts -=1
			print("That is not the mystery species, but both your proposed species and the mystery species are members of %s." % lca_taxon.name)
			print("Remaining attempts: %s" % str(attempts))

	print("You lose! The mystery species was %s" % mystery_taxon.name)

if __name__ == '__main__':
	#### VARS ####
	delnodes = "delnodes.dmp" # file with deleted nodes

	#### MAIN ####
	# Read taxo library
	print("Welcome to Metazooa Pro version!")
	print("In this game you have to guess a species. If you provide the wrong species, the name of the nearest node shared by the mystery species and your species in the NCBI taxnonmy database is returned as a hint.")
	print("Please wait while we load the database...")
	taxdb = taxopy.TaxDb(nodes_dmp = "nodes.dmp", names_dmp = "names.dmp", merged_dmp = "merged.dmp")

	print("Databse loaded!")

	# Select clade to limit the game to
	print("The game with all taxa can be absurdly hard. Do you want to limit the game to some set of species? If so, enter the name of the group to limit to:") # HAVE TO FIND HOW TO ENTER ROOT IN CASE SOMEONE IS CRAZY
	limit_taxid = name2taxid(taxdb)

	# Find max taxid in the database
	max_taxid = find_max_taxid("nodes.dmp")

	# Generate random taxid for the mystery species, make sure it is a species and not a genus or whatever
	print("Please wait while we decide on a mystery species for you to find...")
	mystery_taxon = generate_mystery_taxon(max_taxid, limit_taxid, taxdb)

	# Play the game!
	play_metazooa_pro(mystery_taxon, taxdb)
