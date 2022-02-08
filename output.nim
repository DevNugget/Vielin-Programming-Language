import parseutils, strutils

proc splitArgs(args: string): seq[string] =
  var
    parsed, tmp: string
    i, quotes: int
  
  while i < args.len:
    i += args.parseUntil(parsed, Whitespace, i) + 1
    tmp.add(parsed)
    if parsed.startsWith('"'):
      quotes.inc
    if parsed.endsWith('"'):
      quotes.dec
    elif quotes > 0:
      tmp.add(" ")

    if parsed.startsWith("'"):
      quotes.inc
    if parsed.endsWith("'"):
      quotes.dec
    elif quotes > 0:
      tmp.add(" ")
    
    if quotes == 0:
      tmp.removePrefix('"')
      tmp.removeSuffix('"')
      result.add(tmp)
      tmp = ""
  
  if tmp.len > 0:
    result.add(tmp[1 .. ^2])

let text = "spam eggs \"spam and eggs\" don't"

var relf = splitArgs(text)
echo relf[3]
