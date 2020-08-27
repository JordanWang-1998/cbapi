'''
    Test cbapi to download and present organization and people data from Crunchbase
'''

import cbapi

def test_cbapi():
	try:
		test_ppl = cbapi.get_ppl(name="Jordan", types="investor")
		test_orgs = cbapi.get_orgs(name="tech", types="investor", locations="New York")
	except Exception:
		print("Runtime Error")

if __name__ == "__main__":
    test_cbapi()