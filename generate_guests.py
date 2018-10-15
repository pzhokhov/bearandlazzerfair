import random
import string 
import argparse
import os
import yaml

def rand_str(N):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(N))


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--guestfile', default='guests.yaml')
    argparser.add_argument('--keylen', default=8)
    
    args = argparser.parse_args()

    guestfile_path = os.path.expanduser(args.guestfile)

    assert os.path.exists(guestfile_path), 'Guest list yaml file (guests.yaml) not found'

    print('Loading guest list ... ')
    with open(guestfile_path, 'r') as f:
        guest_list = yaml.load(f)
        
    print('Done')

    for g in guest_list:
        if g.get('key') is None or g.get('key') == 'xxx':
            print('Generating key for {}'.format(g['name']))
            g['key'] = rand_str(args.keylen)
       
    print('Saving updated guest list ... ')
    with open(guestfile_path, 'w') as f:
        yaml.dump(guest_list, f, default_flow_style=False)
    print('All done!')

if __name__ == '__main__':
    main()
