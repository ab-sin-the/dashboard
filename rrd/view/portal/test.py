# -*- coding: utf-8 -*-  

import json

aa = '{"totalRows":5620,"sort":[["column_","desc"]],"data":[{"column_key":"Info</span>","key":338332678,"column_vlan":0,"column_info":"</span>","column_server":"10.20.207.255 :889 ","column_thpt":"70.18 kbit/s ","column_duration":"26:44","column_bytes":"12.93 MB","column_breakdown":"ClientServer","column_client":"HQDEMACBOOK-PRO :889 ","column_proto_l4":"UDP","column_ndpi":" Unknown "},{"column_key":"Info</span>","key":338330258,"column_vlan":0,"column_info":"</span>","column_server":"10.20.207.255 :889 ","column_thpt":"65.5 kbit/s ","column_duration":"26:44","column_bytes":"12.9 MB","column_breakdown":"ClientServer","column_client":"10.20.192.124 :889 ","column_proto_l4":"UDP","column_ndpi":" Unknown "},{"column_key":"Info</span>","key":1077882044,"column_vlan":0,"column_info":"</span>","column_server":"ff02::fb :mdns ","column_thpt":"9.64 kbit/s ","column_duration":"26:41","column_bytes":"1.93 MB","column_breakdown":"ClientServer","column_client":"localhost_prl [IPv6] :mdns ","column_proto_l4":"UDP","column_ndpi":" MDNS "},{"column_key":"Info</span>","key":3927351695,"column_vlan":0,"column_info":"</span>","column_server":"224.0.0.251:mdns ","column_thpt":"9.45 kbit/s ","column_duration":"26:41","column_bytes":"1.9 MB","column_breakdown":"ClientServer","column_client":"localhost_prl :mdns ","column_proto_l4":"UDP","column_ndpi":" MDNS "},{"column_key":"Info</span>","key":3927352907,"column_vlan":0,"column_info":"</span>","column_server":"224.0.0.251:mdns ","column_thpt":"1.86 kbit/s ","column_duration":"25:58","column_bytes":"825.77 KB","column_breakdown":"ClientServer","column_client":"Kiddo:mdns ","column_proto_l4":"UDP","column_ndpi":" MDNS "},{"column_key":"Info</span>","key":2315303236,"column_vlan":0,"column_info":"</span>","column_server":"224.0.0.251:mdns ","column_thpt":"6.42 kbit/s ","column_duration":"26:33","column_bytes":"791.08 KB","column_breakdown":"ClientServer","column_client":"HP Color LaserJet MFP M2...:mdns ","column_proto_l4":"UDP","column_ndpi":" MDNS "},{"column_key":"Info</span>","key":3927352218,"column_vlan":0,"column_info":"</span>","column_server":"224.0.0.251:mdns ","column_thpt":"6.42 kbit/s ","column_duration":"26:36","column_bytes":"720.68 KB","column_breakdown":"ClientServer","column_client":"HP Color LaserJet MFP M2...:mdns ","column_proto_l4":"UDP","column_ndpi":" MDNS "},{"column_key":"Info</span>","key":338389335,"column_vlan":0,"column_info":"</span>","column_server":"10.20.207.255 :mdns ","column_thpt":"4.74 kbit/s ","column_duration":"26:39","column_bytes":"720.24 KB","column_breakdown":"ClientServer","column_client":"8ae3e0c30625 :mdns ","column_proto_l4":"UDP","column_ndpi":" MDNS "},{"column_key":"Info</span>","key":3927352869,"column_vlan":0,"column_info":"</span>","column_server":"224.0.0.251:mdns ","column_thpt":"8.72 kbit/s ","column_duration":"26:38","column_bytes":"714.02 KB","column_breakdown":"ClientServer","column_client":"��靖的MacBook Pro:mdns ","column_proto_l4":"UDP","column_ndpi":" MDNS "},{"column_key":"Info</span>","key":4194852175,"column_vlan":0,"column_info":"</span>","column_server":"239.242.6.7:24267 ","column_thpt":"4.41 kbit/s ","column_duration":"26:40","column_bytes":"708.94 KB","column_breakdown":"ClientServer","column_client":"WORKGROUP :24267 ","column_proto_l4":"UDP","column_ndpi":" Unknown "}],"perPage":10,"currentPage":1}'
print(json.loads(aa))
