import re

USERNAME_REGEX = re.compile(r"^[A-Za-z0-9_]+$")
DB_PATH = "database/database.sqlite"
SCHEMA_PATH = "database/schema.sql"
STATUS_TYPE = [
  "Pending",
  "Accepted"
]
DUMMY_DATA = {
  "post_category": [
    { "id": 1, "category": "music" },
    { "id": 2, "category": "art" },
    { "id": 3, "category": "sports" },
    { "id": 4, "category": "programming" },
    { "id": 5, "category": "gardening" },
    { "id": 6, "category": "finance" },
    { "id": 7, "category": "economy" },
    { "id": 8, "category": "math" },
    { "id": 9, "category": "literature" },
    { "id": 10, "category": "language" }
  ],
  "users": [{
    "id": 1,
    "username": "cplomer0",
    "email": "gtrimnell0@people.com.cn",
    "password": "gcrannach0",
    "location": "Philippines"
  }, {
    "id": 2,
    "username": "ltamas1",
    "email": "rruilton1@tumblr.com",
    "password": "apitson1",
    "location": "Azerbaijan"
  }, {
    "id": 3,
    "username": "csmallacombe2",
    "email": "jcumbridge2@stanford.edu",
    "password": "jdows2",
    "location": "Japan"
  }, {
    "id": 4,
    "username": "smoncrieffe3",
    "email": "vmcgairl3@github.io",
    "password": "jkefford3",
    "location": "Indonesia"
  }, {
    "id": 5,
    "username": "cjeffries4",
    "email": "jsweet4@uiuc.edu",
    "password": "bvaisey4",
    "location": "South Africa"
  }, {
    "id": 6,
    "username": "jbardell5",
    "email": "kellerman5@sbwire.com",
    "password": "msanbrook5",
    "location": "Democratic Republic of the Congo"
  }, {
    "id": 7,
    "username": "kkrzysztofiak6",
    "email": "lsoutherton6@symantec.com",
    "password": "bechallier6",
    "location": "Argentina"
  }, {
    "id": 8,
    "username": "kbinestead7",
    "email": "ccorkan7@oracle.com",
    "password": "lmccaig7",
    "location": "Brazil"
  }, {
    "id": 9,
    "username": "lhaskey8",
    "email": "sdonoghue8@posterous.com",
    "password": "hmcnicol8",
    "location": "China"
  }, {
    "id": 10,
    "username": "rsetter9",
    "email": "khickenbottom9@unesco.org",
    "password": "wfilinkov9",
    "location": "Indonesia"
  }],
  "posts": [{
    "owner": 1,
    "title": "Piano guide",
    "description": "Lorem ipsum",
    "category_id": 1,
    "is_open": 1,
  },{
    "owner": 2,
    "title": "Guitar",
    "description": "Lorem ipsum",
    "category_id": 1,
    "is_open": 1,
  },{
    "owner": 3,
    "title": "Football",
    "description": "Lorem ipsum",
    "category_id": 3,
    "is_open": 1,
  },{
    "owner": 4,
    "title": "Basketball",
    "description": "Lorem ipsum",
    "category_id": 3,
    "is_open": 1,
  },{
    "owner": 5,
    "title": "Baseball",
    "description": "Lorem ipsum",
    "category_id": 3,
    "is_open": 1,
  },{
    "owner": 6,
    "title": "Python programming",
    "description": "Lorem ipsum",
    "category_id": 4,
    "is_open": 1,
  },{
    "owner": 7,
    "title": "System programming",
    "description": "Lorem ipsum",
    "category_id": 4,
    "is_open": 1,
  },{
    "owner": 8,
    "title": "Digital art",
    "description": "Lorem ipsum",
    "category_id": 2,
    "is_open": 1,
  },{
    "owner": 9,
    "title": "Oil art",
    "description": "Lorem ipsum",
    "category_id": 2,
    "is_open": 1,
  },{
    "owner": 10,
    "title": "Algebra",
    "description": "Lorem ipsum",
    "category_id": 8,
    "is_open": 1,
  },{
    "owner": 1,
    "title": "Discrete mathematics",
    "description": "Lorem ipsum",
    "category_id": 8,
    "is_open": 1,
  },{
    "owner": 2,
    "title": "Calculus",
    "description": "Lorem ipsum",
    "category_id": 8,
    "is_open": 1,
  },{
    "owner": 3,
    "title": "Foreign trade",
    "description": "Lorem ipsum",
    "category_id": 7,
    "is_open": 1,
  },{
    "owner": 4,
    "title": "Flower arrangement",
    "description": "Lorem ipsum",
    "category_id": 5,
    "is_open": 1,
  },{
    "owner": 5,
    "title": "German",
    "description": "Lorem ipsum",
    "category_id": 10,
    "is_open": 1,
  },{
    "owner": 6,
    "title": "Portuguese (Portugal)",
    "description": "Lorem ipsum",
    "category_id": 10,
    "is_open": 1,
  },{
    "owner": 7,
    "title": "Portuguese (Brazil)",
    "description": "Lorem ipsum",
    "category_id": 10,
    "is_open": 1,
  },],
  "trade_offers": [
    { "post_send": 1, "post_receive": 2 },
    { "post_send": 1, "post_receive": 3 },
    { "post_send": 1, "post_receive": 4 },
    { "post_send": 5, "post_receive": 1 },
    { "post_send": 6, "post_receive": 1 },
  ]
}