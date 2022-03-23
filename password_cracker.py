import hashlib
import concurrent.futures


database = {}


def thread_function(salt):
  print(salt)
  f_p = open("top-10000-passwords.txt", "r", encoding='utf-8')
  for p in f_p:
    p = p.replace ("\n", "")
    p = p.strip()
    hashed_pass = hashlib.sha1((p+salt).encode('utf-8')).hexdigest()
    database[hashed_pass] = p
    print('Raw text: {}  Hashed {}'.format(p+salt, hashed_pass))
    hashed_pass = hashlib.sha1((salt+p).encode('utf-8')).hexdigest()
    database[hashed_pass] = p
    print('Raw text: {}  Hashed {}'.format(salt+p, hashed_pass))
  f_p.close()
  print("Done job {}".format(salt))

    
def init_database():
  print("Load common passwords from file")
  f_s = open("known-salts.txt", "r", encoding='utf-8')
  known_salts = [""]
  for s in f_s: 
    s = s.replace ("\n", "")
    s = s.strip()
    known_salts.append(s)
  f_s.close()
  
  with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(thread_function, known_salts)
    

def test_database():
  print(database['614f12f9bb415a6368c3456d98e9c6d6bca3ed26'])
  print(database['c7ab388a5ebefbf4d550652f1eb4d833e5316e3e'])
  print(database['b305921a3723cd5d70a375cd21a61e60aabb84ec'])
  print(database['18c28604dd31094a8d69dae60f1bcd347f1afc5a'])


def crack_sha1_hash(hash, use_salts=False):
  if hash in database:
    return database[hash]
  return "PASSWORD NOT IN DATABASE"
    