from code import foo

def test_foo(snapx):
	assert snapx.to_match_snapshot(["fdfd", "fdfd"])
	assert foo() == "hello world"

def test_goo():
	assert True