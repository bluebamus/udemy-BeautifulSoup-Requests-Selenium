import re

# 숫자에 매칭 (\d) -- 어떤 십진수도 매칭 -- [0-9]
regex = re.compile("\d")

# 숫자가 아닌 문자에 매칭 (\D) -- 어떤 비 숫자문자도 매칭 -- [^0-9]
regex = re.compile("\D")

# 공백 문자에 매칭 (\s)
regex = re.compile("\s")

# 공백이 아닌 문자에 매칭 (\S)
regex = re.compile("\S")

# 알파벳과 숫자 문자에 매칭 (\w) -- [a-zA-Z0-9_]
regex = re.compile("\w")

# 알파벳과 숫자가 아닌 문자에 매칭 (\W) -- [^ a-zA-Z0-9_]
regex = re.compile("\W")
