# Copyright 2013-2014 Valentin Gosu.
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.


# Run as: python make_idna_table.py idna_table.txt > src/idna_table.rs
# You can get the latest idna table from
# http://www.unicode.org/Public/idna/latest/IdnaMappingTable.txt

print('''\
// Copyright 2013-2014 Valentin Gosu.
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option. This file may not be copied, modified, or distributed
// except according to those terms.

// Generated by make_idna_table.py
''')

print('''\
#[allow(non_camel_case_types)]
pub enum MappingStatus {
    valid,
    ignored,
    mapped,
    deviation,
    disallowed,
    disallowed_STD3_valid,
    disallowed_STD3_mapped,
}

pub struct Mapping {
    pub from: u32,
    pub to: u32,
    pub status: MappingStatus,
    pub mapping: &'static [u32],
}

''')

print("static NONE: [u32;0] = [];")

txt = open("IdnaMappingTable.txt")
line_no = 0

for line in txt:
    # remove comments
    head, sep, tail = line.partition('#')
    # skip empty lines
    if len(head.strip()) == 0:
        continue
    line_no = line_no + 1

txt = open("IdnaMappingTable.txt")
print("pub static TABLE: [Mapping; "+str(line_no)+"] = [")

mappings = []

for line in txt:
    # remove comments
    head, sep, tail = line.partition('#')
    # skip empty lines
    if len(head.strip()) == 0:
        continue
    table_line = head.split(';')
    first, sep, last = table_line[0].strip().partition('..')
    if len(last)==0:
        last = first
    mapping = "NONE"
    if len(table_line)>2:
        if len(table_line[2].strip())>0:
            codes = table_line[2].strip().split(' ')
            newmap = ""
            for code in codes:
                newmap = newmap + "0x" + code + ", "
            newmap = "[" + newmap + "]"
            mapping = "MAPPING_%s_%s" % (first, last)
            static_array = "static %s : [u32; %d] = %s;" % (mapping, len(codes), newmap)
            mappings.append(static_array)
    print "    Mapping{ from: 0x%s, to: 0x%s, status: MappingStatus::%s, mapping: &%s }," % (first, last, table_line[1].strip(), mapping)

print("];")

for mapping in mappings:
    print mapping
