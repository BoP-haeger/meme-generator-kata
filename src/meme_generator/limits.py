"""Input limits. So far only MULTIPART_SPOOL_BYTES is applied; the others are not enforced."""

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_SOURCE_PIXELS = 25_000_000
MAX_LONG_SIDE = 1600
MAX_TEXT_CHARS = 200

# Starlette spools multipart parts above this size to a temp file.
# Keep it above the upload limit so an accepted upload never touches disk.
MULTIPART_SPOOL_BYTES = MAX_UPLOAD_BYTES + 1024 * 1024
