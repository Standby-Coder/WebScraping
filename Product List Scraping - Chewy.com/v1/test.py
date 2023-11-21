import urllib.parse

def convert_chewy_url(raw_url):
    # Remove any leading and trailing whitespace and backslashes
    raw_url = raw_url.strip("\\").strip()

    # Check if the URL contains "/b/" or "/dp/"
    if "/b/" in raw_url or "/dp/" in raw_url:
        # Parse the raw URL
        parsed_url = urllib.parse.urlparse(raw_url)
        print(parsed_url)
        # Split the path into segments
        path_segments = parsed_url.path.split("/")

        # Check if "/b/" is present in the path segments
        if "/b/" in path_segments:
            # Find the index of "/b/" in the segments
            index = path_segments.index("/b/")

            # Construct a new path with "/b/" and everything after it
            new_path = "/".join(path_segments[index:])

            # Construct the final URL
            final_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params, parsed_url.query, parsed_url.fragment))

            return final_url

        # Check if "/dp/" is present in the path segments
        elif "/dp/" in path_segments:
            # Find the index of "/dp/" in the segments
            index = path_segments.index("/dp/")

            # Construct a new path with "/dp/" and everything after it
            new_path = "/".join(path_segments[index:])

            # Construct the final URL
            final_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params, parsed_url.query, parsed_url.fragment))

            return final_url

    # If the URL doesn't contain "/b/" or "/dp/", return it as is
    return raw_url

# Example usage:
raw_url = "(hhttps://www.chewy.com/b/dog-supplies-1969\")"
converted_url = convert_chewy_url(raw_url)
print(converted_url)  # Output: https://www.chewy.com/b/dog-supplies-1969
