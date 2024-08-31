#!/usr/bin/env python3

#### LIBS ####
import taxopy
import random as rd

#### FUNS ####
def name2taxid(taxdb):
	"""
	Prompts the user to input a taxon name and gets its taxid from the database. If the name is not found in the database, it keeps asking until it is a valid name or until the execution is stopped by Ctrl+D.

	Arguments:
		taxdb: A taxdb object from the taxopy library, contanining the NCBI taxonomy database or an equivalently formatted custom database.

	Returns:
		A string containing the proposed taxon's name.

	"""
	while 1:
		try:
			proposed_taxname = input("Enter a taxon name:\n")
			# Transform species name to taxid
			proposed_taxid = taxopy.taxid_from_name(proposed_taxname, taxdb)[0] # Note this will NOT work with homonyms, e.g. Pieris is a genus of both plants and butterflies
			print(proposed_taxname)
			print(proposed_taxid)
			return proposed_taxid
		except:
			del proposed_taxname
			print("That is not a valid species name. Please revise spelling an try again:")


def find_max_taxid(taxdb, delnodes):
	"""
	Given a taxdb object and the path to a file of deleted node numbers, find the maximum valid taxid.

	Arguments:
		taxdb: A taxdb object from the taxopy library, contanining the NCBI taxonomy database or an equivalently formatted custom database.
		delnodes: The name of a file containing the deleted nodes from the NCBI taxonomy database.

	Returns:
		The highest valid taxid in the database.
	"""
	# Read delnodes into a list
	delnodes_list = []
	with open(delnodes, 'r') as fh:
		for line in fh:
			delnodes_list.append(int(line.strip().split("\t")[0]))

	# Get maxmimum taxid taking into account the deleted taxids
	i = 1 # we start at one which is the taxid for the root of the tree of life (i.e. the LUCA)
	while 1:
		print(i)
		try:
			max_taxon = taxopy.Taxon(i, taxdb)
			i +=1
		except taxopy.exceptions.TaxidError:
			if i in delnodes_list:
				i += 1
				continue
			else:
				max_taxid = max_taxon.taxid
				print("Maximum taxid is: %s" %str(max_taxid))
				return(max_taxid)

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
	limit_taxon = name2taxid(taxdb)

	# Find max taxid available


	# For now we skip because of taxdump meaning taxids are not consecutive and I was lazy to find the taxdump file now
	max_taxid = 1000000 # placeholder, this is NOT the max taxid at all


	# Generate random taxid for the mystery species, make sure it is a species and not a genus or whatever
	print("Please wait while we decide on a mystery species for you to find...")
	while 1:
		try:
			mystery_taxid = rd.randint(1, max_taxid)
			mystery_taxon = taxopy.Taxon(mystery_taxid, taxdb) # Need to change, BUT need to provide robustness against missing taxids that could appear
			assert mystery_taxon.rank == 'species'
			break
		except:
			pass

	# Ask for user input of species name
	print("Done! Now you can start guessing the species:")
	attempts = 10
	while attempts:
		proposed_taxid = name2taxid(taxdb)

		# Tranform proposed taxid to taxon
		proposed_taxon = taxopy.Taxon(proposed_taxid, taxdb)


		# Find LCA of propsed taxon and mystery taxon
		lca_taxon = taxopy.find_lca([mystery_taxon, proposed_taxon], taxdb)

		# If LCA is the same as mystery taxon, they found the taxon
		if lca_taxon.taxid == mystery_taxid:
			print("Congratulations! You found the mystery species: %s" % mystery_taxon.name)
			exit("Thanks for playing!\n")
		else:
			attempts -=1
			print("That is not the mystery species, but both your proposed species and the mystery species are members of %s." % lca_taxon.name)
			print("Remaining attempts: %s" % str(attempts))

	print("You lose! The mystery species was %s" % mystery_taxon.name)