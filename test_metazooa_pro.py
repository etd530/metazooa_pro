#### LIBS ####
import metazooa_pro as mt
import mock # for testing stuff that requires user input

#### VARS ####
taxdb = mt.taxopy.TaxDb(nodes_dmp = "test_nodes.dmp", names_dmp = "test_names.dmp", merged_dmp = "test_merged.dmp")

#### Tests for find_max_taxid ####
# Test that it returns the correct last node, skipping deleted ones
def test_find_max_taxid():
	assert mt.find_max_taxid(taxdb, "test_delnodes.dmp") == 10

#### Tests for name2taxid ####
# Tets that it returns the correct taxid from a species name
def test_name2taxid_species_name(monkeypatch):
	with mock.patch('builtins.input', return_value = 'Azorhizobium'):
		assert mt.name2taxid(taxdb) == 6