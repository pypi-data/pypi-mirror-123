'''
Copyright 2021 Rairye
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''

def is_punct(char):
    if type(char) != str:
        return False
    
    if len(char) > 1 or len(char) == 0:
        return False

    return ((char.isalpha() or char.isnumeric()) or char.isspace()) == False

def get_category(char):
    if char.isspace():
        return "SPACE"

    return "PUNCT" if is_punct(char) else "NOTPUNCT"

def normalize_punct(input_str, mode, input_skips = "", replacement = " "):
    result = ""
    skips = [] if type(input_skips) != str else set([char for char in input_skips])
    replacement = replacement if type(replacement) == str else " "
    last_space = None
    last_replacement = None

    for i in range(len(input_str)):
        char = input_str[i]
        current_category = get_category(char)

        if current_category == "PUNCT" and char not in skips:
            if mode == "REPLACE" and ((last_space == None and last_replacement == None) or ((last_space != i-1 and input_str[i-1] != replacement) and (last_replacement != i-1 and not result.endswith(replacement)))):
                result+=replacement
                last_replacement = i
                last_space = i

            continue
            
        if current_category == "SPACE" and mode == "REPLACE":
            last_space = i

            if result.endswith(char) and (last_replacement == i-1):
                    continue

        result+=char    

    return result

def strip_punct(input_str, input_skips = ""):
    if type(input_str) != str:
        return input_str
    
    return normalize_punct(input_str, "STRIP", input_skips)

def replace_punct(input_str, input_skips = "", replacement= " "):
    if type(input_str) != str:
        return input_str
    
    return normalize_punct(input_str, "REPLACE", input_skips, replacement)
