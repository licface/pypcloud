Pcloud CLI
===================

Usage
================
	pcloud.py [-h] [-l] [-U USERNAME] [-P PASSWORD] [-A AUTH]
					 [-cp CHANGE_PASSWORD CHANGE_PASSWORD] [-F] [-Fi] [-L]
					 [-s SORT] [-re] [-f] [-T] [-i] [-x SET_AUTH_EXPIRE]
					 [-X [PROXY [PROXY ...]]] [-I INPUT_METHOD] [-S] [-t]
					 [-a [ARGV [ARGV ...]]] [-d] [-p DOWNLOAD_PATH] [-g]
					 [-r REMOTE_UPLOADS] [-rr CLEAR_REMOTE_UPLOADS]
					 [-rd REMOTE_UPLOADS_DOWNLOAD] [-n DOWNLOAD_NAME]
					 [-nn [DOWNLOAD_NUMBER [DOWNLOAD_NUMBER ...]]]
					 [-N LIST_NUMBER] [-u [UPLOADS [UPLOADS ...]]] [-R]
					 [-Ri REGISTER_INVITE] [-Ro REGISTER_OS] [--hash HASH]
					 [-cf CREATE_FOLDER] [-v] [-fi FOLDER_ID] [-fn FOLDER_NAME]
					 [-pi PARENT_ID] [-D]
					 [-DF [DELETE_FOLDERID [DELETE_FOLDERID ...]]]
					 [-Df [DELETE_FILEID [DELETE_FILEID ...]]]
					 [-Di [DELETE_ID [DELETE_ID ...]]]

	optional arguments:
	  -h, --help            show this help message and exit
	  -l, --login           Login
	  -U USERNAME, --username USERNAME
							Username Authentication
	  -P PASSWORD, --password PASSWORD
							Password Authentication
	  -A AUTH, --auth AUTH  Authentication Code
	  -cp CHANGE_PASSWORD CHANGE_PASSWORD, --change-password CHANGE_PASSWORD CHANGE_PASSWORD
							Change Password, format: oldpassword newpassword, or just enter pass with prompt
	  -F, --list-folder     List Folder, default root folder
	  -Fi, --folder-info    Get Info of Parent Folder, default root folder
	  -L, --list-content    List File or Directory
	  -s SORT, --sort SORT  Sort List File or Directory
	  -re, --reverse        Sort List File or Directory Reverse
	  -f, --list-file       List Files with given folder name or folder index, default folder index = 0
	  -T, --list-token      List Token
	  -i, --user-info       User Info
	  -x SET_AUTH_EXPIRE, --set-auth-expire SET_AUTH_EXPIRE
							Set Authentication Expired in Seconds
	  -X [PROXY [PROXY ...]], --proxy [PROXY [PROXY ...]]
							Set Proxy, format example http://127.0.0.1:8118 https://127.0.0.1:3128
	  -I INPUT_METHOD, --input-method INPUT_METHOD
							Change input method by insert a word then enter (default) or "msvcrt" = just input a word
	  -S, --save-config     Save config (authentication)
	  -t, --func            Test usage
	  -a [ARGV [ARGV ...]], --argv [ARGV [ARGV ...]]
							parameter/argument function
	  -d, --download        Download
	  -p DOWNLOAD_PATH, --download-path DOWNLOAD_PATH
							Download Path save to
	  -g, --get-currentserver
							Get Current Server
	  -r REMOTE_UPLOADS, --remote-uploads REMOTE_UPLOADS
							Remote Upload url
	  -rr CLEAR_REMOTE_UPLOADS, --clear-remote-uploads CLEAR_REMOTE_UPLOADS
							Clear Screen & Remote Upload url
	  -rd REMOTE_UPLOADS_DOWNLOAD, --remote-uploads-download REMOTE_UPLOADS_DOWNLOAD
							Remote Upload url then download it
	  -n DOWNLOAD_NAME, --download-name DOWNLOAD_NAME
							Rename after downloaded
	  -nn [DOWNLOAD_NUMBER [DOWNLOAD_NUMBER ...]], --download-number [DOWNLOAD_NUMBER [DOWNLOAD_NUMBER ...]]
							Direct download to number of list
	  -N LIST_NUMBER, --list-number LIST_NUMBER
							Numbers of list perline
	  -u [UPLOADS [UPLOADS ...]], --uploads [UPLOADS [UPLOADS ...]]
							Upload files
	  -R, --register        Register/SingUp
	  -Ri REGISTER_INVITE, --register-invite REGISTER_INVITE
							Register/SingUp Invite
	  -Ro REGISTER_OS, --register-os REGISTER_OS
							Register/SingUp OS
	  --hash HASH           Upload/Progress Hash or File hash
	  -cf CREATE_FOLDER, --create-folder CREATE_FOLDER
							Create Folder
	  -v, --debug           Debug Verbosity
	  -fi FOLDER_ID, --folder-id FOLDER_ID
							Folder ID
	  -fn FOLDER_NAME, --folder-name FOLDER_NAME
							Folder Name
	  -pi PARENT_ID, --parent-id PARENT_ID
							Parent ID
	  -D, --delete          Delete Action
	  -DF [DELETE_FOLDERID [DELETE_FOLDERID ...]], --delete-folderid [DELETE_FOLDERID [DELETE_FOLDERID ...]]
							Delete, parameter: folderid [list]
	  -Df [DELETE_FILEID [DELETE_FILEID ...]], --delete-fileid [DELETE_FILEID [DELETE_FILEID ...]]
							Delete, parameter: fileid  [list]
	  -Di [DELETE_ID [DELETE_ID ...]], --delete-id [DELETE_ID [DELETE_ID ...]]
							Delete, paramteer: id [list]


Author
===========
[LICFACE](mailto:licface@yahoo.com)

Debug
============
set system enviroment DEBUG=1 to show debug process 