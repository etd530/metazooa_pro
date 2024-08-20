#### LIBS ####
import metazooa_pro as mt

#### Tests for name2taxid ####
# Test that it returns the correct last node, skipping deleted ones
def test_find_max_taxid():
	taxdb = mt.taxopy.TaxDb(nodes_dmp = "test_nodes.dmp", names_dmp = "test_names.dmp", merged_dmp = "test_merged.dmp")

	assert mt.find_max_taxid(taxdb, "test_delnodes.dmp") == 10

