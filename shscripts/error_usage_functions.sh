print_usage ( )
{
	echo "$usage_string" >&2
}

print_error ( )
{
	echo "Error: $@" >&2
}

print_error_and_die ( )
{
	print_error $@
	print_usage
	exit 1
}

print_usage_and_die ( )
{
	print_usage
	exit 0
}

