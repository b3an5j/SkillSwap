import re

USERNAME_REGEX = re.compile(r"^[A-Za-z0-9_]+$")
DB_PATH = "database/database.sqlite"
SCHEMA_PATH = "database/schema.sql"
DUMMY_DATA = {
  "post_category": [
    { "category": "music" },
    { "category": "art" },
    { "category": "sports" },
    { "category": "programming" },
    { "category": "gardening" },
    { "category": "finance" },
    { "category": "economy" },
    { "category": "math" },
    { "category": "literature" },
    { "category": "language" }
  ],
  "users": [{
    "username": "cplomer0",
    "email": "gtrimnell0@people.com.cn",
    "password": "gcrannach0",
    "location": "Philippines"
  }, {
    "username": "ltamas1",
    "email": "rruilton1@tumblr.com",
    "password": "apitson1",
    "location": "Azerbaijan"
  }, {
    "username": "csmallacombe2",
    "email": "jcumbridge2@stanford.edu",
    "password": "jdows2",
    "location": "Japan"
  }, {
    "username": "smoncrieffe3",
    "email": "vmcgairl3@github.io",
    "password": "jkefford3",
    "location": "Indonesia"
  }, {
    "username": "cjeffries4",
    "email": "jsweet4@uiuc.edu",
    "password": "bvaisey4",
    "location": "South Africa"
  }, {
    "username": "jbardell5",
    "email": "kellerman5@sbwire.com",
    "password": "msanbrook5",
    "location": "Democratic Republic of the Congo"
  }, {
    "username": "kkrzysztofiak6",
    "email": "lsoutherton6@symantec.com",
    "password": "bechallier6",
    "location": "Argentina"
  }, {
    "username": "kbinestead7",
    "email": "ccorkan7@oracle.com",
    "password": "lmccaig7",
    "location": "Brazil"
  }, {
    "username": "lhaskey8",
    "email": "sdonoghue8@posterous.com",
    "password": "hmcnicol8",
    "location": "China"
  }, {
    "username": "rsetter9",
    "email": "khickenbottom9@unesco.org",
    "password": "wfilinkov9",
    "location": "Indonesia"
  }],
}