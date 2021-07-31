from converter import parse_arguments


def test_parse_arguments():
    args1 = ["--from-sdf", "foo", "--to-tm", "bar"]
    parsed_args1 = parse_arguments(args1)
    assert parsed_args1.from_sdf == "foo" and parsed_args1.to_tm == "bar"

    args2 = ["--from-tm", "foo", "--to-sdf", "bar"]
    parsed_args2 = parse_arguments(args2)
    assert parsed_args2.from_tm == "foo" and parsed_args2.to_sdf == "bar"
