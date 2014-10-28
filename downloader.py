#!/usr/bin/python

import sys, getopt, os
import libtorrent as lt
import time



def download_torrent(torrent_file, download_directory):
	ses = lt.session()
	ses.listen_on(6881, 6891)

	e = lt.bdecode(open(torrent_file, 'rb').read())
	info = lt.torrent_info(e)

	params = { 'save_path': download_directory,
	        'storage_mode': lt.storage_mode_t.storage_mode_sparse }
	h = ses.add_torrent(params)

	while (not h.is_seed()):
	        s = h.status()

	        state_str = ['queued', 'checking', 'downloading metadata', \
	                'downloading', 'finished', 'seeding', 'allocating']
	        print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
	                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
	                s.num_peers, state_str[s.state])

	        time.sleep(1)

def fix_directory(old_directory):
	if (old_directory[-1:] == "/"):
		return old_directory
	else:
		return old_directory + "/"

def main():
	torrent_file = ''
	download_directory = ''

	print "Arguments", str(sys.argv)
	zoom = sys.argv[1]
	myopts, args = getopt.getopt(sys.argv[1:], "z:d:f:o:")
	
	
	for o, a in myopts:
		if o == '-d':
			download_directory = a
		elif o == '-f':
			torrent_file = a

	directory = fix_directory(download_directory)
		
	print "Torrent File: ", torrent_file
	print "Download Directory: ", download_directory

	if (os.path.exists(torrent_file) != "" and os.path.isdir(download_directory)):
		download_torrent(torrent_file, download_directory);

main()

